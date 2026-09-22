.. _reachable_pairs:

***********************
Reachable Pair Counts
***********************

.. only:: html

   :Release: |release|
   :Date: |today|

Reference counts of reachable vertex pairs for every graph x grammar pair
in the dataset. A pair :math:`(u, v)` is reachable if there exists a path
from :math:`u` to :math:`v` labeled by a string in the language of the
grammar's start symbol. The sections below follow the graph categories of
the :ref:`Graphs <graphs>` catalog.

.. note::

   Values marked "not available" have not been computed yet. The count is
   a property of the graph and grammar only; it does not depend on the
   algorithm or environment used to compute it.

Download
--------

The full table is available as a CSV file:

- **Package API**: ``from cfpq_data.dataset import reachable_pairs, REACHABLE_PAIRS_CSV``
- **CSV file**: `reachable_pairs.csv <https://raw.githubusercontent.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data/dev/cfpq_data/dataset/reachable_pairs.csv>`_

Columns: ``graph``, ``grammar``, ``category``, ``query_class`` (one of
``cfpq``, ``rpq``, ``mcfpq`` — the names of the ``queries/<class>/``
directories in the graph archives), ``num_reachable_pairs`` (empty when not
yet available).

.. reachable-pairs-tables:begin

C alias analysis
----------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - apache
     - c_alias.cnf
     - 92806768
   * - arch
     - c_alias.cnf
     - 5339563
   * - block
     - c_alias.cnf
     - 5351409
   * - bzip
     - c_alias.cnf
     - 315
   * - crypto
     - c_alias.cnf
     - 5428237
   * - drivers
     - c_alias.cnf
     - 18825025
   * - fs
     - c_alias.cnf
     - 9646475
   * - gzip
     - c_alias.cnf
     - 1458
   * - init
     - c_alias.cnf
     - 3783769
   * - ipc
     - c_alias.cnf
     - 5249389
   * - kernel
     - c_alias.cnf
     - 16747731
   * - lib
     - c_alias.cnf
     - 5276303
   * - ls
     - c_alias.cnf
     - 854
   * - mm
     - c_alias.cnf
     - 3990305
   * - net
     - c_alias.cnf
     - 8833403
   * - postgre
     - c_alias.cnf
     - 90661446
   * - pr
     - c_alias.cnf
     - 385
   * - security
     - c_alias.cnf
     - 5593387
   * - sound
     - c_alias.cnf
     - 6085269
   * - wc
     - c_alias.cnf
     - 156

RDF
---

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - atom
     - nested_parentheses_subClassOf.cnf
     - 2
   * - atom
     - nested_parentheses_subClassOf_type.cnf
     - 6
   * - atom
     - nested_parentheses_type.cnf
     - 4
   * - biomedical
     - nested_parentheses_subClassOf.cnf
     - 43
   * - biomedical
     - nested_parentheses_subClassOf_type.cnf
     - 47
   * - biomedical
     - nested_parentheses_type.cnf
     - 4
   * - core
     - nested_parentheses_subClassOf.cnf
     - 143
   * - core
     - nested_parentheses_subClassOf_type.cnf
     - 204
   * - core
     - nested_parentheses_type.cnf
     - 61
   * - eclass
     - nested_parentheses_subClassOf.cnf
     - 90988
   * - eclass
     - nested_parentheses_subClassOf_type.cnf
     - 90994
   * - eclass
     - nested_parentheses_type.cnf
     - 6
   * - enzyme
     - nested_parentheses_broaderTransitive.cnf
     - 14267542
   * - enzyme
     - nested_parentheses_subClassOf.cnf
     - 394
   * - enzyme
     - nested_parentheses_subClassOf_type.cnf
     - 396
   * - enzyme
     - nested_parentheses_type.cnf
     - 3
   * - foaf
     - nested_parentheses_subClassOf.cnf
     - 7
   * - foaf
     - nested_parentheses_subClassOf_type.cnf
     - 36
   * - foaf
     - nested_parentheses_type.cnf
     - 29
   * - funding
     - nested_parentheses_subClassOf.cnf
     - 27
   * - funding
     - nested_parentheses_subClassOf_type.cnf
     - 58
   * - funding
     - nested_parentheses_type.cnf
     - 31
   * - generations
     - nested_parentheses_subClassOf.cnf
     - 0
   * - generations
     - nested_parentheses_subClassOf_type.cnf
     - 12
   * - generations
     - nested_parentheses_type.cnf
     - 12
   * - geospecies
     - nested_parentheses_broaderTransitive.cnf
     - 226669749
   * - geospecies
     - nested_parentheses_subClassOf.cnf
     - 0
   * - geospecies
     - nested_parentheses_subClassOf_type.cnf
     - 85
   * - geospecies
     - nested_parentheses_type.cnf
     - 85
   * - go
     - nested_parentheses_subClassOf.cnf
     - 640305
   * - go
     - nested_parentheses_subClassOf_type.cnf
     - 640316
   * - go
     - nested_parentheses_type.cnf
     - 9
   * - go_hierarchy
     - nested_parentheses_subClassOf.cnf
     - 588976
   * - go_hierarchy
     - nested_parentheses_subClassOf_type.cnf
     - 588976
   * - go_hierarchy
     - nested_parentheses_type.cnf
     - 0
   * - pathways
     - nested_parentheses_subClassOf.cnf
     - 883
   * - pathways
     - nested_parentheses_subClassOf_type.cnf
     - 884
   * - pathways
     - nested_parentheses_type.cnf
     - 2
   * - people
     - nested_parentheses_subClassOf.cnf
     - 24
   * - people
     - nested_parentheses_subClassOf_type.cnf
     - 51
   * - people
     - nested_parentheses_type.cnf
     - 29
   * - pizza
     - nested_parentheses_subClassOf.cnf
     - 1334
   * - pizza
     - nested_parentheses_subClassOf_type.cnf
     - 1356
   * - pizza
     - nested_parentheses_type.cnf
     - 20
   * - skos
     - nested_parentheses_subClassOf.cnf
     - 1
   * - skos
     - nested_parentheses_subClassOf_type.cnf
     - 30
   * - skos
     - nested_parentheses_type.cnf
     - 29
   * - taxonomy
     - nested_parentheses_subClassOf.cnf
     - 151703
   * - taxonomy
     - nested_parentheses_subClassOf_type.cnf
     - 151706
   * - taxonomy
     - nested_parentheses_type.cnf
     - 4
   * - taxonomy_hierarchy
     - nested_parentheses_subClassOf.cnf
     - 5351657
   * - taxonomy_hierarchy
     - nested_parentheses_subClassOf_type.cnf
     - 5351657
   * - taxonomy_hierarchy
     - nested_parentheses_type.cnf
     - 0
   * - travel
     - nested_parentheses_subClassOf.cnf
     - 33
   * - travel
     - nested_parentheses_subClassOf_type.cnf
     - 52
   * - travel
     - nested_parentheses_type.cnf
     - 19
   * - univ
     - nested_parentheses_subClassOf.cnf
     - 17
   * - univ
     - nested_parentheses_subClassOf_type.cnf
     - 25
   * - univ
     - nested_parentheses_type.cnf
     - 6
   * - wine
     - nested_parentheses_subClassOf.cnf
     - 499
   * - wine
     - nested_parentheses_subClassOf_type.cnf
     - 565
   * - wine
     - nested_parentheses_type.cnf
     - 65

Java points-to graphs
---------------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - avrora
     - java_points_to.cnf
     - 192790
   * - batik
     - java_points_to.cnf
     - 868368
   * - commons_io
     - java_points_to.cnf
     - 24020
   * - commons_lang3
     - java_points_to.cnf
     - 27553
   * - eclipse
     - java_points_to.cnf
     - 378989
   * - fop
     - java_points_to.cnf
     - 1984072
   * - gson
     - java_points_to.cnf
     - 56325
   * - guava
     - java_points_to.cnf
     - 26384496
   * - h2
     - java_points_to.cnf
     - 2611022
   * - jackson
     - java_points_to.cnf
     - 3108775
   * - junit5
     - java_points_to.cnf
     - 129598
   * - jython
     - java_points_to.cnf
     - 561720
   * - luindex
     - java_points_to.cnf
     - 176051
   * - lusearch
     - java_points_to.cnf
     - 43719
   * - mockito
     - java_points_to.cnf
     - 16169
   * - pmd
     - java_points_to.cnf
     - 137120
   * - sunflow
     - java_points_to.cnf
     - 35209
   * - tomcat
     - java_points_to.cnf
     - 3792543
   * - tradebeans
     - java_points_to.cnf
     - 34370090
   * - tradesoap
     - java_points_to.cnf
     - 34451130
   * - xalan
     - java_points_to.cnf
     - 1138776

Field-Sensitive Alias
---------------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - cactus_field_sensitive_alias
     - aa.cnf
     - 37625324
   * - imagick_field_sensitive_alias
     - aa.cnf
     - 369956094
   * - leela_field_sensitive_alias
     - aa.cnf
     - 3968276
   * - nab_field_sensitive_alias
     - aa.cnf
     - 262566
   * - omnetpp_field_sensitive_alias
     - aa.cnf
     - 158255766
   * - parest_field_sensitive_alias
     - aa.cnf
     - 49415038
   * - perlbench_field_sensitive_alias
     - aa.cnf
     - 851737865
   * - povray_field_sensitive_alias
     - aa.cnf
     - 27219043
   * - x264_field_sensitive_alias
     - aa.cnf
     - 5246565
   * - xz_field_sensitive_alias
     - aa.cnf
     - 205164

Context-Sensitive Data-Flow
---------------------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - cactus
     - vf.cnf
     - 47806209
   * - imagick
     - vf.cnf
     - 12687034
   * - leela
     - vf.cnf
     - 662466
   * - nab
     - vf.cnf
     - 739646
   * - omnetpp
     - vf.cnf
     - 8424500
   * - parest
     - vf.cnf
     - 1342540
   * - perlbench
     - vf.cnf
     - 297504186
   * - povray
     - vf.cnf
     - 34599413
   * - x264
     - vf.cnf
     - 20259480
   * - xz
     - vf.cnf
     - 358834

Data Provenance
---------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - airflow
     - prov_derivation.cnf
     - 91350
   * - celery
     - prov_derivation.cnf
     - 25306
   * - click
     - prov_derivation.cnf
     - 2710
   * - django
     - prov_derivation.cnf
     - 615946
   * - fastapi
     - prov_derivation.cnf
     - 8814
   * - flask
     - prov_derivation.cnf
     - 8062
   * - httpx
     - prov_derivation.cnf
     - 4408
   * - itsdangerous
     - prov_derivation.cnf
     - 2912
   * - jinja
     - prov_derivation.cnf
     - 7436
   * - pandas
     - prov_derivation.cnf
     - 154646
   * - pluggy
     - prov_derivation.cnf
     - 880
   * - requests
     - prov_derivation.cnf
     - 2524
   * - sampleproject
     - prov_derivation.cnf
     - 342
   * - scikit-learn
     - prov_derivation.cnf
     - 217728
   * - sphinx
     - prov_derivation.cnf
     - 304084
   * - superset
     - prov_derivation.cnf
     - 97460
   * - wikipedia-provenance
     - prov_derivation.cnf
     - 1732
   * - zulip
     - prov_derivation.cnf
     - 209908

Name Resolution
---------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - jiaozi
     - name_resolution.cnf
     - 14435
   * - jsonpath
     - name_resolution.cnf
     - 59764
   * - libgdx
     - name_resolution.cnf
     - not available
   * - shattered_pixel_dungeon
     - name_resolution.cnf
     - 971998

Biological graphs from UniProt
------------------------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - unigraph_1
     - unigraph_1.cnf
     - 376578
   * - unigraph_10
     - unigraph_10.cnf
     - not available
   * - unigraph_2
     - unigraph_2.cnf
     - 39888347
   * - unigraph_3
     - unigraph_3.cnf
     - 52471840
   * - unigraph_4
     - unigraph_4.cnf
     - 808091802
   * - unigraph_5
     - unigraph_5.cnf
     - 2303590109
   * - unigraph_6
     - unigraph_6.cnf
     - 1722963921
   * - unigraph_7
     - unigraph_7.cnf
     - 2320964134
   * - unigraph_8
     - unigraph_8.cnf
     - not available
   * - unigraph_9
     - unigraph_9.cnf
     - not available

.. reachable-pairs-tables:end
