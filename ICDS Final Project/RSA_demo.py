import random

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def lcm(a, b):
    return a * b // gcd(a, b)

def power(x, p, M):
    if p == 0:
        return 1
    tmp = power(x, p // 2, M)
    ans = tmp * tmp % M
    if p % 2 == 1:
        ans = ans * x % M
    return ans

def primes(N):
    p = []
    d = {}
    t = 2
    while t < N:
        if d.get(t, 0) == 0:
            p.append(t)
            #print(t)
        for each in p:
            d[each * t] = 1
            if t % each == 0:
                break
        t += 1
    return p

def generate_primes(p):
    p1 = p2 = 0
    while p1 == p2 or p1 < 1000 or p2 < 1000:
        p1 = p[random.randint(0, len(p) - 1)]
        p2 = p[random.randint(0, len(p) - 1)]
    return p1, p2

def generate_keys():
    ps = primes(10000)
    p, q = generate_primes(ps)
    M = p * q
    k = (p - 1) * (q - 1)
    e = random.randint(1, k + 1)
    while gcd(e, k) != 1:
        e = random.randint(1, k + 1)
    d = 1
    while d < k:
        if d * e % k == 1:
            break
        d += 1
    return M, e, d
# M, e are public, d is private

def encrypt(s, M, e):
    ans = []
    step = len(str(M))
    for ch in s:
        x = ord(ch)
        tmp = str(power(x, e, M))
        while len(tmp) < step:
            tmp = '0' + tmp
        ans.append(tmp)
    return ''.join(ans)

def decrypt(c, M, d):
    loc = 0
    ans = []
    step = len(str(M))
    while loc < len(c):
        x = int(c[loc : loc + step])
        tmp = chr(power(x, d, M))
        ans.append(tmp)
        loc += step
    return ''.join(ans)

"""M, e, d = generate_keys()
print(M, e, d)
while 1:
    s = input()
    if s == "quit":
        break
    code = encrypt(s, M, e)
    print(code)
    print(decrypt(code, M, d))"""
