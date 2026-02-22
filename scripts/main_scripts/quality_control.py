from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd


def run_fastqc_quality_control(raw_read_1, raw_read_2, qc_output):

    # create FASTQC command for subprocess 
    cmd_fastqc = (["fastqc",            # qulatiy control tool for high througput sequencing data
                   raw_read_1,           # input read1
                   raw_read_2,           # input read2
                   "-o", qc_output])    # output folder

    # run suprocess via helper file
    run_cmd(cmd_fastqc)

    # create MULTIQC command for subprocess 
    cmd_multiqc = (["multiqc",         # aggregate results accross many samples into a single report
                    qc_output,         # input folder
                    "-o", qc_output])  # output folder

    # run suprocess via helper file
    run_cmd(cmd_multiqc)