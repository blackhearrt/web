import time
import multiprocessing

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers):
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(factorize, numbers)
    return results

def main_parallel():
    numbers = [128, 255, 99999, 10651060]

    start_time = time.time()
    results = factorize_parallel(numbers)
    end_time = time.time()

    print("Parallel Execution Time:", end_time - start_time)
    return results

if __name__ == "__main__":
    results_parallel = main_parallel()
    print(results_parallel)
