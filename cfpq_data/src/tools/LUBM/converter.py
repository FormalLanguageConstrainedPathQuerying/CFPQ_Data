"""
    RDF merger and converter for LUBM dataset.
    Database is stored in files <prefix><id>_<sub_id>.owl
    This files are merged for specified number of universities (ids range),
    and edges are replaced with specified mapping.
    Also vertices labels also replaces with integer based names.

    Usage:
    - Create a conversion configuration file. Each line must contain an IRI,
    a whitespace character and a string to replace the IRI by.
    - Run main.py LUBM convert --pref PREFIX --count COUNT --conf CONFIG
    - Result will have name <prefix><count><vertices count><indices count>.xml

    The graph will contain explicit inverted edges added an 'R'.
    """

import subprocess

from cfpq_data.src.tools.CmdParser import CmdParser
from cfpq_data.src.utils import *

MAX_FILES_PER_UNI = 30


class LUBMGraph(CmdParser):
    @staticmethod
    def init_cmd_parser(parser):
        subparsers = parser.add_subparsers(required=True, dest='mode')
        prepare_parser = subparsers.add_parser('prepare')
        converter_parser = subparsers.add_parser('convert')

        prepare_parser.add_argument('--pref', required=True)
        prepare_parser.add_argument('--new', required=True)

        converter_parser.add_argument('--pref', required=True)
        converter_parser.add_argument('--count', required=True, type=int)
        converter_parser.add_argument('--conf', required=True)

    @staticmethod
    def eval_cmd_parser(args):
        if args.mode == 'prepare':
            prefix = args.pref
            new = args.new
            files = os.listdir()

            for f in files:
                if f.startswith(prefix):
                    name = f.replace(prefix, new)
                    try:
                        os.rename(f, name)
                    except Exception:
                        print('Failed to rename file: ' + f + ' to ' + name)
        elif args.mode == 'convert':
            subprocess.run('bash src/tools/LUBM/download.sh')
            subprocess.run('bash src/tools/LUBM/generate.sh')

            replace = {}  # map for replacing predicates
            config = args.conf
            for l in open(config, 'r').readlines():
                pair = l.split(' ')
                old = rdflib.URIRef(pair[0].strip(' '))
                new = pair[1].strip('\n').strip(' ')
                replace[old] = new

            print(replace)

            res = {}  # map from resources to integer ids
            next_id = 0  # id counter
            edges_count = 0  # Total edges

            graph = rdflib.Graph()
            prefix = args.pref
            count = args.count

            processed = []
            notreplaced = set()

            for i in range(0, count):
                for j in range(0, MAX_FILES_PER_UNI):
                    filename = prefix + str(i) + '_' + str(j) + '.owl'
                    try:
                        g = rdflib.Graph()
                        g.parse(filename)

                        for s, p, o in g:
                            for r in [s, o]:
                                if r not in res:
                                    res[r] = str(next_id)
                                    next_id += 1

                            if p in replace:
                                add_rdf_edge(res[s], replace[p], res[o], graph)
                                add_rdf_edge(res[s], replace[p] + 'R', res[o], graph)
                                edges_count += 2
                            else:
                                add_rdf_edge(res[s], 'OTHER', res[o], graph)
                                edges_count += 1
                                notreplaced.add(p)

                        processed.append(filename)
                        print('Merged:', filename)
                    except Exception:
                        pass

            target = prefix + str(count) + 'v' + str(next_id) + 'e' + str(edges_count)  # output file
            write_to_rdf(target, graph)

            print('Total vertices:', next_id)
            print('Total edges:', edges_count)
            print('Processed files:\n', processed)
            print('Not replaced labels:', notreplaced)
