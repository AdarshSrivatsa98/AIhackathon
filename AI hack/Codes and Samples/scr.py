from multiprocessing import Pool

def f(x):
    return x[0]*x[1]

def multi(x):
    with Pool(x) as p:
        print(p.map(f, [(1,2)]))

if __name__ =='__main__':
    multi(5)
    