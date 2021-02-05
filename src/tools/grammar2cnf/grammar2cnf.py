import os

from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from pyformlang.regular_expression import Regex

from cfpq_data_devtools.data_wrapper import DataWrapper
from src.tools.CmdParser import CmdParser

EPS_SYM = 'eps'
SUPPORTED_REGEX_CHARS = '.*()?|'


# Counter function used to create unique variable names
def get_new_var_num():
    get_new_var_num.calls += 1
    return get_new_var_num.calls


get_new_var_num.calls = 0


def regex_to_grammar_productions(regex, head, var_dict, terminal_dict):
    _var_dict = {}
    production_set = set()

    # Getting an NFA from regex
    enfa = regex.to_epsilon_nfa()
    enfa = enfa.minimize()
    transitions = enfa._transition_function._transitions

    # Producing variables from NFA states
    for state in enfa.states:
        _var_dict[state] = Variable(
            # Creating new CFG variable with unique name
            '%s#REGEX#%s' % (head.value, get_new_var_num())
        )

    for head_state in transitions:
        # Adding productions from head to start states
        for start_state in enfa.start_states:
            start_p = Production(head, [_var_dict[start_state]])
            production_set.add(start_p)

        # Getting productions from NFA transitions
        for sym in list(transitions[head_state]):
            body_state = transitions[head_state][sym]
            inner_head = _var_dict[head_state]
            inner_body = []

            if sym in var_dict:
                inner_body.append(var_dict[sym])
            elif sym in terminal_dict:
                inner_body.append(terminal_dict[sym])
            elif sym == EPS_SYM:
                inner_body.append(Epsilon())
            else:
                raise ValueError(f'''Symbol "{sym}" is not defined as
                                 a terminal or a variable''')

            inner_body.append(_var_dict[body_state])
            production_set.add(
                Production(inner_head, inner_body)
            )

            if transitions[head_state][sym] in enfa.final_states:
                eps_p = Production(_var_dict[body_state], [])
                production_set.add(eps_p)
    return production_set


def from_txt(lines):
    var_dict = {}
    terminal_dict = {}
    production_set = set()

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
        pr = l.split(' -> ')
        head = var_dict[pr[0]]
        body_str = pr[1].rstrip('\n')

        # pyformlang doesn't accept '?' quantifier, transforming to alternative expression
        body_str = body_str.replace('?', f'|{EPS_SYM}')

        production_set |= regex_to_grammar_productions(
            Regex(body_str),
            head,
            var_dict,
            terminal_dict
        )

    cfg = CFG(
        start_symbol=start_var, productions=production_set
    )

    print('Context-free grammar loaded.')
    # DEBUG OUTPUT
    # for w in list(cfg.get_words(5)):
    #     print(w)
    # print(cfg.start_symbol)
    # print(f'Variables: {cfg.variables}')
    # print(f'Terminals: {cfg.terminals}')
    # print(f'Productions: {cfg.productions}')

    return cfg


def to_txt(cfg):
    variables, productions, terminals = '', '', ''

    for var in cfg.variables:
        if var != cfg.start_symbol:
            variables += f'{var.value} '
    for ter in cfg.terminals:
        terminals += f'{ter.value} '
    for pr in cfg.productions:
        head = pr.head.value
        productions += (f'{head} -> ')
        for sym in pr.body:
            productions += f'{sym.value} '
        productions += '\n'
    return f'{cfg.start_symbol} {variables}\n{terminals}\n{productions}'


def convert(input, output):
    with open(input, 'r') as input_file:
        cfg = from_txt(input_file.readlines())
        cfg = cfg.to_normal_form()
        with open(output, 'w') as output_file:
            output_file.write(to_txt(cfg))
            print(f'Grammar in CNF written to {output}')


def conver_suites(suites):
    data = DataWrapper()
    for suite in suites:
        for grammar in data.get_grammars(suite, include_extension='txt'):
            convert(grammar, f'{os.path.splitext(grammar)[0]}.cnf')


class Grammar2Cnf(CmdParser):
    @staticmethod
    def init_cmd_parser(parser):
        subparsers = parser.add_subparsers(required=True, dest='mode')
        file_parser = subparsers.add_parser('file')
        set_parser = subparsers.add_parser('set')
        subparsers.add_parser('all')

        file_parser.add_argument('path')
        file_parser.add_argument('--output', help='file path to store result')

        set_parser.add_argument('suite', nargs='*', choices=DataWrapper().get_suites())

    @staticmethod
    def eval_cmd_parser(args):
        if args.mode == 'file':
            inp = args.path
            if args.output is None:
                output = f'{os.path.splitext(inp)[0]}.cnf'
            else:
                output = args.output
            convert(inp, output)
        elif args.mode == 'set':
            conver_suites(args.suite)
        elif args.mode == 'all':
            conver_suites(DataWrapper().get_suites())
