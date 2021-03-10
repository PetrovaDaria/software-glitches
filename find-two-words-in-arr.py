arr = ['first', 'second', 'third', 'fourth']
pairs = list(' '.join(pair) for pair in zip(arr, arr[1:]))
triples = list(' '.join(pair) for pair in zip(arr, arr[1:], arr[2:]))
print(pairs)
print(triples)

arr2 = ['glitching']
print('glitching' in arr2)

d1 = {
    'a': 1,
    'b': 2
}

d2 = {
    'a': 3,
    'd': 4
}

def join_dicts(d1, d2):
    new_d = {}
    new_d.update(d1)
    for k, v in d2.items():
        if k in new_d.keys():
            new_d[k] += v
        else:
            new_d[k] = v
    return new_d

print(join_dicts(d1, d2))


