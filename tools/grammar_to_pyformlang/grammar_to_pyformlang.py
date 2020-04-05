
from pyformlang.cfg import Production, Variable, Terminal, CFG

INPUT = './examples/example_grammar.txt'

# INPUT FILE FORMAT
#
# Line 0:
#
#   a set of variables delimited by spaces,
#   the first one is the starting symbol
#
# Line 1:
#
#   a set of terminal delimited by spaces
#
# The rest of the lines are productions
# in the form:
#
#   head body


def to_pyformlang(input_file):
    var_dict = {}
    terminal_dict = {}
    production_set = set()

    with open(input_file, "r") as grammar_file:
        lines = grammar_file.readlines()

        # variables
        var_lst = lines[0].split()
        start_var = Variable(var_lst[0])
        for v in var_lst:
            var_dict[v] = Variable(v)

        # terminals
        for t in lines[1].split():
            terminal_dict[t] = Terminal(t)

        # productions
        for l in lines[2:]:
            pr = l.split()
            head = var_dict[pr[0]]
            body = []

            for elem in pr[1:]:
                if elem in var_dict:
                    body.append(var_dict[elem])
                elif elem in terminal_dict:
                    body.append(terminal_dict[elem])
            p = Production(head, body)

            production_set.add(p)

        # cfg
        cfg = CFG(
            set(var_dict.values()),
            set(terminal_dict.values()),
            start_var, production_set
        )

        print('Context-free grammar loaded.')
        print(cfg.variables)
        print(cfg.terminals)
        print(cfg.productions)


if __name__ == "__main__":
    to_pyformlang(INPUT)
