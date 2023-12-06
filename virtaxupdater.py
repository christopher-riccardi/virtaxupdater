#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code by Christopher Riccardi, PhD Student at University of Florence (Italy) https://www.bio.unifi.it/vp-175-our-research.html
Currently Guest Researcher at Sun Lab, University of Southern California, Los Angeles (USA) https://dornsife.usc.edu/profile/fengzhu-sun/
PhD Project Title: Computational modelling of omics data from condition-dependent datasets. Graduating Fall 2024.
Advisor: Marco Fondi (U Florence)
"""
import os
import sys
import logging
import argparse
import numpy as np
import pandas as pd

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
vmr_filename = "current_VMR"

"""
Subcommands:
    connect
    download
    update
"""  

def mkdir(output):
    logging.info(f'Creating directory {output}')
    try:
        os.mkdir(output)
    except:
        logging.info('There was an error creating your working directory. Please check if directory already exists')
        sys.exit(1)
    logging.info(f'Directory created. Use this as input for the other modules.')

def read_Excel(vmr_file):
    try:
        xlsx = pd.read_excel(vmr_file) ## Read Excel spreadsheet using pandas and openpyxl
    except:
        logging.info('There was an error reading your Excel spreadsheet. Was the working directory created?')
        sys.exit(1)
    df = xlsx[~xlsx['Virus GENBANK accession'].isnull()] ## Not all entries link GenBank. Use only rows where GenBank accession is available
    df.to_csv(vmr_file.replace('.xlsx', '.tsv'), sep='\t', index=False) ## Dump a non-Excel version, for easy bash scripting.
    return df

def GenBank_cleanup(accession):
    ## Parse a non-uniformly formatted file
    accsns = []
    if ': ' in accession: ## ': ' means there are strings to split
        accsns = [line.split(';')[0].replace(' ', '') for line in accession.split(':') if line.startswith(' ')]
    else:
        if '; ' in accession: ## Other cases
            accsns = accession.split('; ')
        else:
            if ';' in accession:
              accsns = accession.split(';')
            else:
              accsns = [accession]
    accsns = [elem.split()[0] for elem in accsns]
    accsns = [item for row in accsns for item in row.split(';')]
    return accsns

def run_Entrez(df, data_dir):
    ## Must have entrez installed. See https://www.ncbi.nlm.nih.gov/books/NBK179288/ for more.
    ## I used this in Linux kernel -> sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
    
    ## Get GenBank accessions from data frame. There can be multiple per row,
    ## so parse carefully every entry and record multiple GenBank files per virus.
    ## Generate a folder named 'Data' in ../ and make one directory per row.
    ## Download GenBank files systematically inside each directory/GenBank
    ## GenBank files (e.g., for entry "MF176343") are downloaded by using the following command:
        ## esearch -db nuccore -query "MF176343" | efetch -format genbank
    import subprocess
    logging.info('Will run esearch and efetch to download viral GenBank files.')
    genbank=df['Virus GENBANK accession'] ## These have been polished, and separated by a semicolon
    if genbank.empty:
        logging.info('There was an error processing your GenBank accessions. The relative VMR spreadheet column seems empty.')
        sys.exit(1)
        
    accsns = []
    files_processed = 0
    
    for i, accession in enumerate(genbank):
        accsns = accession.split(';')
        ## Now create a directory for every index, and download the sequences associated
        dir = os.path.join(data_dir, str(df.iloc[i]['Sort']))
        os.mkdir(dir)
        os.mkdir(os.path.join(dir, 'GenBank'))
        accessions_file=open(os.path.join(dir, 'accessions.txt'), 'w')
        print(*accsns, sep='\n', file=accessions_file)
        accessions_file.close()

        ## Might as well create the bash script and execute it from here
        bash_script = 'while read accession; do esearch -db nuccore -query "$accession" | efetch -format genbank > GenBank/"$accession".gb; done < <(cat accessions.txt)'
        print(bash_script, file=open(os.path.join(dir, 'download_genbank.sh'), 'w'))

        ## Change directory temporarily and execute bash script from within.
        cwd = os.getcwd()
        os.chdir(dir)
        cmd = ['bash', 'download_genbank.sh']
        subprocess.run(cmd)
        files_processed += len(os.listdir('GenBank'))
        
        ## Then come back to main wd
        os.chdir(cwd)
    logging.info(f'Downloaded {files_processed} GenBank files inside each subfolder at {data_dir}')
    
def VMR_Connect(url, vmr_file):
    ## Use urllib to download a local copy of the current VMR table from the ICTV.
    ## Note that this is the file you find by:
    ## (1) Navigating to https://ictv.global/
    ## (2) Under 'Taxonomy', selecting 'Virus Metadata Resource'
    ## (3) Clicking on 'Download Current Virus Metadata Resource (VMR)'
    ## This table is composed of 2 sheets, with the first sheet having 26 columns
    ## (First 3:'Sort', 'Isolate sort', 'Realm', Last 3: 'Genome coverage', 'Genome composition', 'Host source')
    from urllib.request import urlretrieve
    logging.info(f'Connecting to {url}')
    path, headers = urlretrieve(url, vmr_file)
    for name, value in headers.items():
        print(name, value, file=sys.stderr)
    logging.info(f'Done connecting. File should be at {vmr_file}')

def flag_errors(input):
    ## Look for empty GenBank files and flag them to a file called "flagged.txt".
    ## Either way, return a list of problematic files so that user can delete them and update the spreadsheet
    ## from within this script.
    outdated = set()
    for listdir in os.listdir(os.path.join(input, 'Data')):
        folder = os.path.join(os.path.join(os.path.join(input, 'Data'), listdir), 'GenBank')
        gbks = os.listdir(folder)
        for file in gbks:
            gb = os.path.join(folder, file)
            size = len(open(gb).readline())
            if size < 80:
                print(gb, file=open(os.path.join(input, 'flagged.txt'), 'a'))
                logging.info(f'Found potentially empty file at {gb}')
                outdated.add(os.path.join(os.path.join(input, 'Data'), listdir))
    if len(outdated) == 0:
        logging.info('No errors found in GenBank files. All good.')
    else:
        logging.info(f'{len(outdated)} files were potentially empty. Please check')
    return outdated

def delete_outdated(outdated):
  import shutil
  for folder in outdated:
      response = shutil.rmtree(folder)
      print(response)

def update_dataframe(df, outdated):
    empty = [int(os.path.basename(line)) for line in outdated]
    return df[~df['Sort'].isin(pd.Series(empty))]

def Excel_cleanup(df):
    ## Cleanup GenBank accession column, since it's heterogeneous. Update 'Virus GENBANK accession' on the TSV file
    cleanup = []
    for accession in df['Virus GENBANK accession']:
        acc_list = GenBank_cleanup(accession)
        acc_string = ";".join(acc_list)
        cleanup.append(acc_string)
    df['Virus GENBANK accession'] = cleanup
    return df

def connect(url, output):
    mkdir(output)
    vmr_file = os.path.join(output, vmr_filename + ".xlsx") ## Local copy of the VMR table
    VMR_Connect(url, vmr_file) ## Download current VMR file
    df = read_Excel(vmr_file)
    df = Excel_cleanup(df)
    df.to_csv(vmr_file.replace('.xlsx', '.tsv'), sep='\t', index=False) ## Dump a non-Excel version, for easy bash scripting.

def download(input):
    vmr_file = os.path.join(input, vmr_filename + ".xlsx") ## Local copy of the VMR table
    df = read_Excel(vmr_file)
    df = Excel_cleanup(df)
    df.to_csv(vmr_file.replace('.xlsx', '.tsv'), sep='\t', index=False) ## Dump a non-Excel version, for easy bash scripting.
    ## Create a Data directory where to store all the files!
    data_dir = os.path.join(input, 'Data')
    mkdir(data_dir)
    run_Entrez(df, data_dir)
    
def update(input, delete_dirs):
    vmr_file = os.path.join(input, vmr_filename + ".xlsx") ## Local copy of the VMR table
    df = read_Excel(vmr_file)
    df = Excel_cleanup(df)
    outdated = flag_errors(input)
    df = update_dataframe(df, outdated)
    df.to_csv(vmr_file.replace('.xlsx', '.tsv'), sep='\t', index=False) ## Dump a non-Excel version, for easy bash scripting.
    if delete_dirs:
        logging.info(f'Deleting outdated subfolders in {input}')
        delete_outdated(outdated)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    conn = subparsers.add_parser('connect')
    conn.add_argument(
        '-u', '--url', dest='url', default="https://ictv.global/vmr/current", help='Use urllib to download a local copy of the current VMR table from the ICTV')
    conn.add_argument(
        '-o', '--output', dest='output', required=True, help='Working directory in order for all subsequent modules to work!')

    #

    downl = subparsers.add_parser('download')
    downl.add_argument(
        '-i', '--input', dest='input', required=True, help='Working directory created by %s connect' % sys.argv[0])

    #

    up = subparsers.add_parser('update')
    up.add_argument(
        '-i', '--input', dest='input', required=True, help='Working directory created by %s connect' % sys.argv[0])
    up.add_argument(
        '-d', '--delete-dirs', dest='delete_dirs', action='store_true', help='Delete directories containing empty GenBank files')
    up.set_defaults(delete_dirs=False)
    #
    
    kwargs = vars(parser.parse_args())
    try:
        response = sys.argv[1]
    except:
        print(f'Usage: {sys.argv[0]} <Subcommands: connect, download, update>')
        sys.exit(1)
    globals()[kwargs.pop('subparser')](**kwargs)
    
    ## Done
    logging.info(f'Thank you for using {sys.argv[0]}')
