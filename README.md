# CFPQ_Data

Graphs and grammars for experimental analysis of context free path querying algorithms.

## Prerequirements
* GCC
* Python 3

## How to start

Just install requirements and run init.py: 

```
pip3 install -r requirements.txt
python3 init.py
```

In order to load/update one specific part of the dataset run:
```
python3 init.py --update [GroupName]
```
Options for ```[GroupName]``` are ```rdf, scalefree, full, worstcase, sparse```

The script downloads data (real-world RDF files) and [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) — a suite of synthetic graph generators.

## Repository structure

Graphs and grammars can be found in  ```data``` — all graphs are divided into groups, which are placed in different directories. Each ```data/Matrices/GroupName/``` contains graph descriptions and ```data/Grammars``` — descriptions of queries. 

## Integration with graph DBs

We provide a set of scripts to simplify data loading into soe popular graph databases.

### RedisGraph

Data set can be loaded to RedisGraph with ```tools/redis-rdf```, for example:
```
cd ./tools/redis-rdf
python3 main.py --port [PORT] dir ../../data/Matrices/ScaleFree/
python3 main.py --port [PORT] file ../../data/Matrices/RDF/foaf.rdf foaf
```

### Neo4j

Work in progress.

## Data set

Set contains both real-world data and synthetic graphs for several specific cases; all graphs are represented in triples.
All graphs are represented in RDF format to unify loading process.

### Graphs
- **RDF** — Real-world RDF files:

  - Smaller graphs
    - a set of popular semantic web ontologies like **foaf**, **wine**, **pizza**.
  - Bigger graphs
    - **geospecies** – graph related to taxonomic hierarchy and geographical information of animal species
    - a set of graphs from the **Uniprot** protein sequences database

- **Worst cases** — graphs with two cylces; the query is a grammar for the language of correct bracket sequences.

- **Sparse** — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) to emulate sparse data.

- **Scale-free** — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) by using the Barab\'asi-Albert model of scale-free networks

- **Full graph**

### Grammars

- **GPPerf1, GPPerf2** — queries over _subClassOf_ and _type_ relations 
  - Use with **RDF** graphs

- **geo**
  - Use with **geospecies** dataset

- **an_bm_cm_dn**
  - Use with **ScaleFree** graphs

- **Brackets** — query describing correct bracket sequences
  - Use with **WorstCase** graphs

- **A_star** — kleene star producing full graph
  - Use with **FullGraph**

### Reference values

Control values(e.g. number of paths) for algorithms checking: Work in progress

## Papers using this data set

- [Evaluation of the Context-Free Path Querying Algorithm Based on Matrix Multiplication](https://dl.acm.org/citation.cfm?id=3328503)
