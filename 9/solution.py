import sys

with open(sys.argv[1]) as f:
    line = f.readline().strip('\n')
    s = []
    free_blocks = []
    file_blocks = []
    id = 0
    for i, c in enumerate(line):
        if i % 2 > 0:
            free_blocks.append((len(s), int(c)))
            for _ in range(int(c)):
                s.append(-1)
        else:
            file_blocks.append((id, len(s), int(c)))
            for _ in range(int(c)):
                s.append(id)
            id += 1
    i = 0
    j = len(s) - 1
    while i <= j:
        if s[i] != -1:
            i += 1
        elif s[j] == -1:
            j -= 1
        else:
            s[i] = s[j]
            s[j] = -1
    for i, (id, idx_file, size_file) in enumerate(file_blocks[::-1]):
        for j, (idx_free, size_free) in enumerate(free_blocks):
            if idx_free > idx_file:
                break
            elif size_file <= size_free:
                free_blocks[j] = (idx_free + size_file, size_free - size_file)
                del file_blocks[file_blocks.index((id, idx_file, size_file))]
                file_blocks.insert(j+1, (id, idx_free, size_file))
                break
    checksum = 0
    for i, e in enumerate(s):
        if e != -1:
            checksum += i * e
    print('Part 1:', checksum)

    checksum = 0
    for id, idx, size in file_blocks:
        for i in range(idx, idx+size):
            checksum += i*id
    print('Part 2:', checksum)
