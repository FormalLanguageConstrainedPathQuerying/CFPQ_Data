Grammar
-------

This grammar is taken from ``grammar/kotgll/name_resolution.cfg`` in the graph archive.
The start nonterminal is :math:`Q`.

.. math::

   S &\to \varepsilon \\
   S &\to \mathit{eps} \; S \\
   S &\to Q \; S \\
   S &\to V \; S \\
   S_{\mathit{psh}_i} &\to \mathit{psh}_i \; S \\
   S_{\mathit{vpsh}_i} &\to \mathit{vpsh}_i \; S \\
   V &\to S_{\mathit{vpsh}_i} \; \mathit{vpp}_i \\
   Q &\to S_{\mathit{psh}_i} \; \mathit{pp}_i \\
   &\forall i
