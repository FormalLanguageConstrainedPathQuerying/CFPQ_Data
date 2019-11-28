# CFPQ_Data

Graphs and grammars for experiments in context free path querying algorithms.

## Prerequirements
* GCC
* Python 3

## How to start

Just install requirements and run init.py: 

```
pip3 install -r requirements.txt
python3 init.py
```

The script downloads data and [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) - a suite of synthetic graph generators.

## Repository structure

Graphs and grammars can be found in  ```data/graphs``` - all graphs are divided into groups, which are placed in different directories. Each ```data/graphs/GroupName``` contains ```Matrices``` with graph descriptions and ```Grammars``` - descriptions of queries. 

## Data set

Set contains both real-world data and synthetic graphs for several specific cases; all graphs are represented in triples.

### RDFs

Real-world RDF files.
- Small
  - [skos](http://www.w3.org/2004/02/skos/core.html) - knowledge organization system based on RDF
- Big
  - [go](http://purl.obolibrary.org/obo/go.owl) - an ontology for describing the function of genes and gene products 
  - [geospecies](http://lod.geospecies.org/geospecies.rdf.gz) - graph related to taxonomic hierarchy and geographical information of animal species

### Static analysis cases

Points-to graphs generated from [DacapoSuite](https://github.com/dacapobench/dacapobench) java benchmarks used in [Cauliflower:  a Solver Generator Tool forContext-Free Language Reachability](https://easychair.org/publications/open/bnVq)
Clone into ```git@bitbucket.org:jensdietrich/gigascale-pointsto-oopsla2015.git```, pre-generated graphs in basic CSV format can be found at ```datasets/dacapo9```.

### Worst cases

Graphs with two cylces; the query is a grammar for the language of correct bracket sequences.

### Sparse graphs 

Graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) to emulate sparse data.

## Reference values

|Filename                       |g1    |      |      |      |      |      |      |      |geo.cnf|         |                            |
|-------------------------------|------|------|------|------|------|------|------|------|-------|---------|----------------------------|
|                               |s time|s     |s1    |s2    |s3    |s4    |s5    |s6    |s time |s        |s1                          |
|atom-primitive.txt             |0.034 |15454 |122   |122   |138   |138   |15128 |0     |       |         |                            |
|funding.txt                    |0.034 |17634 |90    |90    |304   |304   |6555  |2375  |       |         |                            |
|pizza.txt                      |0.124 |56195 |259   |259   |365   |365   |23044 |720   |       |         |                            |
|biomedical-mesure-primitive.txt|0.044 |15156 |122   |122   |130   |130   |15006 |0     |       |         |                            |
|generations.txt                |0.003 |2164  |0     |0     |78    |78    |0     |259   |       |         |                            |
|skos.txt                       |0.001 |810   |1     |1     |70    |70    |5     |0     |       |         |                            |
|core.txt                       |0.007 |316   |178   |178   |706   |1412  |82    |239   |       |         |                            |
|go-hierarchy.txt               |13.953|588976|490109|490109|0     |0     |324016|0     |       |         |                            |
|taxonomy.txt                   |      |      |      |      |      |      |      |      |       |         |                            |
|eclass_514en.txt               |5.776 |90994 |90962 |90962 |72517 |72517 |35505 |30330 |       |         |                            |
|go.txt                         |5.553 |304070|90512 |90512 |58483 |58483 |278610|39642 |       |         |                            |
|travel.txt                     |0.006 |2499  |30    |30    |90    |90    |1110  |630   |       |         |                            |
|enzyme.txt                     |0.595 |396   |8163  |8163  |14989 |14989 |393   |393   |       |         |                            |
|pathways.txt                   |0.060 |884   |3117  |3117  |3118  |3118  |882   |882   |       |         |                            |
|univ-bench.txt                 |0.005 |2540  |36    |36    |84    |84    |1478  |0     |       |         |                            |
|foaf.txt                       |0.005 |4118  |10    |10    |174   |174   |120   |195   |       |         |                            |
|people_pets.txt                |0.015 |9472  |33    |33    |161   |161   |2486  |1881  |       |         |                            |
|wine.txt                       |0.111 |66572 |126   |126   |485   |485   |8172  |16261 |       |         |                            |
|geospeices.txt                 |2.286 |85    |0     |0     |89062 |89062 |0     |0     |265.654|226669749|21361542                    |

## Works using this data set

- [Evaluation of the Context-Free Path Querying Algorithm Based on Matrix Multiplication](https://dl.acm.org/citation.cfm?id=3328503)
