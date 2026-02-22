from pathlib import Path
from scripts.helper_scripts.run_suprocess import run_cmd

def run_download_reads(raw_read_1, raw_read_2, ena_read_1, ena_read_2):
    
    # create commands for subprocess
    # read 1
    cmd_read_1 = ["wget",               # package for retrieving files using HTTP, HTTPS, FTP, FTPS
                   "-nc",               # not overwriting existing files
                   "-O", raw_read_1,    # output folder
                   ena_read_1]          # input path (FTP)
    
    # read 2
    cmd_read_2 = ["wget",              # package for retrieving files using HTTP, HTTPS, FTP, FTPS
                   "-nc",              # not overwriting existing files
                   "-O", raw_read_2,   # output folder
                   ena_read_2]         # input path (FTP)

    # run suprocess via helper file
    run_cmd(cmd_read_1)
    run_cmd(cmd_read_2)
