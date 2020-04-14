from functools import reduce
from multiprocessing import Pool, current_process, cpu_count
import time

def add(x, y):
    """Return the sum of the arguments"""
    print(f"Worker {current_process().pid} is processing add({x}, {y})")
    time.sleep(1)
    return x + y

def product(x, y):
    """Return the product of the arguments"""
    print(f"Worker {current_process().pid} is processing product({x}, {y})")
    time.sleep(1)
    return x * y

if __name__ == "__main__":

    a = list(range(1,40))
    b = list(range(21,60))

    print(len(a))
    print(len(b))
    print(cpu_count())

    # Now create a Pool of workers
    with Pool() as pool:
        sum_future = pool.starmap_async(add, zip(a,b))
        product_future = pool.starmap_async(product, zip(a,b))

        sum_future.wait()
        product_future.wait()

    total_sum = reduce(lambda x, y: x + y, sum_future.get())
    total_product = reduce(lambda x, y: x + y, product_future.get())

    print(f"Sum of sums of 'a' and 'b' is {total_sum}")
    print(f"Sum of products of 'a' and 'b' is {total_product}")