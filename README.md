# Variant_Analysis
small project to show pipeline structure and analyse variants of SARS-CoV2

---
## Folder Structure

```shell
.
├── config.yaml
├── env.yml
├── README.md
├── run_pipeline.py
└── scripts
    ├── helper_scripts
    │   └── run_suprocess.py
    └── main_scripts
        ├── alignment.py
        ├── analysis.py
        ├── download_data.py
        ├── quality_control.py
        ├── trimming.py
        └── variant_calling.py
```
--

## Pipeline discription
### 1. creates environment
tools and dependencies defined in env.yml
Path: env.yml
### 2. Loads config.yaml file
defines, links, output folders, filters and spike gene, therads
create all output folders

Path: config.yaml
### 3. Download FASTQ data
uses links defined in yaml file to download  SARS-CoV2 Fastq data (paired-end reads) from european nucleotide archive
[http://www.ebi.ac.uk/ena/browser/view/SRR23971484](http://www.ebi.ac.uk/ena/browser/view/SRR23971484)


Path: scripts/main_scripts/download_data.py

input folder:

ena_read1: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR239/084/SRR23971484/SRR23971484_1.fastq.gz

ena_read2: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR239/084/SRR23971484/SRR23971484_2.fastq.gz

output folder: 

raw_read1: data/input/raw_read1

raw_read2: data/input/raw_read2


### 4. Quality Control
checks quality of sequencing data using fastqc and multiqc

Path: scripts/main_scripts/quality_control.py

input folder: 

raw_read1: data/input/raw_read1

raw_read2: data/input/raw_read2

output folder: 

data/results/qc_output

### 5. Trimming
uses fastp for quality trimming
trimmes low quality bases from ends
removes short, bad reads

fastp = ultrafast all-in-one preprocessing ans quality control for FastQ data


Path: scripts/main_scripts/trimming.py

input folder: 

raw_read1: data/input/raw_read1

raw_read2: data/input/raw_read2

output folder:

trim_read1: data/results/trim_output/trim_read1

trim_read2: data/results/trim_output/trim_read2


### 5. Alignment

Path: scripts/main_scripts/alignment.py
#### 1. Reference genome
download ncbi reference fasta for wuhan SARS-CoV2 variant
path for download defined in config.yaml
#### 2. allign using minimap2
allign paired-end reads using minimap2

input:

trim_read1: data/results/trim_output/trim_read1

trim_read2: data/results/trim_output/trim_read2

output:

data/results/aligend_output/aligned.sam

#### 3. Convert, sort, index
using samtools

input: 

data/results/aligend_output/aligned.sam

output:

data/results/aligend_output/aligned.sorted.bam

### 6. Variant calling
using bcftools

Path: scripts/main_scripts/variant_calling.py

#### 1. mpileup
create bcf file

#### 2. call
SNP/indel calling
include all found variants also not SNP/indel calling

output: data/results/aligend_output

### 7. Analysis

Path: scripts/main_scripts/analysis.py

load data

parameters set in config.yaml
- filter based on min depth and min quality (cerate filtered output csv)
- load position of spike (add boolean column)

created plots

data/results/filt_variants_output/depth_distribution.png

data/results/filt_variants_output/mutation_types.png

data/results/filt_variants_output/spike_occurence.png

output: data/results/filt_variants_output/analysed_variants.csv

---

## How to use the pipeline

1. create/update and activate environment
2. run python pipeline
   
### conda
update or create environment
```bash
conda env update -f env.yml -n variant_env || conda env create -f env.yml -n variant_env
```
activate environment
```bash
conda activate variant_env
```
### micromamba
update or create environment
```bash
micromamba env update -f env.yml -n variant_env || micromamba env create -f env.yml -n variant_env
```
activate environment
```shell
micromamba activate variant_env 
```
### run pipline
```bash
python -u run_pipeline.py
```

