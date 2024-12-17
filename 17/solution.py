import sys

def combo(operand, p):
    if operand < 4:
        return operand
    elif operand == 4:
        return p['a']
    elif operand == 5:
        return p['b']
    elif operand == 6:
        return p['c']
    else:
        return None

def adv(operand, p):
    p['ptr'] += 2
    p['a'] >>= combo(operand, p)
    return p
def blx(operand, p):
    p['ptr'] += 2
    p['b'] ^= operand
    return p
def bst(operand, p):
    p['ptr'] += 2
    p['b'] = combo(operand, p) % 8
    return p
def jnz(operand, p):
    if p['a']!= 0:
        p['ptr'] = combo(operand, p)
    else:
        p['ptr'] += 2
    return p
def bxc(operand, p):
    p['ptr'] += 2
    p['b'] ^= p['c']
    return p
def out(operand, p):
    p['ptr'] += 2
    p['output'].append(combo(operand, p) % 8)
    return p
def bdv(operand, p):
    p['ptr'] += 2
    p['b'] = p['a'] >> combo(operand, p)
    return p
def cdv(operand, p):
    p['ptr'] += 2
    p['c'] = p['a'] >> combo(operand, p)
    return p

def run(program, p):
    ptr = p['ptr']
    while ptr < len(program) - 1:
        p = op[program[ptr]](program[ptr+1], p)
        ptr = p['ptr']
    return p['output']

with open(sys.argv[1]) as f:
    p = dict()
    p['a'] = int(f.readline().strip('\n').split(': ')[-1])
    b = int(f.readline().strip('\n').split(': ')[-1])
    p['b'] = b
    c = int(f.readline().strip('\n').split(': ')[-1])
    p['c'] = c
    p['output'] = []
    p['ptr'] = 0
    f.readline()
    program = list(map(int, f.readline().strip('\n').split(': ')[-1].split(',')))
    op = {
        0: adv,
        1: blx,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    output = run(program, p)
    print('Part 1:',','.join(map(str, output)))
    vs = [i for i in range(8)]
    while True:
        for a in vs:
            p = {
                'a': a,
                'b': b,
                'c': c,
                'ptr': 0,
                'output': [],
            }
            output = run(program, p)
            if output == program[len(program)-len(output):]:
                base = a << 3
                for i in range(8):
                    vs.append(base + i)
                if len(output) == len(program):
                    print('Part 2:', a)
                    exit()
