def f(n):
    return (float(n) - 1) * 4/5

def f_6(n):
    for _ in range(6):
        n = f(n)
    return n

def is_int(n):
    return (n - int(n)) == 0

coconuts = 1
while True:
    if is_int(f_6(coconuts)):
        break
    coconuts += 1

print coconuts
