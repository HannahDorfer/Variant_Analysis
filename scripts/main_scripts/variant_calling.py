import subprocess
from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd


def run_bcftools_variant_calling(ncbi_fasta, variant_vcf, pileup_bcf, aligend_sored_bam):
    
    # create commands for subprocess
    cmd_pileup = [  "bcftools",                 # utilizes for variant calling and manipulating VCF and BCF files
                     "mpileup",                 # multi-way pileup producing genotype likelihood
                     "-d", "10000",
                     "-f", ncbi_fasta,          # fasta reference file
                     "-Ou", "-o", pileup_bcf,   # output format: uncompressed BCF file, output path
                     aligend_sored_bam]         # input file 
    
    # run suprocess via helper file
    run_cmd(cmd_pileup)

    # create commands for subprocess
    cmd_variants = ["bcftools",                 # utilizes for variant calling and manipulating VCF and BCF files
                     "call",                    # SNP/indel calling
                     "-m",                      # multiallelic caller
                     "-A",                      # keep alternative allele if not present in any genotypes
                     "-*",                      # keep unobservable allele
                     "--ploidy", "1",           # haploid genome
                     "-Ov", "-o", variant_vcf,  # output format: uncompressed VCF file, output path
                     pileup_bcf]                # input path
    
    # run suprocess via helper file
    run_cmd(cmd_variants)