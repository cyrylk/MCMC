from multiprocessing import Pool
import os

D = {(i, j): 0 for i in range(10) for j in range(10)}

def poc(a):
    global D
    D[a] = a[0] + a[1]



with Pool(2*os.cpu_count()) as pool:
    s = pool.map(poc, {(i, j): 0 for i in range(10) for j in range(10)})
    for key in D:
        print(D[key])