#! /usr/bin/env python

"""
Org Column Append
Usage:
  oca.py <file1> <file2> [-o=<output>] [-c=<column>] [-f]
  oca.py (-h | --help)

  <file1>   org file 1
  <file2>   org file 2

Options:
  -h --help             Show this screen.
  -c --column=<column>  Column to append (zero based) [default: 0]
  -o --output=<output>  File to save output to
  -f --force            Overwrites output file if it exists
"""

from docopt import docopt
import os

def read_table(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    has_header = any([l.startswith('|--') for l in lines])
    lines = [l.strip() for l in lines
             if not l.startswith('|--')]  # filter frame lines
    lines = [l for l in lines
             if l.startswith('|')]  # filter title
    lines = [l for l in lines
             if len(l) > 0]  # filter empty lines
    split_lines = [l.split('|') for l in lines]
    clean_lines = [[i.strip() for i in l if i.strip()] for l in split_lines]
    header = None
    if has_header:
        header = clean_lines[0]
        clean_lines = clean_lines[1:]
    return header, clean_lines

if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.1')
    # print arguments
    file1 = arguments['<file1>']
    file2 = arguments['<file2>']
    column = int(arguments['--column'])
    output = arguments['--output']
    force = arguments['--force']

    header1, lines1 = read_table(file1)
    header2, lines2 = read_table(file2)

    # If one file has more lines than the other, ignore the extra lines
    num_lines = min(len(lines1), len(lines2))
    lines1 = lines1[:num_lines]
    lines2 = lines2[:num_lines]

    appended = zip(map(lambda x: x[column], lines1), map(lambda x: x[column], lines2))
    outstring = '| ' + '|\n| '.join([' | '.join(i) for i in appended]) + '|\n'
    if output:
        if not os.path.exists(output) or force:
            with open(output, 'w') as f:
                f.write('|----------------+-----------------|\n')
                f.write('|  {}   | {} |\n'.format(file1, file2))
                f.write('|----------------+-----------------|\n')
                f.write(outstring)
                f.write('|----------------+-----------------|\n')
        else:
            print "File exists:", output
