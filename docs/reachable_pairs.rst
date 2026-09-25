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
     - not available
   * - arch
     - c_alias.cnf
     - not available
   * - block
     - c_alias.cnf
     - not available
   * - bzip
     - c_alias.cnf
     - 315
   * - crypto
     - c_alias.cnf
     - not available
   * - drivers
     - c_alias.cnf
     - not available
   * - fs
     - c_alias.cnf
     - not available
   * - gzip
     - c_alias.cnf
     - 1458
   * - init
     - c_alias.cnf
     - not available
   * - ipc
     - c_alias.cnf
     - not available
   * - kernel
     - c_alias.cnf
     - not available
   * - lib
     - c_alias.cnf
     - not available
   * - ls
     - c_alias.cnf
     - 854
   * - mm
     - c_alias.cnf
     - not available
   * - net
     - c_alias.cnf
     - not available
   * - postgre
     - c_alias.cnf
     - not available
   * - pr
     - c_alias.cnf
     - 385
   * - security
     - c_alias.cnf
     - not available
   * - sound
     - c_alias.cnf
     - not available
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
     - not available
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
     - not available
   * - geospecies
     - nested_parentheses_subClassOf.cnf
     - 0
   * - geospecies
     - nested_parentheses_subClassOf_type.cnf
     - not available
   * - geospecies
     - nested_parentheses_type.cnf
     - not available
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
     - not available
   * - taxonomy
     - nested_parentheses_subClassOf_type.cnf
     - not available
   * - taxonomy
     - nested_parentheses_type.cnf
     - not available
   * - taxonomy_hierarchy
     - nested_parentheses_subClassOf.cnf
     - not available
   * - taxonomy_hierarchy
     - nested_parentheses_subClassOf_type.cnf
     - not available
   * - taxonomy_hierarchy
     - nested_parentheses_type.cnf
     - not available
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
     - 21532
   * - batik
     - java_points_to.cnf
     - not available
   * - commons_io
     - java_points_to.cnf
     - 24020
   * - commons_lang3
     - java_points_to.cnf
     - 27553
   * - eclipse
     - java_points_to.cnf
     - not available
   * - fop
     - java_points_to.cnf
     - not available
   * - gson
     - java_points_to.cnf
     - 56325
   * - guava
     - java_points_to.cnf
     - not available
   * - h2
     - java_points_to.cnf
     - not available
   * - jackson
     - java_points_to.cnf
     - not available
   * - junit5
     - java_points_to.cnf
     - not available
   * - jython
     - java_points_to.cnf
     - not available
   * - luindex
     - java_points_to.cnf
     - 9677
   * - lusearch
     - java_points_to.cnf
     - 9242
   * - mockito
     - java_points_to.cnf
     - 16169
   * - pmd
     - java_points_to.cnf
     - 60518
   * - sunflow
     - java_points_to.cnf
     - 16354
   * - tomcat
     - java_points_to.cnf
     - not available
   * - tradebeans
     - java_points_to.cnf
     - not available
   * - tradesoap
     - java_points_to.cnf
     - not available
   * - xalan
     - java_points_to.cnf
     - not available

Field-Sensitive Alias
---------------------

.. list-table::
   :header-rows: 1
   :align: left

   * - Graph
     - Grammar
     - Reachable pairs
   * - cactus_field_sensitive_alias
     - vf.cnf
     - not available
   * - imagick_field_sensitive_alias
     - vf.cnf
     - not available
   * - leela_field_sensitive_alias
     - vf.cnf
     - 3968276
   * - nab_field_sensitive_alias
     - vf.cnf
     - 262566
   * - omnetpp_field_sensitive_alias
     - vf.cnf
     - not available
   * - parest_field_sensitive_alias
     - vf.cnf
     - not available
   * - perlbench_field_sensitive_alias
     - vf.cnf
     - not available
   * - povray_field_sensitive_alias
     - vf.cnf
     - not available
   * - x264_field_sensitive_alias
     - vf.cnf
     - 5246565
   * - xz_field_sensitive_alias
     - vf.cnf
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
     - aa.cnf
     - not available
   * - imagick
     - aa.cnf
     - 12687034
   * - leela
     - aa.cnf
     - 662466
   * - nab
     - aa.cnf
     - 739646
   * - omnetpp
     - aa.cnf
     - not available
   * - parest
     - aa.cnf
     - 1342540
   * - perlbench
     - aa.cnf
     - not available
   * - povray
     - aa.cnf
     - not available
   * - x264
     - aa.cnf
     - 20259480
   * - xz
     - aa.cnf
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
     - not available
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
     - not available
   * - jsonpath
     - name_resolution.cnf
     - 59764
   * - libgdx
     - name_resolution.cnf
     - not available
   * - shattered_pixel_dungeon
     - name_resolution.cnf
     - not available

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
     - not available
   * - unigraph_3
     - unigraph_3.cnf
     - not available
   * - unigraph_4
     - unigraph_4.cnf
     - not available
   * - unigraph_5
     - unigraph_5.cnf
     - not available
   * - unigraph_6
     - unigraph_6.cnf
     - not available
   * - unigraph_7
     - unigraph_7.cnf
     - not available
   * - unigraph_8
     - unigraph_8.cnf
     - not available
   * - unigraph_9
     - unigraph_9.cnf
     - not available

.. reachable-pairs-tables:end
