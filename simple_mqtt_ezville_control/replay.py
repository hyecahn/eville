import re
import sys

# Simple replay harness to verify arrival-detection branching.
# Usage:
#   python replay.py [path/to/logfile.log]
# If no file provided, runs builtin sample packets.

SAMPLE_PACKETS = [
    'F7330143018007F6',  # arrival sample
    'F7330143011097AABB', # ack-like sample
    'F7330181030024006336' # sendcmd sample
]


def check_packet(packet):
    p = re.sub(r'\s+', '', packet).upper()
    print('Packet: {}'.format(p))
    print(' Length:', len(p))
    try:
        s2_14 = p[2:14]
    except Exception:
        s2_14 = ''
    try:
        s2_12 = p[2:12]
    except Exception:
        s2_12 = ''
    print(' packet[2:14]:', s2_14)
    print(' packet[2:12]:', s2_12)

    # Mirror the detection logic in `ezville.py` (including the recent fix)
    if s2_14 == '33014301800716' or s2_14 == '33014301800706' or s2_14 == '330143018007':
        print(' -> Decision: ALERT BRANCH (arrival detected)')
    else:
        print(' -> Decision: ELSE BRANCH (no arrival)')
    print('-' * 60)


def extract_packets_from_file(path):
    data = open(path, 'r', encoding='utf-8', errors='ignore').read()
    # find contiguous hex tokens starting with F7 (common in logs)
    tokens = re.findall(r'(F7[0-9A-Fa-f]+)', data)
    return tokens


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print('Reading file:', path)
        tokens = extract_packets_from_file(path)
        if not tokens:
            print('No F7-hex tokens found in file.')
            sys.exit(0)
        for t in tokens:
            check_packet(t)
    else:
        print('No file provided — running built-in samples')
        for t in SAMPLE_PACKETS:
            check_packet(t)
