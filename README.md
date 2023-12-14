# Virtaxupdater  
#### With Virtaxupdater you can:  
* Download ICTV VMR exemplar viruses [GenBank Flat Files](https://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html)
* Extract meaningful information from records (DNA sequence, date, host and more)
* Update an existing data set
* Deflate/Inflate data for hosting ICTV VMR on your own GitHub  

All in one simple framework! Keep scrolling for more info.  
<br>  
## Introduction   
### Download viral genomes by connecting to the latest ICTV Virus Metadata Resource (VMR)  

Hello, and welcome.  
As stated in https://ictv.global/vmr, the ICTV *chooses an exemplar virus for each species and the VMR provides a list of these exemplars (...) and includes the GenBank accession number for the genomic sequence of the isolate as well as the virus name, isolate designation, suggested abbreviation, genome composition, and host source*.  
<br>
Virtaxupdater automatically collects sequences and metadata associated to each exemplar virus in the latest VMR. It is a simple and powerful python framework with very little requirements that makes over 16,000 records available in less than 2 hours. Throughout this documentation we refer to the viral sequences, taxonomy, and additional information of the exemplars as **the Data**. The Data is available for download through this repository, but it is partitioned due to size limit (total ~130MB). See [Accessing the Data](#accessing-the-data) to learn how to assemble it. Note that we tested this framework on a Linux kernel only.   
The currently hosted Data derives from:  
* **VMR_MSL38_v2** Created 09/13/2023 - 17:32 https://ictv.global/vmr.   
<br>  

## Index  
[Accessing the Data](#accessing-the-data)  
[How to run](#how-to-run)  
[Installation](#installation)  
[Requirements](#requirements)  
[Querying the data](#querying-the-data)  
[Troubleshooting](#troubleshooting)  
[Future developments](#future-developments)  
 <br>
 ## Accessing the Data  
 Strictly speaking, you don't *need* to install Virtaxupdater to have access to the VMR. We split the Data into several parts so that we could upload it on GitHub. You can download it from here, and use bash to re-assemble it. Simply download the Database folder in this repository, open a terminal in the directory containing it (<ins>don't</ins> *cd* into Database/) and ```Ctrl```+```C``` ```Ctrl```+```V``` this one-liner:
 ```bash
 :> exemplars.tsv.gz; while read part; do cat "$part" >> exemplars.tsv.gz; done < <(cat Database/deflate/parts.index)
 ```
That's it! Your data are in this large, 31-column, tab-delimited, gzip-compressed table, **exemplars.tsv.gz**. Head over to [Querying the data](#querying-the-data) for a quick and easy run-through.  
Note, however, that you can also use Virtaxupdater to re-assemble the data, retrieve GenBank flat files, update existing versions of the Data and much more.   
 <br>
 [Back to Index](#index)  
 <br>  
 
 ## How to run  
 Virtaxupdater is composed of seven subcommands. Having the script broken down into seven modules makes it possible to perform separate tasks without running the entire pipeline every time. The thought process is pretty straightforward: there is a subcommand for each task to bring you from zero to VMR-hero in less than 2 hours.    
### Quick start: install and run Virtaxupdater
Use Virtaxupdater to download data from the VMR from scratch; this allows you to have full control over all files, including all GenBank flat files, from which you may wish to extract additional information your own way. This section lets you create a conda/mamba environment, download the Entrez Direct toolset needed to programmatically access the NCBI, make Virtaxupdater executable, and run four essential commands. Here we go.  
Assuming you have conda or better yet, **mamba**, you will first run ```conda create -n vtu -c conda-forge biopython openpyxl pandas -y``` to create a new environment called vtu. It only costs a few minutes of your time and helps avoid library conflicts. Then run ```sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"``` to install [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/) (it takes 30 seconds, agree to everything the installer wants). After cloning the repository, make it executable with the command ```chmod +x virtaxupdater; conda activate vtu``` and finally run the four essential subcommands:  
 ```bash
./virtaxupdater connect -i myfolder
./virtaxupdater index -i myfolder
./virtaxupdater download -i myfolder
./virtaxupdater extract -i myfolder
 ```
That's it, you should find a large tab-delimited, gzipp'd table at myfolder/exemplars.tsv.gz in less than 2 hours.  Head over to [Querying the data](#querying-the-data) for a quick and easy run-through.  

### Subcommands  
Every subcommand requires the ```-i INPUT``` command line argument, which is the name of the working directory where you will store the Data. As you can see from the previous example, the first command we run is ```./virtaxupdater connect -i myfolder``` and it is recommended that ```myfolder``` does not exist. The subcommands are:  
<br>
```connect```  
```
usage: connect [-h] [-u URL] -i INPUT  
```
Establish connection with the ICTV Virus Metadata Resource (VMR), and download the current VMR spreadsheet. In 2023, this is a two-sheet table with the first sheet being
informative of virus exemplars (it contains 26 columns). If the ICTV moves the spreadsheet elsewhere and the script fails (let us know) you have two options: either
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
Use Entrez Direct https://www.ncbi.nlm.nih.gov/books/NBK179288/ to download genbank files by accession. Entrez allows to download batches of up to 100 accession at a
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
 (1) Virtaxupdater uses [pandas](https://pypi.org/project/pandas/) + [openpyxl](https://pypi.org/project/openpyxl/) for I/O on large data frames and/or Excel spreadsheets. While the former is likely already installed on your computer, the latter isn't unless you specifically installed it.  
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
 This section provides (work in progress)
 <br>  
 [Back to Index](#index)  
 <br>  
 
 ## Troubleshooting  
 <br>  
 [Back to Index](#index)  
 <br>  
 
 ## Future developments  
 <br>  
 [Back to Index](#index)  
 <br>  



 
