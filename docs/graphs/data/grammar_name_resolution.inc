Grammar
-------

The grammar file is attached to the archive.

.. math::

   S &\to \varepsilon \\
     &\mid eps \quad S \\
     &\mid Q \quad S \\
     &\mid V \quad S \\
   S\#psh_{i} &\to psh_{i} \quad S \\
   S\#vpsh_{i} &\to vpsh_{i} \quad S \\
   V &\to S\#vpsh_{i} \quad vpp_{i} \\
   Q &\to S\#psh_{i} \quad pp_{i}
