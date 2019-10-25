# CFPQ_Data

Graphs and grammars for experiments in context free path querying algorithms.

## Prerequirements
* GCC
* Python 3

## How to start

Just run init.py: 

```python3 init.py```

The script downloads data and [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) - a suite of synthetic graph generators.

## Repository structure

Graphs and grammars can be found in  ```data/graphs``` - all graphs are divided into groups, which are placed in different directories. Each ```data/graphs/GroupName``` contains ```Matrices``` with graph descriptions and ```Grammars``` - descriptions of queries. 

## Data set

Set contains both real-world data and synthetic graphs for several specific cases; all graphs are represented in triples.

#### RDFs

Real-world RDF files.
- Small
  - [skos](http://www.w3.org/2004/02/skos/core.html) - knowledge organization system based on RDF
- Big
  - [go](http://purl.obolibrary.org/obo/go.owl) - an ontology for describing the function of genes and gene products 
  - [geospecies](http://lod.geospecies.org/geospecies.rdf.gz) - graph related to taxonomic hierarchy and geographical information of animal species

#### Worst cases

Graphs with two cylces; the query is a grammar for the language of correct bracket sequences.

#### Sparse graphs 

Graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) to emulate sparse data.

## Reference values


## Works using this data set

- [Evaluation of the Context-Free Path Querying Algorithm Based on Matrix Multiplication](https://dl.acm.org/citation.cfm?id=3328503)