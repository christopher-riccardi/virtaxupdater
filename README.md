# Virtaxupdater  
#### With Virtaxupdater you can:  
* Download ICTV VMR exemplar viruses [GenBank Flat Files](https://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html)
* Extract meaningful information from records (DNA sequence, date, host and more)
* Update an existing data set
* Deploy or host ICTV VMR data on your own GitHub  

All in one simple framework! Keep scrolling for more info.  
<br>  
## Introduction   
### Download viral genomes by connecting to the latest ICTV Virus Metadata Resource (VMR)  

Hello, and welcome.  
As stated in https://ictv.global/vmr, the ICTV *chooses an exemplar virus for each species and the VMR provides a list of these exemplars (...) and includes the GenBank accession number for the genomic sequence of the isolate as well as the virus name, isolate designation, suggested abbreviation, genome composition, and host source*.  
<br>
Virtaxupdater automatically collects sequences and metadata associated to each exemplar virus in the latest VMR. It is a simple and powerful python framework with very little requirements that makes over 16,000 records available in less than 2 hours. Throughout this documentation we refer to the viral sequences, taxonomy, and additional information of the exemplars as **Exemplars**. We created a table containing all these information (yes even the DNA sequence) and this table can be downloaded from this repository, but it is partitioned due to size limit (total ~130MB). See [Accessing the Data](#accessing-the-data) to learn how to easily assemble it.  
<br>  
<ins>Windows users</ins>: Subcommands ```deflate``` and ```inflate``` work also on Windows, so you can download the **Exemplars** even if you're not a Linux user! See [Compatibility](#compatibility) for more information.    
<br>  
The currently hosted **Exemplars** derive from:  
* **VMR_MSL38_v2** Created 09/13/2023 - 17:32 https://ictv.global/vmr.   
<br>  

## Index  
[Accessing the Data](#accessing-the-data)  
[How to run](#how-to-run)  
[Installation](#installation)  
[Requirements](#requirements)  
[Querying the data](#querying-the-data)  
[Troubleshooting](#troubleshooting)  
[Compatibility](#compatibility)  

 <br>  
 
 ## Accessing the Data  
 Strictly speaking, you don't *need* to install Virtaxupdater to have access to the **Exemplars**. We split the table into several parts so that we could upload it on GitHub. You can download it from here, and use bash to re-assemble it. Simply download the Database folder in this repository, open a terminal in the directory containing it (<ins>don't</ins> *cd* into Database/) and ```Ctrl```+```C``` ```Ctrl```+```V``` this one-liner:
 ```bash
 :> exemplars.tsv.gz; while read part; do cat "$part" >> exemplars.tsv.gz; done < <(cat Database/deflate/parts.index)
 ```
That's it! Your date are in the form of this large, 31-column, tab-delimited, gzip-compressed table, **exemplars.tsv.gz**. Head over to [Querying the data](#querying-the-data) for a quick and easy run-through.  
Note, however, that you can also use Virtaxupdater to re-assemble the table, retrieve GenBank flat files, update existing versions of the **Exemplars** and much more.  
You can access the **Exemplars** on Windows too! Check out the [Compatibility](#compatibility) section to learn how to access the partitioned table using Virtaxupdater on any OS.   
 <br>
 [Back to Index](#index)  
 <br>  
 
 ## How to run  
 Virtaxupdater is composed of seven subcommands. Having the script broken down into seven modules makes it possible to perform separate tasks without running the entire pipeline every time. The thought process is pretty straightforward: there is a subcommand for each task to bring you from zero to hero in less than 2 hours.    
### Quick start: install and run Virtaxupdater
Use Virtaxupdater to download data from the VMR from scratch; this allows you to have full control over all files, including all GenBank flat files, from which you may wish to extract additional information your own way. This section lets you create a conda/mamba environment, download the Entrez Direct toolset needed to programmatically access the NCBI, make Virtaxupdater executable, and run four essential commands. Here goes something.  
Assuming you have conda or better yet, **mamba**, you will first run ```conda create -n vtu -c conda-forge biopython openpyxl pandas -y``` to create a new environment called vtu. It only costs a few minutes of your time and helps avoid library conflicts. Then run ```sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"``` to install [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/) (it takes 30 seconds, agree to everything the installer wants). After cloning the repository, make it executable with the command ```chmod +x virtaxupdater; conda activate vtu``` and finally run the four essential subcommands:  
 ```bash
./virtaxupdater connect -i myfolder
./virtaxupdater index -i myfolder
./virtaxupdater download -i myfolder
./virtaxupdater extract -i myfolder
 ```
That's it, you should find a large tab-delimited, gzipp'd table at myfolder/exemplars.tsv.gz in less than 2 hours. Head over to [Querying the data](#querying-the-data) for a quick and easy run-through.  

### Subcommands  
Every subcommand requires the ```-i INPUT``` command line argument, which is the name of the working directory where you will store the **Exemplars**. As you can see from the previous example, the first command we run is ```./virtaxupdater connect -i myfolder``` and it is recommended that ```myfolder``` does not exist. Most, but not all, subcommands create a directory with their name. This is an internal detail for better data organization. The subcommands are:  
<br>
```connect```  
```
usage: connect [-h] [-u URL] -i INPUT  
```
Establish connection with the ICTV Virus Metadata Resource (VMR), and download the current VMR spreadsheet. In 2023, this is a two-sheet table with the first sheet being
informative of virus exemplars (it contains 26 columns, find it on this repo at Database/connect/vmr_spreadsheet.xlsx). If the ICTV moves the spreadsheet elsewhere and the script fails (let us know) you have two options: either
specify the url using the -u command line option, or manually move the spreadsheet to the "connect" directory, renaming it to "vmr_spreadsheet.xlsx".  
<br>

```index```    
```
usage: index [-h] -i INPUT
```  
The VMR spreadsheet contains one exemplar per row. Exemplars are identified by a "Sort" integer. Occasionally, for segmented viruses, the GenBank cell in a row contains
multiple GenBank accessions. (e.g., segmented viruses -> SegA: JX403941; SegB: JX403942) or (e.g., Polydnaviriformidae -> C1: AJ632304; C2: AJ632305; C3: AJ632306; etc
etc). There are also cases with <accession> (start.end) ( e.g., LK928904 (2253.10260) ) where the viral sequence is confined to a range within a larger contig. Parse
these one by one to obtain a "long"-formatted table, having one accession per row. The index file is used by the subsequent subcommands for accessing data at multiple
levels, so it is stored in JSON format to allow easy I/O, especially since it is continuously updated by the final subcommands.  
<br>  

```update```    
```
usage: update [-h] -i INPUT
```
Compute a diff between an existing database and a possible update from the ICTV so that later, the "download" subcommand can download the additional files only, without
querying Entrez again.  
<br>  

```download```    
```
usage: download [-h] [-b BATCH_SIZE] -i INPUT  
```
Use [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/) to download genbank files by accession. Entrez allows to download batches of up to 100 accession at a
time. This is much faster than single downloads.  
<br>  

```extract```
```
usage: extract [-h] -i INPUT  
```
Go through the freshly downloaded GenBank files, one by one, and extract information. Here we use the Biopython module for a straightforward access to each record. Note
that occasionally the nucleotide sequence is not found. In such cases, the program tries downloading it again using Entrez Direct with the "-fasta" flag. Note also: "extract"
is probably the last module you need, since it creates a tab-delimited, compressed table containing 31 columns, with information ranging from host, contry and date to the
complete ICTV taxonomy and DNA sequence.  
<br>  

```deflate```
```
usage: deflate [-h] [-m Megabytes] -i INPUT  
```
Split the large table into smaller, binary files. These can be reassembled later using the "inflate" subcommand on the same directory. This is useful if deploying the
database on a webapp or, like us, uploading it on GitHub.  
<br>  

```inflate```
```
usage: inflate [-h] -i INPUT  
```
Put together the binary files that were split using "deflate". This will create a directory named "inflate" with the reconstructed tab-delimited, compressed data table.  
<br>

 [Back to Index](#index)  
 <br>  
 
 ## Installation  
 Virtaxupdater is a python script that does not require a formal installation. Its dependencies, however, do. Check out the [Requirements](#requirements) section for more information.  
 <br>
 [Back to Index](#index)  
 <br>  
 
 ## Requirements  
 (1) Virtaxupdater uses [pandas](https://pypi.org/project/pandas/) + [openpyxl](https://pypi.org/project/openpyxl/) for I/O on large data frames or Excel spreadsheets. While the former is likely already installed on your computer, the latter isn't unless you specifically installed it.  
 (2) [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/) is a command line toolset for programmatic access to the NCBI's suite of interconnected databases (publication, sequence, structure, gene, variation, expression, etc.). Its installation is really easy (see point 4).  
 (3) The GenBank flat files downloaded using Entrez Direct can be parsed using [Biopython](https://anaconda.org/conda-forge/biopython), without having to reinvent the wheel.  
 (4) If you wish to create a conda/mamba environment from which to use Virtaxupdater, this is how you can install the dependencies:  
 ```bash
conda create -n vtu -c conda-forge biopython openpyxl pandas -y
sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
 ```
  *Disclaimer: conda is great, but for those type of projects we strongly recommend that you use [mamba](https://github.com/conda-forge/miniforge/#Download) instead.*  
 <br>  
 [Back to Index](#index)  
 <br>  
 
 ## Querying the Data  
 This section provides a brief demonstration on reading and understanding the **Exemplars**. It assumes you know how to use basic pandas functions for tabular data analysis. For further display of compatibility, we run these commands on Windows: \*nix users surely will know how to re-adapt the code to fit their need. Here we simply open a terminal in the working directory that contains the Database folder downloaded from this repository.   
```python
## Imports
>>> import pandas as pd
>>> import numpy as np
>>> import seaborn as sns # Optional, for data visualization
>>> import matplotlib.pyplot as plt # Same

## Load the Exemplars
>>> df = pd.read_csv('Database\inflate\exemplars.tsv.gz', sep='\t', compression='gzip') # Tab-delimited, gzipp'd file

## Query the data frame
>>> df.shape # Rows and columns in my data set
(16383, 31)

>>> df.columns # Column names
Index(['accession', 'sort', 'virus_name', 'host', 'host_VMR', 'partition',
       'molecule_type', 'genome_composition', 'topology', 'genome_coverage',
       'exemplar_additional', 'date', 'country', 'length', 'gc_fraction',
       'sequence', 'Realm', 'Subrealm', 'Kingdom', 'Subkingdom', 'Phylum',
       'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family',
       'Subfamily', 'Genus', 'Subgenus', 'Species'],
      dtype='object')
>>> np.unique(df[df['Species'].duplicated()]['Species']).size # Exemplars with duplicated Species names
1566

>>> df.describe()[['length', 'gc_fraction']][1:] # Descriptive statistics for genome length and G+C content of sequences
            length  gc_fraction
mean  2.979801e+04     0.453533
std   9.925672e+04     0.087242
min   1.660000e+02     0.177812
25%   2.739000e+03     0.392925
50%   6.665000e+03     0.441712
75%   3.570750e+04     0.504307
max   4.857450e+06     0.785244

>>> df['genome_coverage'].value_counts() # Counts of genome coverage descriptions across the data
Complete genome           13061
Coding-complete genome     1464
Complete coding genome      939
Partial genome              912
partial genome                7
Name: genome_coverage, dtype: int64

>>> df[df['length']==df['length'].min()][['Realm', 'genome_coverage', 'date']] ## Realm, genome coverage and edit date of the record with the smallest genome 
           Realm genome_coverage         date
12451  Riboviria  Partial genome  09-JAN-2014

>>> sns.kdeplot(df['gc_fraction']) # Frequency of G+C content across all exemplars
<Axes: xlabel='gc_fraction', ylabel='Density'>
>>> plt.show()
```
![kdeplot](https://github.com/christopher-riccardi/virtaxupdater/assets/119225793/999257a6-b3b2-4584-8d69-d2147d31e048)

```python
## Finally, write a FASTA file ('exemplars_multifasta.fa') containing all the sequences 
>>> print(*df['sequence'].to_list(), sep='\n', file=open('exemplars_multifasta.fa', 'w'))
>>> quit()
```
It is within reach to to convert this to an actual SQL database, depending on the usage and impact it will have.  
 <br>  
 [Back to Index](#index)  
 <br>  
 
 ## Troubleshooting  
 This section is empty because the repository is new.  To avoid issues we would advise you create a conda/mamba environment and run the program from there. Try not to move files around, all you need at the end of the day is the **Exemplars** table and, potentially, the GenBank flat files. See [How to run](#how-to-run) for a detailed explanation of the subcommands.   
 <br>  
 [Back to Index](#index)  
 <br>  
 
 ## Compatibility  
 <ins>Important</ins>: if you're using Windows you can still download the VMR Spreadsheet and the **Exemplars** hosted at this repository! All commands except ```download``` and ```extract``` work on Windows\*, therefore virtually anyone with internet access can download the data. Here is how you can re-assemble the partitioned **Exemplars**, on any OS:  
```bash
# 1. Clone Virtaxupdater as well as the Database directory
# 2. Run the script explicitly using the python interpreter. Here we use 'python' but yours may be 'python3'
# 3. Note that I am using Windows 10, and the output informs me of the successful outcome

python virtaxupdater inflate -i Database

#(v) This is Virtaxupdater version 1.0.0

#15-Dec-23 00:18:29 - CreateDirectory:457 [INFO] Successfully created/updated directory at Database
#15-Dec-23 00:18:29 - CreateDirectory:457 [INFO] Successfully created/updated directory at Database\inflate
#15-Dec-23 00:18:29 - inflate_subcommand:366 [INFO] Inflating table from 6 .part files
#15-Dec-23 00:18:29 - inflate_subcommand:371 [INFO] Your table is ready at Database\inflate\exemplars.tsv.gz
```
Once you obtain the **Exemplars** at Database\inflate\exemplars.tsv.gz, you're good to go. Check out the [Querying the data](#querying-the-data) section for a brief demonstration.  
\*We tested Virtaxupdater on Linux kernel only, but we suspect that it might work also on MacOS. When it comes to Windows, according to Entrez Direct's documentation: *EDirect will run on Unix and Macintosh computers, and under the Cygwin Unix-emulation environment on Windows PCs*. If you're willing to test it on Windows + Cygwin please let us know the outcome!  
 <br>  
 [Back to Index](#index)  
 <br>  



 
