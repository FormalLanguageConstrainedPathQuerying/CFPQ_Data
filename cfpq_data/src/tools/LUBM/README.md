# LUBM dataset

## Folder structure
- config.txt - configures mappings from IRI names to short string names (for our purposes)
- download.sh - downloads and unzips the lubm generator from oficial website
- generate.sh - generates dataset for 10 universities (this could be changed in the script: set -univ N)


## Usage
You can prepare files names of the generated dataset (optional) by running
```
$ python3 main.py LUBM prepare --pref PREFIX --new NEW_PREFIX
```
Utility downloads lubm java based generating tool and run dataset generating for 10 universities by itself, and then you can run
generated database file with mapping for merged 3 universities (indicies 0..2) as an example.

```
$ python3 main.py LUBM convert --pref univ\\University --count 3 --conf config.txt
```
