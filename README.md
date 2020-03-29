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

Set contains both real-world data and synthetic graphs for several specific cases; all graphs are represented in RDF format to unify loading process.

### Graphs

```data/Matrices/RDF``` — Fixed versions of real-world RDF files(links are provided for updating purposes only!):

   - Smaller graphs:
    - a set of popular semantic web ontologies, download links: [skos](https://www.w3.org/2009/08/skos-reference/skos.rdf), [foaf](http://xmlns.com/foaf/0.1/), [wine](https://www.w3.org/TR/owl-guide/wine.rdf), [pizza](https://protege.stanford.edu/ontologies/pizza/pizza.owl), [generations](http://www.owl-ontologies.com/generations.owl), [travel](https://protege.stanford.edu/ontologies/travel.owl), [univ-bench](http://swat.cse.lehigh.edu/onto/univ-bench.owl), [people-pets](http://owl.man.ac.uk/tutorial/people+pets.rdf)
  
  - Bigger graphs:
    - _geospecies_ – graph related to taxonomic hierarchy and geographical information of animal species, download here: <https://old.datahub.io/dataset/geospecies> 
    - a set of graphs from the _Uniprot_ protein sequences database, download here: <ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf>

```data/Synthetic/Matrices/WorstCase``` — graphs with two cylces; the query is a grammar for the language of correct bracket sequences.

```data/Synthetic/Matrices/SparseGraph``` — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) to emulate sparse data.

```data/Synthetic/Matrices/ScaleFree``` — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) by using the Barab\'asi-Albert model of scale-free networks

```data/Synthetic/Matrices/FullGraph``` — a cycle, all edges are labeled with the same token 

### Grammars

```GPPerf1```, ```GPPerf2``` — queries over _subClassOf_ and _type_ relations 
  - Use with _RDF_ dataset

```geo```
  - Use with _geospecies_ dataset

```an_bm_cm_dn``` — query for _A<sub>n</sub>B<sub>m</sub>C<sub>m</sub>D<sub>n</sub>_ language
  - Use with _ScaleFree_ graphs

```Brackets``` — query describing correct bracket sequences
  - Use with _WorstCase_ graphs

```A_star``` — kleene star query producing full graph
  - Use with _FullGraph_

### Reference values

Control values for algorithms correctness checking can be found in ```control_values.csv```.

## Papers using this data set

- [Evaluation of the Context-Free Path Querying Algorithm Based on Matrix Multiplication](https://dl.acm.org/citation.cfm?id=3328503)
