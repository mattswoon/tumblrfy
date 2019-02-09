import argparse
import logging

from .ops import *
from .ops.core import OPERATIONS, DESCRIPTIONS


def get_text(parsed_args):
    if parsed_args.input:
        with open(parsed_args.input, 'r') as f:
            text = f.read()
        return text
    if parsed_args.text:
        return parsed_args.text


def write_out(text, fname):
    if fname:
        with open(fname, 'w') as f:
            f.write(text)
    else:
        print(text)


def desc(op):
    return DESCRIPTIONS[op].replace('\n', '\n\t\t')


def main():
    parser = argparse.ArgumentParser(
        description='Make your text more tumblr'
    )
    parser.add_argument(
        '--ops',
        nargs='+',
        default=list(OPERATIONS.keys()),
        help='Operations to use to tumblrfy your text'
    )
    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='List available operations'
    )
    parser.add_argument(
        '-i',
        '--input',
        help='Input file to tumblrfy'
    )
    parser.add_argument(
        '-o',
        '--output',
        help='Output file'
    )
    parser.add_argument(
        '-t',
        '--text',
        help='Text to tumblrfy'
    )
    parsed_args = parser.parse_args()

    if parsed_args.list:
        print(
            'Available operations are \n\t' + '\n\n\t'.join(
                [f'{op}:\t{desc(op)}' for op in OPERATIONS.keys()]
            )
        )
    else:
        text = get_text(parsed_args)
        for op_name in parsed_args.ops:
            text = OPERATIONS[op_name](text)
        write_out(text, parsed_args.output)


if __name__ == '__main__':
    main()
