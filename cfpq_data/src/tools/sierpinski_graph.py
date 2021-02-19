def gen_sierpinski_graph(target_dir, degree, predicates=('A')):
    """ Generates a Sierpinski Triangle graph. """

    def sierpinski(t, l, r, deg, preds, g):
        """ Core function for generating the Sierpinski Triangle. """

        if deg > 0:
            lt = next(ids)
            tr = next(ids)
            rl = next(ids)
            sierpinski(l, lt, rl, deg - 1, preds, g)
            sierpinski(lt, t, tr, deg - 1, preds, g)
            sierpinski(rl, tr, r, deg - 1, preds, g)
        else:
            add_edges(l, t, preds, g)
            add_edges(t, r, preds, g)
            add_edges(r, l, preds, g)

    def add_edges(u, v, preds, g):
        """ Adds edges between vertices u and v for all predicates. """

        for p in preds:
            g += [[u, p, v]]
            g += [[v, p, u]]

    def _idgen():
        """ Generates integer identifiers for vertices. """

        c = 4
        while True:
            yield c
            c += 1

    ids = _idgen()
    graph = []
    sierpinski(1, 2, 3, degree, predicates, graph)

    with open(target_dir / f'sierpinskigraph_{degree}.txt', 'w') as out_file:
        for triple in graph:
            out_file.write(f'{triple[0]} {triple[1]} {triple[2]} \n')
