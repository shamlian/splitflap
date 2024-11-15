import argparse
import random
import sys
import textwrap
import time

from splitflap_proto import (
    ask_for_serial_port_if_necessary,
    splitflap_context,
)

words = [
    'ALPACA', 'BABOON', 'BADGER', 'BELUGA', 'BOBCAT', 'FERRET',
    'GOPHER', 'IMPALA', 'JACKAL', 'JAGUAR', 'KITTEN', 'MARMOT',
    'MONKEY', 'OCELOT', 'RABBIT', 'RACOON', 'TURTLE', 'WALRUS',
    'WEASEL', 'WOMBAT',
]

def transform(s):
    # for vertically interleaved chanlink drivers
    # c = 6 # number of columns in the display
    # return "".join(i + j for i, j in zip(s[c:c*2], s[0:c]))

    # for a normal run of chainlink drivers
    # return s

    # For my ridiculous arrangement
    c = 6
    s = s[::-1]
    s = ''.join(i + j for i, j in zip(s[c:c*2], s[0:c]))
    s = s[0:c] + ''.join(j+i for i, j in zip(s[c::2], s[c+1::2]))
    return s

def _run():
    parser = argparse.ArgumentParser(prog='Demo',
                                     description='Splitflap Demo')
    parser.add_argument('-i', '--infile', nargs='?',
                        type=argparse.FileType('r'),
                        const=sys.stdin, default=None,
                        help='Input file to display on splitflap')
    parser.add_argument('-c', '--console', action='store_true',
                        help='Console-interactive mode')
    parser.add_argument('-l', '--loop', action='store_true',
                        help='Flag to loop infinitely (default false)')
    parser.add_argument('-d', '--delay', type=float, default=5.0,
                        help='Delay between display updates in seconds')
    args = parser.parse_args()
    print(args)

    p = ask_for_serial_port_if_necessary()
    with splitflap_context(p) as s:
        modules = s.get_num_modules()
        alphabet = s.get_alphabet()

        while True:
            if args.infile == None:
                if args.console:
                    string = input('> ')[:12].ljust(12)
                else:
                    string = ''
                    while len(string) < modules:
                        string += random.choice(words)
                s.set_text(transform(string))
                time.sleep(args.delay)
            else:
                strings = textwrap.wrap(args.infile.read(), width=6)

                if len(strings) % 2 == 1:
                    strings.append('')

                it = iter(strings)

                for out in [f"{x:6}{y:6}" for x, y in zip(it, it)]:
                    s.set_text(transform(out).upper())
                    time.sleep(args.delay)

                if args.infile != sys.stdin:
                    args.infile.seek(0)

            if not args.loop:
                break


if __name__ == '__main__':
    _run()
