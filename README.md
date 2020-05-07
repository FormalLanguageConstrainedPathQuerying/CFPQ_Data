# CFPQ_Data

Graphs and grammars for experimental analysis of context free path querying algorithms.

## Prerequirements
* GCC
* Python 3

## How to start

Just install requirements and run ```init.py```: 

```
pip3 install -r requirements.txt
python3 init.py
```

This script downloads data (real-world RDF files) and [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) — a suite of synthetic graph generators. After that it generates some synthatic graphs.

In order to download/update one specific part of the dataset run:
```
python3 init.py --update [GroupName]
```
Options for ```[GroupName]``` are ```rdf, scalefree, full, worstcase, sparse```


## Integration with graph DBs

We provide a set of scripts to simplify data loading into some popular graph databases.

### RedisGraph

The dataset can be loaded to RedisGraph with ```tools/redis-rdf```, for example:
```
cd ./tools/redis-rdf
python3 main.py --port [PORT] dir ../../data/Matrices/ScaleFree/
python3 main.py --port [PORT] file ../../data/Matrices/RDF/foaf.rdf foaf
```

### Neo4j

To load RDF data into Neo4j database one can use [Neosemantix plugin for Neo4j](https://neo4j.com/labs/nsmtx-rdf/).

## Dataset

Set contains both real-world data and synthetic graphs for several specific cases. All graphs are represented in RDF format to unify loading process.

### Query format

Queries are represented as context-free grammars which are represented in the following format:

- Line 0: a set of variable symbols delimited by spaces, the first one is the starting symbol
- Line 1: a set of terminal symbols delimited by spaces
- The rest of the lines are productions in the form:

     ```head -> body | body | ... | body```

    where each body can contain basic regular expression, allowed operators:
    
    - The concatenation, the default operator, which can by represented either by a space or a dot (```.```)
    - The union, represented by ```|```
    - The ```?``` quantifier
    - The kleene star, represented by ```*```
    
    Epsilon symbol should be represented by ```eps```

Example!!!

Grammar can be converted to CNF with ```tools/gramar_to_cnf```.


pyformlang!!!!

### Dataset structure

Graphs and grammars can be found in  ```data``` — all graphs are divided into groups, which are placed in different directories. Each ```data/Matrices/GroupName/``` contains graph descriptions and ```data/Grammars``` — descriptions of queries. 


**```data/RDF```** — fixed versions of real-world RDF files (links are provided for updating purposes only!):
- Smaller graphs:
    - a set of popular semantic web ontologies. This set is introduced by Xiaowang Zhang in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743) :
       - [skos](https://www.w3.org/2009/08/skos-reference/skos.rdf)
       - [foaf](http://xmlns.com/foaf/0.1/)
       - [wine](https://www.w3.org/TR/owl-guide/wine.rdf)
       - [pizza](https://protege.stanford.edu/ontologies/pizza/pizza.owl)
       - [generations](http://www.owl-ontologies.com/generations.owl)
       - [travel](https://protege.stanford.edu/ontologies/travel.owl)
       - [univ-bench](http://swat.cse.lehigh.edu/onto/univ-bench.owl)
       - [people-pets](http://owl.man.ac.uk/tutorial/people+pets.rdf)
  
- Bigger graphs:
   - **geospecies** – graph related to taxonomic hierarchy and geographical information of animal species, download here: <https://old.datahub.io/dataset/geospecies>. Introduced in ["An Experimental Study ofContext-Free Path Query Evaluation Methods"](https://dl.acm.org/doi/pdf/10.1145/3335783.3335791)
   - a set of graphs from the **Uniprot** protein sequences database, download here: <ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/rdf>
       - **go**
       - **go-hierarchy**
       - **pathways**
       - **taxonomy**
       - **taxonomy-hierarchy**
       - **core**
       - **enzime**
   - **eclass_514en** 

Grammars list contains the following variants of same-generation query over different relation tipes.
-  **g1** — same-geneartion query over _type_ and _subclass-of_ relations. Introduced in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743)
-  **g2** — same-geneartion query over _type_ and _subclass-of_ relations. Introduced in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743)
-  **geo** — same-generation query over _broader-transitive_ relation.
  

**```data/MemoryAliases```** — real-world data for points-to analysis of C code.
  - First part is a dataset form [Graspan tool](https://github.com/Graspan/graspan-cpp). The original data is placed [here](https://drive.google.com/drive/folders/0B8bQanV_QfNkbDJsOWc2WWk4SkE?usp=sharing). This part is placed in ```Graspan``` folder.
  - Second part is a part of dataset form ["Demand-driven alias analysis for C"](https://dl.acm.org/doi/10.1145/1328897.1328464). This part is placed in ```small``` folder.

  Both grammars ```g1``` and ```g2``` specify the same language which is described in related papers. These two grammars were written in a different way in order to investigate dependencies on query specification format.

- ```data/Synthetic/Matrices/WorstCase``` — graphs with two cylces; the query is a grammar for the language of correct bracket sequences.

- ```data/Synthetic/Matrices/SparseGraph``` — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) to emulate sparse data.

- ```data/Synthetic/Matrices/ScaleFree``` — graphs generated with [GTgraph](http://www.cse.psu.edu/~kxm85/software/GTgraph/) by using the Barab\'asi-Albert model of scale-free networks

- ```data/Synthetic/Matrices/FullGraph``` — a cycle, all edges are labeled with the same token 



```an_bm_cm_dn``` — query for _A<sub>n</sub>B<sub>m</sub>C<sub>m</sub>D<sub>n</sub>_ language
  - Use with **ScaleFree** graphs

```Brackets``` — query describing correct bracket sequences
  - Use with **WorstCase** graphs

```A_star``` — kleene star query producing full graph
  - Use with **FullGraph**

### Reference values

Reference values for algorithms correctnes checking, which can be found in [reference_values.csv](./reference_values.csv), are in the following format: ```graph, grammar, control_sum```, where ```control_sum``` is the number of paths generated by non-terminals of the grammars.

example !!!

## Papers on CFPQ

List of CFPQ-related works. The list is not full, work in progress.

### Graph databases
- M. Yannakakis. "Graph-theoretic methods in database theory".
- P. Sevon and L. Eronen. "Subgraph queries by context-free grammars".
- J. Kuijpers, G. Fletcher, N. Yakovets, and T. Lindaaker. "An experimental study of context-free path query evaluation methods".
- H. Miao and A. Deshpande. "Understanding Data Science Lifecycle Provenance via Graph Segmentation and Summarization". 
- TBD

### Static code analysis
- T. Reps. "Program analysis via graph reachability".
- X. Zheng and R. Rugina. "Demand-driven alias analysis for C".
- TBD

## Papers using this dataset

- [Evaluation of the Context-Free Path Querying Algorithm Based on Matrix Multiplication](https://dl.acm.org/citation.cfm?id=3328503)
