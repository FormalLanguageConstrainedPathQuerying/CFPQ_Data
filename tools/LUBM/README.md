# LUBM dataset

## Folder structure
- config.txt - configures mappings from IRI names to short string names (for our purposes)
- download.sh - downloads and unzips the lubm generator from oficial website
- generate.sh - generates dataset for 10 universities (this could be changed in the script: set -univ N)
- prepare.py - prepares files names of the generated dataset (optional)
- converter.py - convert set of database files to single file with mappings applied

## Usage

Download lubm java based generating tool. Run dataset generating for  10 universities, and then 
generated database file with mapping for merged 3 universities (indicies 0..2) as an example.

```
$ bash download.sh
$ bash generate.sh
$ python3 converter.py univ\\University 3 config.txt
```
