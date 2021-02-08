# CFPQ_Data

Graphs and grammars for experimental analysis of context-free path querying algorithms.

## Prerequirements
* GCC
* Python 3

## How to start

* Install requirements ```pip3 install -r requirements.txt```

* Choose part of the dataset

| Graphs | Command |
|:------:|:-------:|
| RDF | python3 cfpq_data.py RDF --all |
| MemoryAliases | python3 cfpq_data.py MemoryAliases --all |
| ScaleFree | python3 cfpq_data.py ScaleFree --preset |
| FullGraph| python3 cfpq_data.py FullGraph --preset |
| WorstCase | python3 cfpq_data.py WorstCase --preset |
| SparseGraph | python3 cfpq_data.py SparseGraph --preset |
| LUBM | python3 cfpq_data.py LUBM |

* Or one of tools

| Tool description | Command |
|:----------------:|:-------:|
| Convert specific graph or part of dataset to TXT file | python3 graph2txt -h |
| Convert grammar to cnf format | python3 grammar2cnf -h |
| Generate RPQ queries | python3 gen_RPQ -h |
| Load RDF graph to RedisGraph | python3 redis_rdf -h |

## Integration with graph DBs

We provide a set of scripts to simplify data loading into some popular graph databases.

### RedisGraph

The dataset can be loaded to RedisGraph with ```src/tools/redis_rdf```, for example:
```
python3 main.py redis_rdf --host [HOST] --port [PORT] dir ../../data/Matrices/ScaleFree/
python3 main.py redis_rdf --host [HOST] --port [PORT] file ../../data/Matrices/RDF/foaf.rdf foaf
```

### Neo4j

To load RDF data into Neo4j database one can use [Neosemantix plugin for Neo4j](https://neo4j.com/labs/nsmtx-rdf/).

## Dataset

Set contains both real-world data and synthetic graphs for several specific cases. All graphs are represented in RDF format to unify loading process.

### Query format

Queries are represented as context-free grammars in the following format:

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

Example query in such format:
```
S
a b
S -> a S b S
S -> eps
```

Grammar can be converted to CNF with ```src/tools/grammar2cnf```, which uses [pyformlang](https://pypi.org/project/pyformlang/) library to perform context-free grammar modifications.
```
$ python3 main.py grammar2cnf file [PATH_TO_GRAMMAR] --output [PATH_TO_OUTPUT]
```

### Dataset structure

Graphs and grammars can be found in  ```data``` — all graphs are divided into groups, which are placed in different directories. Each ```data/[GroupName]/Matrices``` contains graph descriptions and ```data/[GroupName]/Grammars``` — descriptions of queries. 

**```RDF```** — fixed versions of real-world RDF files (links are provided for updating purposes only!):
- Small graphs is a set of popular semantic web ontologies. This set is introduced by Xiaowang Zhang in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743) :
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
-  **g1** — same-generation query over _type_ and _subclass-of_ relations. Introduced in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743)
-  **g2** — same-generation query over _type_ and _subclass-of_ relations. Introduced in ["Context-Free Path Queries on RDF Graphs"](https://arxiv.org/abs/1506.00743)
-  **geo** — same-generation query over _broader-transitive_ relation.
  

**```MemoryAliases```** — real-world data for points-to analysis of C code.
  - First part is a dataset form [Graspan tool](https://github.com/Graspan/graspan-cpp). The original data is placed [here](https://drive.google.com/drive/folders/0B8bQanV_QfNkbDJsOWc2WWk4SkE?usp=sharing). This part is placed in ```Graspan``` folder.
  - Second part is a part of dataset form ["Demand-driven alias analysis for C"](https://dl.acm.org/doi/10.1145/1328897.1328464). This part is placed in ```small``` folder.

  Both grammars **g1** and **g2** specify the same language which is described in related papers. These two grammars were written in a different way in order to investigate dependencies on query specification format.

**```WorstCase```** — graphs with two cylces; the query **Brackets** is a grammar for the language of correct bracket sequences.

**```SparseGraph```** — graphs generated with [NetworkX](https://networkx.github.io/) to emulate sparse data. The grammar provided is a variant of the same-generation query.

**```ScaleFree```** — graphs generated by using the Barab\'asi-Albert model of scale-free networks. Use with grammar **an_bm_cm_dn**, which is a query for _A<sub>n</sub>B<sub>m</sub>C<sub>m</sub>D<sub>n</sub>_ language.

**```FullGraph```** — cycle graphs, all edges are labeled with the same token. Use with **A_star** queries, which produce full graph on that dataset.

### RDF
| Name | Vertices | Edges | Size of file (Bytes) |
|:---:|:---:|:---:|:---:|
| atom-primitive.owl | 291 | 425 | 48884 |
| biomedical-mesure-primitive.owl | 341 | 459 | 53057 |
| core.owl | 1323 | 2752 | 270846 |
| eclass_514en.owl | 239111 | 360248 | 40191953 |
| enzyme.rdf | 48815 | 86543 | 8806602 |
| foaf.rdf | 256 | 631 | 44209 |
| funding.rdf | 778 | 1086 | 131564 |
| generations.owl | 129 | 273 | 13826 |
| geospecies.rdf | 450609 | 2201532 | 187133434 |
| go-hierarchy.owl | 45007 | 490109 | 38888638 |
| go.owl | 582929 | 1437437 | 164749424 |
| pathways.rdf | 6238 | 12363 | 1305842 |
| people_pets.rdf | 337 | 640 | 40375 |
| pizza.owl | 671 | 1980 | 126939 |
| skos.rdf | 144 | 252 | 28966 |
| travel.owl | 131 | 277 | 17169 |
| univ-bench.owl | 179 | 293 | 14433 |
| wine.rdf | 733 | 1839 | 78225 |
### MemoryAliases
| Name | Vertices | Edges | Size of file (Bytes) |
|:---:|:---:|:---:|:---:|
| Apache_httpd_2.2.18_pointsto_graph.xml | 1721418 | 1510411 | 138037427 |
| arch_afterInline.txt.xml | 3448422 | 2970242 | 278669103 |
| block_afterInline.txt.xml | 3423234 | 2951393 | 276869199 |
| bzip2.txt.xml | 632 | 556 | 45432 |
| crypto_afterInline.txt.xml | 3464970 | 2988387 | 280248585 |
| drivers_afterInline.txt.xml | 4273803 | 3707769 | 346720743 |
| fs_afterInline.txt.xml | 4177416 | 3609373 | 337856145 |
| gzip.txt.xml | 2687 | 2293 | 199239 |
| init_afterInline.txt.xml | 2446224 | 2112809 | 197676888 |
| ipc_afterInline.txt.xml | 3401022 | 2931498 | 275033440 |
| kernel_afterInline.txt.xml | 11254434 | 9484213 | 886162222 |
| lib_afterInline.txt.xml | 3401355 | 2931880 | 275060825 |
| ls.txt.xml | 1687 | 1453 | 126329 |
| mm_afterInline.txt.xml | 2538243 | 2191079 | 205010253 |
| net_afterInline.txt.xml | 4039470 | 3500141 | 327815218 |
| PostgreSQL_8.3.9_pointsto_graph.xml | 5203419 | 4678543 | 429924717 |
| pr.txt.xml | 815 | 692 | 59629 |
| security_afterInline.txt.xml | 3479982 | 3003326 | 281698638 |
| sound_afterInline.txt.xml | 3528861 | 3049732 | 285856817 |
| wc.txt.xml | 332 | 269 | 23679 |
### Reference values

Reference values for algorithms correctnes checking, which can be found in [reference_values.csv](./reference_values.csv), are in the following format: ```graph, grammar, control_sum```, where ```control_sum``` is the number of paths generated by non-terminals of the grammars.

Example of the ```FullGraph``` dataset reference values in such format:
```
fullgraph_10,A_star0,"{'s': 100}"
fullgraph_100,A_star0,"{'s': 10000}"
...
```

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
