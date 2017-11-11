from pylab import *

n, m = 10000, 10000

history = arange(1.*n*m).reshape((n, m))
delays = (500*abs(randn(m, m))).astype(int32) % n

for i in xrange(m):
	for j in xrange(m):
		if j > i:
			delays[i, j] = delays[j, i]

indices = tile(arange(m), (m, 1))

lin_indices = m*delays + indices

# three options for indexing:
# history[delays, indices], history.flat[lin_indices], take(history, lin_indices)

# n, m = 1000, 100

>>> %timeit history[delays, indices]
1000 loops, best of 3: 330 us per loop

>>> %timeit history.flat[lin_indices]
10000 loops, best of 3: 85.1 us per loop

>>> %timeit take(history, lin_indices, mode='wrap')
10000 loops, best of 3: 24.9 us per loop

# n, m = 10000, 1000

>>> %timeit history[delays, indices]
10 loops, best of 3: 99.7 ms per loop

>>> %timeit history.flat[lin_indices]
10 loops, best of 3: 33.7 ms per loop

>>> %timeit take(history, lin_indices, mode='wrap')
10 loops, best of 3: 20.3 ms per loop

>>> history.nbytes/1024/1024
76

# n, m = 10000, 10000; on one core of the cluster

>>> %timeit history[delays, indices]
1 loops, best of 3: 12.7 s per loop

>>> %timeit history.flat[lin_indices]
1 loops, best of 3: 3.5 s per loop

>>> %timeit take(history, lin_indices, mode='wrap')
1 loops, best of 3: 1.56 s per loop

>>> history.nbytes/1024/1024
762

