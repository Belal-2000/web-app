from string import ascii_lowercase , ascii_uppercase , punctuation
from itertools import cycle


# making dict
spi1 = punctuation+'1234567890 '
spi2 = '1234567890 ' + punctuation
out_of_book = {k: v for k, v in zip(spi1, spi2)}
out_of_book2 = {v: k for k, v in zip(spi1, spi2)}
dict1 = {k: {m: ascii_lowercase[(i + x + 1) % len(ascii_lowercase)] for x, m in enumerate(ascii_lowercase)} for i, k in enumerate(ascii_lowercase)}
dict2 = {k: {m: ascii_uppercase[(i + x + 1) % len(ascii_uppercase)] for x, m in enumerate(ascii_uppercase)} for i, k in enumerate(ascii_uppercase)}
for i in dict1:
    dict1[i].update(dict2[i.upper()])
cifer_book = dict1
recifer_book = {k_: {k: v for v, k in dict1[k_].items()} for k_ in dict1}


# making func to cifer text ..
def cifer(massage , key , order):
    if order == 'r':
        outbut = ''
        for m, k in zip(massage, cycle(key)):
            if m.lower() in cifer_book:
                k1 = recifer_book[k]
                if isinstance(k1, dict):
                    outbut += k1[m]
                else:
                    outbut += k1
            elif m in out_of_book2:
                outbut += out_of_book2[m]
            else:
                outbut += m
    elif order == 'c':
        outbut = ''
        for m, k in zip(massage, cycle(key)):
            if m.lower() in cifer_book:
                k1 = cifer_book[k]
                if isinstance(k1, dict):
                    outbut += k1[m]
                else:
                    outbut += k1
            elif m in out_of_book:
                outbut += out_of_book[m]
            else:
                outbut += m
    return outbut
