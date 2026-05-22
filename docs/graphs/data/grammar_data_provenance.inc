Grammar
-------

The grammar file is attached to the archive.

.. math::

   S &\to Entity \quad Core \quad Entity \\
   Core &\to wasDerivedFrom \\
        &\mid wasDerivedFrom_{r} \\
        &\mid specializationOf \\
        &\mid specializationOf_{r} \\
        &\mid wasGeneratedBy \quad Activity \quad used \\
        &\mid used_{r} \quad Activity \quad wasGeneratedBy_{r} \\
        &\mid wasGeneratedBy \quad Activity \quad Core \\
        &\quad Activity \quad wasGeneratedBy_{r} \\
        &\mid used_{r} \quad Activity \quad Core \\
        &\quad Activity \quad used \\
        &\mid wasDerivedFrom \quad Entity \quad Core \\
        &\quad Entity \quad wasDerivedFrom_{r} \\
        &\mid specializationOf \quad Entity \quad Core \\
        &\quad Entity \quad specializationOf_{r}
