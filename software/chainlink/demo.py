import random
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
    p = ask_for_serial_port_if_necessary()
    with splitflap_context(p) as s:
        modules = s.get_num_modules()
        alphabet = s.get_alphabet()

        # Show a random set of words every 10 seconds
        while True:
            string = ''
            while len(string) < modules:
                string += random.choice(words)
            s.set_text(transform(string))
            time.sleep(10)


if __name__ == '__main__':
    _run()
