from src.tools.install import InstallTool
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', required=True)

    tools = {
        'install': InstallTool(),
        # all tools will be here
    }
    for name, tool in tools.items():
        subparser = subparsers.add_parser(name)
        tool.init_parser(subparser)

    args = parser.parse_args()
    tools[args.tool].eval(args)

