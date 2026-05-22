Grammar
-------

The grammar file is attached to the archive.

.. math::

   S &\to \texttt{Entity} \quad Core \quad \texttt{Entity} \\
   Core &\to \texttt{wasDerivedFrom} \\
        &\mid \texttt{wasDerivedFrom\_r} \\
        &\mid \texttt{specializationOf} \\
        &\mid \texttt{specializationOf\_r} \\
        &\mid \texttt{wasGeneratedBy} \quad \texttt{Activity} \quad \texttt{used} \\
        &\mid \texttt{used\_r} \quad \texttt{Activity} \quad \texttt{wasGeneratedBy\_r} \\
        &\mid \texttt{wasGeneratedBy} \quad \texttt{Activity} \quad Core \\
        &\quad \texttt{Activity} \quad \texttt{wasGeneratedBy\_r} \\
        &\mid \texttt{used\_r} \quad \texttt{Activity} \quad Core \\
        &\quad \texttt{Activity} \quad \texttt{used} \\
        &\mid \texttt{wasDerivedFrom} \quad \texttt{Entity} \quad Core \\
        &\quad \texttt{Entity} \quad \texttt{wasDerivedFrom\_r} \\
        &\mid \texttt{specializationOf} \quad \texttt{Entity} \quad Core \\
        &\quad \texttt{Entity} \quad \texttt{specializationOf\_r}
