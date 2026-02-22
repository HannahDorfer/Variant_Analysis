from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd

def run_alignment(ncbi_download, ncbi_fasta, trim_read_1, trim_read_2, aligned_sam, cpu, aligend_bam, aligend_sored_bam):

    print("Start loading reference data (fasta file from ncbi).")
    download_ncbi_fasta(ncbi_fasta, ncbi_download)
    print("Start minimpa2_alignment.")
    minimap2_alignment(trim_read_1, trim_read_2, ncbi_fasta, aligned_sam, cpu)
    print("Start converting SAM to BAM format.")
    create_BAM(aligned_sam, aligend_bam, aligend_sored_bam)


def download_ncbi_fasta(ncbi_fasta, ncbi_download):
    # get reference data from ncbi
    cmd_curl = (["curl", 
                 "-o", ncbi_fasta, # output path and filename
                 "-L", ncbi_download])    # input path https

    # run suprocess via helper file
    run_cmd(cmd_curl)


def minimap2_alignment(trim_read_1, trim_read_2, ncbi_fasta, aligned_sam, cpu):

    # create commands for subprocess
    cmd_minimap2 = (["minimap2",            # versatile sequence alignment tool
                     "-a",                  # creates SAM format (sequence alignment map)
                     "-x", "sr",            # selects parameters for short read (for illumina data)
                     "-t", cpu,             # cpu usage
                     ncbi_fasta,              # reference database
                     trim_read_1,           # input read1
                     trim_read_2,           # input read2
                     "-o", aligned_sam])    # output file

    # run suprocess via helper file
    run_cmd(cmd_minimap2)


def create_BAM(aligned_sam, aligend_bam, aligend_sored_bam):

    # create commands for subprocess
    cmd_bam = (["samtools",                 # tool for manipulating SAM (Sequence Alignment/Map)
                     "view",
                     "-b",                  # change output format to BAM
                     aligned_sam,           # input file
                     "-o", aligend_bam])    # output file

    # run suprocess via helper file
    run_cmd(cmd_bam)

    # create commands for subprocess
    cmd_bam_sorted = (["samtools",              # tool for manipulating SAM (Sequence Alignment/Map)
                     "sort",                    # sort alignments by leftmost coordinates
                     aligend_bam,               # input file
                     "-o", aligend_sored_bam])  # output file

    # run suprocess via helper file
    run_cmd(cmd_bam_sorted)

    # create commands for subprocess
    cmd_bam_index = (["samtools",           # tool for manipulating SAM (Sequence Alignment/Map)
                     "index",               # add index to file
                     aligend_sored_bam])    # oinput file

    # run suprocess via helper file
    run_cmd(cmd_bam_index)
