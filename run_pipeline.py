from pathlib import Path
import yaml

from scripts.main_scripts.download_data import run_download_reads
from scripts.main_scripts.quality_control import run_fastqc_quality_control
from scripts.main_scripts.trimming import run_fastp_trimming
from scripts.main_scripts.alignment import run_alignment
from scripts.main_scripts.variant_calling import run_bcftools_variant_calling
from scripts.main_scripts.analysis import run_analysis_and_filtering


def main():
    # load config file
    config = yaml.safe_load(Path("config.yaml").read_text())

    # cpu 
    cpu = str(config["therads"])

    # create output folder if not exist
    for name, folder in config["output_folder"].items():
        Path(folder).mkdir(parents=True, exist_ok=True)

    # paths for downloading data script
    ena_read_1 = str(config["ena_download"]["ena_read1"])
    ena_read_2 = str(config["ena_download"]["ena_read2"])
    # paths for rawdata
    raw_read_1 = Path(config["output_folder"]["raw_read1"]) / "raw_read1.fastq.gz"
    raw_read_2 = Path(config["output_folder"]["raw_read2"]) / "raw_read2.fastq.gz"
    # path for quality control
    qc_output = Path(config["output_folder"]["qc_output"])
    # paths for trimming
    trim_read_1 = Path(config["output_folder"]["trim_read1"]) / "trimmed_read1.fastq"
    trim_read_2 = Path(config["output_folder"]["trim_read2"]) / "trimmed_read2.fastq"
    trim_html = Path(config["output_folder"]["trim_out"]) / "fastp.html"
    trim_json = Path(config["output_folder"]["trim_out"]) / "fastp.json"        
    # paths for downloading reference data
    ncbi_download = Path(config["ncbi_download"])
    ncbi_fasta = Path(config["output_folder"]["ncbi_data"]) / "sars_cov2_wuhan.fasta"
    # paths for alignment
    aligned_sam = Path(config["output_folder"]["aligned_output"]) / "aligned.sam"
    aligend_bam = Path(config["output_folder"]["aligned_output"]) / "aligned.bam"
    aligend_sored_bam = Path(config["output_folder"]["aligned_output"]) / "aligned.sorted.bam"
    # paths for variant calling
    variant_vcf = Path(config["output_folder"]["variant_output"]) / "variants.vcf"
    pileup_bcf = Path(config["output_folder"]["variant_output"]) / "pileup.bcf"
    # get filtering thersholds
    min_depth = int(config["variant_filters"]["min_depth"])
    min_qual = int(config["variant_filters"]["min_quality"]) 
    # get spike parameters
    spike_start = int(config["genes"]["spike"]["start"])
    spike_end = int(config["genes"]["spike"]["end"])
    # path for csv's
    not_filtered_data = Path(config["output_folder"]["filt_variants"]) / "not_filtered_data.csv"
    filtered_data= Path(config["output_folder"]["filt_variants"]) / "filtered_data.csv"
    analysed_variants = Path(config["output_folder"]["filt_variants"]) / "analysed_variants.csv"
    # paths to png
    png_mutation_types = Path(config["output_folder"]["filt_variants"]) / "mutation_types.png"
    png_depth_distr= Path(config["output_folder"]["filt_variants"]) / "depth_distribution.png"
    png_spike_occurence= Path(config["output_folder"]["filt_variants"]) / "spike_occurence.png"

    print("Start Variant Analysis Pipeline ...")
    # download data
    run_download_reads(raw_read_1, raw_read_2, ena_read_1, ena_read_2)
    # analyse quality
    run_fastqc_quality_control(raw_read_1, raw_read_2, qc_output)
    # trimm sequencing data
    run_fastp_trimming(raw_read_1, raw_read_2, trim_read_1, trim_read_2, trim_html, trim_json)
    # run allignemnt
    run_alignment(ncbi_download, ncbi_fasta, trim_read_1, trim_read_2, aligned_sam, cpu, aligend_bam, aligend_sored_bam)
    # run variant calling
    run_bcftools_variant_calling(ncbi_fasta, variant_vcf, pileup_bcf, aligend_sored_bam)
    # run analysis
    run_analysis_and_filtering(variant_vcf, min_depth, min_qual, spike_start, spike_end, not_filtered_data, filtered_data, analysed_variants, png_mutation_types, png_depth_distr, png_spike_occurence)
    print("Finished Pipeline.")

if __name__ == "__main__":
    main()