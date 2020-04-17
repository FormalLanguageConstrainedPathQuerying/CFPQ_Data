from pyformlang.cfg import Production, Variable, Terminal, CFG
from pyformlang.regular_expression import Regex
import argparse
import re

EPS_SYM = 'eps'
SUPPORTED_REGEX_CHARS = '.+*()?'

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
            elif sym != EPS_SYM:
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

        for body in body_str.split('|'):
            if any(i in body for i in SUPPORTED_REGEX_CHARS):
                # Getting productions when body has regex

                # pyformlang doesn't accept '?' quantifier, transforming to alternative expression
                body = body.replace('?',f'+{EPS_SYM}')
                production_set |= regex_to_grammar_productions(
                    Regex(body),
                    head,
                    var_dict,
                    terminal_dict
                )
            else:
                # Getting productions when body has no regex
                inner_body = []
                for sym in body.split():
                    if sym in var_dict:
                        inner_body.append(var_dict[sym])
                    elif sym in terminal_dict:
                        inner_body.append(terminal_dict[sym])
                    elif sym != EPS_SYM:
                        raise ValueError(f'''Symbol "{sym}" is not defined as
                                        a terminal or a variable''')
                p = Production(head, inner_body)
                production_set.add(p)

    cfg = CFG(
        start_symbol=start_var, productions=production_set
    )

    print('Context-free grammar loaded.')
    # DEBUG OUTPUT
    # for w in list(cfg.get_words(5)):
    #     print(w)
    # print(f'Variables: {cfg.variables}')
    # print(f'Terminals: {cfg.terminals}')
    # print(f'Productions: {cfg.productions}')

    return cfg


def to_txt(cfg):
    variables, productions, terminals = '', '', ''

    for var in cfg.variables:
        variables += f'{var.value} '
    for ter in cfg.terminals:
        terminals += f'{ter.value} '
    for pr in cfg.productions:
        head = pr.head.value
        productions += (f'{head} -> ')
        for sym in pr.body:
            productions += f'{sym.value} '
        productions += '\n'
    return f'{variables}\n{terminals}\n{productions}'


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input',
                        type=argparse.FileType('r')
                        )
    parser.add_argument("-o", "--output",
                        help="Directs the output to a name of your choice",
                        required=True
                        )
    args = parser.parse_args()

    cfg = from_txt(args.input.readlines())
    cfg = cfg.to_normal_form()
    with open(args.output, 'w') as output_file:
        output_file.write(to_txt(cfg))
        print(f'Grammar in CNF written to {args.output}')


if __name__ == "__main__":
    main()
