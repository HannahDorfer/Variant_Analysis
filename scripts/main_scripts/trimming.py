from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd

def run_fastp_trimming(raw_read_1, raw_read_2, trim_read_1, trim_read_2, trim_html, trim_json):


    # create commands for subprocess
    cmd_fastp = (["fastp",              # ultrafast all-in-one preprocessing ans quality control for FastQ data
                  "-i", raw_read_1,      # input read1
                  "-I", raw_read_2,      # input read2
                  "-o", trim_read_1,    # output trimmed read1
                  "-O", trim_read_2,    # output trimmed read2
                  "-h", trim_html,      # output html file
                  "-j", trim_json])     # output json file

    # run suprocess via helper file
    run_cmd(cmd_fastp)