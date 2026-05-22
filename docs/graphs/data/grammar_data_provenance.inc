Grammar
-------

This grammar is taken from ``grammar/kotgll/prov_derivation.cfg`` in the graph archive.
The start nonterminal is :math:`S`.

.. math::

   S &\to \mathit{Entity} \; S_{1} \\
   S_{1} &\to \mathit{Core} \; \mathit{Entity} \\
   \mathit{Core} &\to \mathit{wasDerivedFrom} \mid \mathit{wasDerivedFrom}^{r} \\
                 &\mid \mathit{specializationOf} \mid \mathit{specializationOf}^{r} \\
                 &\mid \mathit{wasGeneratedBy} \; \mathit{Core}_{1} \\
                 &\mid \mathit{used}^{r} \; \mathit{Core}_{2} \\
                 &\mid \mathit{wasGeneratedBy} \; \mathit{Core}_{3} \\
                 &\mid \mathit{used}^{r} \; \mathit{Core}_{6} \\
                 &\mid \mathit{wasDerivedFrom} \; \mathit{Core}_{9} \\
                 &\mid \mathit{specializationOf} \; \mathit{Core}_{12} \\
   \mathit{Core}_{1} &\to \mathit{Activity} \; \mathit{used} \\
   \mathit{Core}_{2} &\to \mathit{Activity} \; \mathit{wasGeneratedBy}^{r} \\
   \mathit{Core}_{3} &\to \mathit{Activity} \; \mathit{Core}_{4} \\
   \mathit{Core}_{4} &\to \mathit{Core} \; \mathit{Core}_{5} \\
   \mathit{Core}_{5} &\to \mathit{Activity} \; \mathit{wasGeneratedBy}^{r} \\
   \mathit{Core}_{6} &\to \mathit{Activity} \; \mathit{Core}_{7} \\
   \mathit{Core}_{7} &\to \mathit{Core} \; \mathit{Core}_{8} \\
   \mathit{Core}_{8} &\to \mathit{Activity} \; \mathit{used} \\
   \mathit{Core}_{9} &\to \mathit{Entity} \; \mathit{Core}_{10} \\
   \mathit{Core}_{10} &\to \mathit{Core} \; \mathit{Core}_{11} \\
   \mathit{Core}_{11} &\to \mathit{Entity} \; \mathit{wasDerivedFrom}^{r} \\
   \mathit{Core}_{12} &\to \mathit{Entity} \; \mathit{Core}_{13} \\
   \mathit{Core}_{13} &\to \mathit{Core} \; \mathit{Core}_{14} \\
   \mathit{Core}_{14} &\to \mathit{Entity} \; \mathit{specializationOf}^{r}
