import argparse

import numpy
import os
import rdflib
import shutil

from src.tools.base import Tool
from src.tools.gen_RPQ.RDF_edge_stat import *

templates = [(1, '%s*', 'q1'), (2, '%s %s*', 'q2'), (3, '%s %s* %s*', 'q3'),
             (2, '(%s | %s)*', 'q4_2'), (3, '(%s | %s | %s)*', 'q4_3'), (4, '(%s | %s | %s | %s)*', 'q4_4'),
             (5, '(%s | %s | %s | %s | %s)*', 'q4_5'),
             (3, '%s %s* %s', 'q5'), (2, '%s* %s*', 'q6'), (3, '%s %s %s*', 'q7'), (2, '%s? %s*', 'q8'),
             (2, '(%s | %s)+', 'q9_2'), (3, '(%s | %s | %s)+', 'q9_3'), (4, '(%s | %s | %s | %s)+', 'q9_4'),
             (5, '(%s | %s | %s | %s | %s)+', 'q9_5'),
             (3, '(%s | %s) %s*', 'q10_2'), (4, '(%s | %s | %s) %s*', 'q10_3'), (5, '(%s | %s | %s | %s) %s*', 'q10_4'),
             (6, '(%s | %s | %s | %s | %s) %s*', 'q10_5'),
             (2, '%s %s', 'q11_2'), (3, '%s %s %s', 'q11_3'), (4, '%s %s %s %s', 'q11_4'),
             (5, '%s %s %s %s %s', 'q11_5')]


def gen(tpl, n, lst, k):
    res = set()
    while (len(res) < n):
        perm = numpy.random.permutation(lst)
        res.add(((tpl % tuple(perm[0:k])), tuple(perm[0:k])))
    return res


def gen_from_config(config, num_of_lalbels, num_of_queries):
    lbls = [l.split(' ')[1].rstrip() for l in open(config, 'r').readlines()]
    return [(tpl[2], gen(tpl[1], num_of_queries, lbls[0:num_of_lalbels], tpl[0])) for tpl in templates]


def print_qs(qs, root_dir):
    for qd in qs:
        path = os.path.join(root_dir, qd[0])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        i = 0
        for q in qd[1]:
            with open(os.path.join(path, str(i)), 'w') as out:
                out.write('S\n')
                out.write(' '.join(q[1]) + '\n')
                out.write('S -> ' + q[0] + '\n')
                i = i + 1


class GenRPQTool(Tool):
    def init_parser(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(required=True, dest='mode')
        rdf_edge_stat_parser = subparsers.add_parser('rdf_stat')
        gen_parser = subparsers.add_parser('generate')

        rdf_edge_stat_parser.add_argument('rdf')
        rdf_edge_stat_parser.add_argument('output')

        gen_parser.add_argument('-c', help="a config generated at the rdf_stat mode")
        gen_parser.add_argument('-n', type=int, help="first n_URIs labels from config will be used to generate queryes")
        gen_parser.add_argument('-q', type=int, help="q_for_each_tpl queryes will be generated for each template")
        gen_parser.add_argument('-o', help="result root dir")

    def eval(self, args: argparse.Namespace):
        if args.mode == 'rdf_stat':
            g = rdflib.Graph()

            g.load(args.rdf)

            r = get_labels_count(g)

            for x in r:
                print(x[0], ': ', x[1])

            print_config(r, args.output)
        elif args.mode == 'generate':
            r = gen_from_config(args.c, args.n, args.q)

            print_qs(r, args.o)

            for s in r:
                for q in s:
                    print(q)
