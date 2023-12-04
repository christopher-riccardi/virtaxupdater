# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import subprocess
from urllib.request import urlretrieve

print("Disclaimer:\n\tThere's a chance you may have to install openpyxl.")
print("\tIt is very easy to do so. Simply run 'conda install openpyxl' or 'pip install openpyxl'")
print("\tThis is a useful library that lets you easily read Excel spreadsheets into Pandas DataFrames")
print("\nCode by: Christopher Riccardi, PhD Student @ U Florence | Guest Researcher @ University of Southern California")
print()
#### Functions

def VMR_Connect(url="https://ictv.global/vmr/current"):
    ## Use urllib to download a local copy of the current VMR table from the ICTV.
    ## Note that this is the file you find by:
    ## (1) Navigating to https://ictv.global/vmr/current
    ## (2) Under 'Taxonomy', selecting 'Virus Metadata Resource'
    ## (3) Clicking on 'Download Current Virus Metadata Resource (VMR)'
    ## This table is composed of 2 sheets, with the first sheet having 26 columns
    ## (First 3:'Sort', 'Isolate sort', 'Realm', Last 3: 'Genome coverage', 'Genome composition', 'Host source')
    
    vmr_file = "current_VMR.xlsx" ## Local copy of the VMR table
    path, headers = urlretrieve(url, vmr_file)
    for name, value in headers.items():
            print(name, value)
    return vmr_file

def download_GenBank(df):
    ## Get GenBank accessions from data frame. There can be multiple per row,
    ## so parse carefully every entry and record multiple GenBank files per virus.
    ## Generate a folder named 'Data' in ../ and make one directory per row.
    ## Download GenBank files systematically inside each directory/GenBank
    ## GenBank files (e.g., for entry "MF176343") are downloaded by using the following command:
        ## esearch -db nuccore -query "MF176343" | efetch -format genbank
    genbank=df['Virus GENBANK accession']
    arr = []
    files = 0
    os.mkdir('../Data') ## Creating a Data directory in ../ 
    for i, accession in enumerate(genbank):
        ## Parse a non-uniformly formatted file
        if ': ' in accession: ## ': ' means there are strings to split
            arr = [line.split(';')[0].replace(' ', '') for line in accession.split(':') if line.startswith(' ')]
        else:
            if '; ' in accession: ## Other cases
                arr = accession.split('; ')
            else:
                if ';' in accession:
                  arr = accession.split(';')
                else:       
                  arr = [accession]
        arr = [elem.split()[0] for elem in arr]
        arr = [item for row in arr for item in row.split(';')]
        
        ## Now create a directory for every index, and download the sequences associated
     
        dir = os.path.join('../Data/', str(df.iloc[i]['Sort']))
        os.mkdir(dir)
        os.mkdir(os.path.join(dir, 'GenBank'))
        metadata=open(os.path.join(dir, 'metadata.txt'), 'w')
        print(*arr, sep='\n', file=metadata)
        metadata.close()

        bash_script = 'while read accession; do esearch -db nuccore -query "$accession" | efetch -format genbank > GenBank/"$accession".gb; done < <(cat metadata.txt)'
        print(bash_script, file=open(os.path.join(dir, 'download_genbank.sh'), 'w'))

        ## Change directory temporarily and execute bash script from within.
        cwd = os.getcwd()
        os.chdir(dir)
        cmd = ['bash', 'download_genbank.sh']
        subprocess.run(cmd)
        files += len(os.listdir('GenBank'))
        
        ## Then come back to main wd
        os.chdir(cwd)
    print(f'Downloaded {files} files. Check ../Data/')

#### Procedural
### Here's a commented helpful list of columns ['Realm', 'Subrealm', 'Kingdom', 'Subkingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species', 'Virus name(s)', 'Host source']
## (1) Optional, download VMR
VMR_Connect()

## (2) Read Excel spreadsheet using pandas and openpyxl
xlsx = pd.read_excel('current_VMR.xlsx')

## (3) If using exec(), here's a subset of the data for rapid assessment
sample = xlsx.sample(100)

## (4) Not all entries link GenBank. Use only rows where GenBank accession is available
df = xlsx[~xlsx['Virus GENBANK accession'].isnull()]

## (5) Dump a non-Excel version, for easy bash scripting.
df.to_csv('current_VMR.tsv', sep='\t', index=False)

## (6) Iterate table rows and download per-virus GenBank files. 
download_GenBank(df)

