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
Virtaxupdater automatically collects sequences and metadata associated to each exemplar virus in the latest VMR. It is a simple and powerful python framework with very little requirements that makes over 16,000 records available in less than 2 hours.   
<br>  

## Index  
[How to run](#how-to-run)  
[Installation](#installation)  
[Requirements](#requirements)  
[How it works](#how-it-works)  
[Querying the data](#querying-the-data)  
[Troubleshooting](#troubleshooting)  
[Future developments](#future-developments)  
 <br>
 ## How to run  
 Virtaxupdater is composed of seven subcommands. Having the script broken down into seven modules makes it possible to perform separate tasks without running the entire pipeline every time. The thought process is pretty straightforward: there is a subcommand for each task to bring you from zero to VMR-hero in less than 2 hours.  
 
 ### I don't have time to go through the documentation  
 Fine, you have two options.  
 * Option 1: you don't even need Virtaxupdater. Simply download the Database folder in this repository, open a terminal in the directory containing it (<ins>don't</ins> *cd* into Database/) and ```Ctrl```+```C``` ```Ctrl```+```V``` this one-liner:
 ```bash
 :> exemplars.tsv.gz; while read part; do cat "$part" >> exemplars.tsv.gz; done < <(cat Database/deflate/parts.index)
 ```
That's it! Your data are in this large, 31-column, tab-delimited, gzip-compressed table, **exemplars.tsv.gz**. Head over to [Querying the data](#querying-the-data) for a quick and easy run-through.  

 * Option 2: use Virtaxupdater to download your own, up-to-date version of the VMR. Assuming you have conda or better yet, **mamba** you will first run ```conda create -n vtu -c conda-forge biopython openpyxl pandas -y``` to create a new environment called vtu. It only costs a few minutes of your time and helps avoid library conflicts. Then run ```sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"``` to install [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/) (it takes 30 seconds, agree to everything the installer wants). After cloning the repository, make it executable with the command ```chmod +x virtaxupdater; conda activate vtu``` and finally run the four essential subcommands:  
 ```bash
./virtaxupdater connect -i myfolder
./virtaxupdater index -i myfolder
./virtaxupdater download -i myfolder
./virtaxupdater extract -i myfolder
 ```
That's it, you should find a large tab-delimited, gzipp'd table at myfolder/exemplars.tsv.gz in less than 2 hours.  

### Give me the documentation
 
 [back](#index)  
 <br>  
 ## Installation  
 [back](#index)  
 <br>  
 ## Requirements  
 [back](#index)  
 <br>  
 ## How it works  
 [back](#index)  
 <br>  
 ## Querying the data  
 [back](#index)  
 <br>  
 ## Troubleshooting  
 [back](#index)  
 <br>  
 ## Future developments  
 [back](#index)  
 <br>  



 
