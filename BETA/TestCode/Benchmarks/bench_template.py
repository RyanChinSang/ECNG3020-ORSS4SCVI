import timeit


def f1():
    pass


def f2():
    pass


iterations = 10000

fn1 = timeit.Timer(stmt='f1()', setup='from __main__ import f1')
fn2 = timeit.Timer(stmt='f2()', setup='from __main__ import f2')

fn1.val = fn1.timeit(iterations)
fn2.val = fn2.timeit(iterations)

min_val = min([fn1.val, fn2.val])

print('fn1 %0.12f (%0.2f%% as fast)' % (fn1.val, (100 * min_val / fn1.val), ))
print('fn2 %0.12f (%0.2f%% as fast)' % (fn2.val, (100 * min_val / fn2.val), ))

