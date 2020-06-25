#!/usr/bin/env python3
import subprocess as sp

def genome_index(config, ref, path):
    """
    Generating genome indices for minimap2
    """
    reference = config["genome"][ref]
    cmd = "ln -s " + reference + " " + path + "/" + ref + "_genome.fa;"
    cmd += config["mapping"]["mapping_cmd"] +" "+ config["mapping"]["index_options"] + " "
    cmd += path + "/" + ref + "_genome.mmi "
    cmd += path + "/" + ref + "_genome.fa "
    sp.check_call(cmd, shell=True)


def mapping_dna(config):
    """
    Mapping DNA using minimap2
    """
    genome_index(config)
    organism = config["data"]["ref"]

    cmd = config["mapping"]["mapping_cmd"]+" "
    cmd += config["mapping"]["mapping_dna_options"]+" "
    cmd += config["data"]["mapping"] + "/" + organism + "_genome.fa "
    cmd += config["info_dict"]["fastq"]+ "/" + config["data"]["Sample_Name"]+".fastq.gz |"
    cmd += config["mapping"]["samtools_cmd"]+" sort "+config["mapping"]["samtools_options"]
    cmd += " -o "+ config["data"]["mapping"] + "/" +config["data"]["Sample_Name"]+".bam ; "
    cmd += config["mapping"]["samtools_cmd"]+ " index "
    cmd += config["data"]["mapping"] + "/" +config["data"]["Sample_Name"]+".bam"
    sp.check_call(cmd, shell=True)


def mapping_rna(config, data, ref):
   """
   Mapping RNA using minimap2
   """
   # TODO different organism on the same flowcell
   for k, v in data.items():	
        group=v["Sample_Project"].split("_")[2]
        final_path = config["paths"]["groupDir"]+"/"+group+"/sequencing_data/"+config["input"]["name"]
        analysis_dir = final_path+"/Analysis_"+v["Sample_Project"]+"/mapping_on_"+ref
        genome_index(config,ref, analysis_dir)
        cmd = config["mapping"]["mapping_cmd"]+ " "
        cmd += config["mapping"]["mapping_rna_options"]
        cmd += " --junc-bed "+config["transcripts"][ref] + " "
        cmd += config["data"]["mapping"] + "/" + ref + "_genome.fa "
        cmd += config["info_dict"]["flowcell_path"]+"/Project_"+v["Sample_Project"]+"/Sample_"+v["Sample_ID"]+"/"+v["Sample_Name"]+".fastq.gz | "
        cmd += config["mapping"]["samtools_cmd"]+ " sort "+ config["mapping"]["samtools_options"]
        cmd += " -o "+ analysis_dir + "/" +v["Sample_Name"]+".bam ; "
        cmd += config["mapping"]["samtools_cmd"]+ " index "
        cmd += analysis_dir + "/" +v["Sample_Name"]+".bam"
        print(cmd)
        sp.check_call(cmd, shell=True)


# def transcriptome_index(config):
#     """
#     Generating indeces for transcriptome
#     """
#     organism = config["data"]["ref"]
#     cmd = config["mapping"]["bedtools_cmd"] +" getfasta "+ config["mapping"]["bedtools_option"]
#     cmd += " -fi " + config["genome"][organism]
#     cmd += " -bed " + config["transcripts"][organism]
#     cmd += " > " + config["data"]["mapping"] + "/" + organism + "_transcripts.fa; "
#     cmd += "sed -i \"s/(+)//; s/(-)//\" "
#     cmd += config["data"]["mapping"] + "/" + organism + "_transcripts.fa;"
#     cmd += config["mapping"]["mapping_cmd"] + " " + config["mapping"]["index_options"] + " "
#     cmd += config["data"]["mapping"] + "/" + organism + "_transcripts.mmi "
#     cmd += config["data"]["mapping"] + "/" + organism + "_transcripts.fa "
#     sp.check_call(cmd, shell=True)
#
# def mapping_rna(config):
#     """
#     mapping RNA using minimap2
#     """
#     transcriptome_index(config)
#     organism = config["data"]["ref"]
#     cmd = config["mapping"]["mapping_cmd"]+" "
#     cmd += config["mapping"]["mapping_options"]+" "
#     cmd += config["data"]["mapping"] + "/" + organism + "_transcripts.fa "
#     cmd += config["info_dict"]["fastq"]+ "/" + config["data"]["Sample_Name"]+".fastq.gz |"
#     cmd += config["mapping"]["samtools_cmd"]+ " sort "+ config["mapping"]["samtools_options"]
#     cmd += " -o "+ config["data"]["mapping"] + "/" +config["data"]["Sample_Name"]+".bam ; "
#     cmd += config["mapping"]["samtools_cmd"]+ " index "
#     cmd += config["data"]["mapping"] + "/" +config["data"]["Sample_Name"]+".bam"
#     print(cmd)
#     sp.check_call(cmd, shell=True)

