# virtaxupdater
### Download viral genomes by connecting to the latest ICTV Virus Metadata Resource (VMR)  

Hello, and welcome.  
As stated in https://ictv.global/vmr, the ICTV *chooses an exemplar virus for each species and the VMR provides a list of these exemplars (...) and includes the GenBank accession number for the genomic sequence of the isolate as well as the virus name, isolate designation, suggested abbreviation, genome composition, and host source*.  
<br>
The code in this repository automatically fetches the VMR information and downloads the GenBank files associated to each exemplar virus.  
<br>  

### Requirements  
```virtaxupdater``` was developed on Linux kernel and it is written in python. In addition to [pandas](https://pypi.org/project/pandas/), it simply requires one additional library for Excel spreadsheet manipulation and the Entrez Direct E-utilities software package for programmatic access to the NCBI's suite of interconnected databases:  

* [openpyxl](https://pypi.org/project/openpyxl/)
* [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
<br>

### How it works  
Three modules allow you to connect to VMR, download all exemplar virus GenBank files and update a local repository. Specifically, use:

```virtaxupdater connect```  To get the current VMR spreadsheet from the [ICTV](https://ictv.global/vmr) and save it to a new working directory.   
```virtaxupdater download```  To process the exemplar virus list and download all GenBank files associated to each 'Sort' (this takes approx 12hrs).  
```virtaxupdater update```  To update and polish the GenBank subdirectories + a TSV spreadsheet obtained using the previous two subcommands.  
<br>  

### Future developments  
Currently looking into extracting the most relevant features from the exemplar viruses, such as virus host, genome composition and possibility to compare taxa within this dataset.  

