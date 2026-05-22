Grammar
-------

The grammar file is attached to the archive.

.. math::

   S &\to \varepsilon \\
     &\mid \texttt{eps} \quad S \\
     &\mid Q \quad S \\
     &\mid V \quad S \\
   S\#psh\_i &\to \texttt{psh\_i} \quad S \\
   S\#vpsh\_i &\to \texttt{vpsh\_i} \quad S \\
   V &\to S\#vpsh\_i \quad \texttt{vpp\_i} \\
   Q &\to S\#psh\_i \quad \texttt{pp\_i}
