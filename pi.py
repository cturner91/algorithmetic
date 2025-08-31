# estimate pi with high accuracy using the algorithmetic methods
# Use a monte-carlo approach - generate two random numbers, work out their hypotenuse
# if hyptoenuse > 1, counts as outside, otherwise is inside

import math
from concurrent.futures import ProcessPoolExecutor
from random import choice

from operations import multiply, add, divide, subtract


N = 1_000_000  # iterations for each worker
N_WORKERS = 5
UPDATE_INTERVAL = 10_000  # how frequently to provide updates

# length of random number
RAND_LENGTH = 10

# Pick up where we left off last time?
STARTING_COUNT_INSIDE = 0
STARTING_COUNT_OUTSIDE = 0


def rand(length: int = 10) -> str:
    CHARS = '0123456789'
    return f"0.{''.join(choice(CHARS) for _ in range(length))}"


def run_batch(iterations: int, worker_id: int = -1) -> tuple[int, int]:
    # Runs a number of iterations and return the count of points found to be inside & outside
    # Splitting into separate func so we can multi-process
    count_inside, count_outside = 0, 0
    for i in range(iterations):
        x = rand(RAND_LENGTH)
        y = rand(RAND_LENGTH)

        # to keep precision, use string operations
        x2 = multiply(x, x)
        y2 = multiply(y, y)
        hypotenuse = add(x2, y2)  # string

        # If >= 1, it's outside
        is_inside = hypotenuse[0] == '0'
        if is_inside:
            count_inside += 1
        else:
            count_outside += 1

        if i % UPDATE_INTERVAL == 0:
            pc = (i + 1) / iterations * 100
            print(f"Worker {worker_id}: {pc:.2f}% completed")

    return count_inside, count_outside


if __name__ == '__main__':

    counts = []
    with ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
        futures = []
        for worker_id in range(N_WORKERS):
            futures.append(executor.submit(run_batch, N, worker_id))

        for future in futures:
            count_inside, count_outside = future.result()
            counts.append((count_inside, count_outside))
            print(f"Batch result: inside = {count_inside}, outside = {count_outside}")

    total_count_inside = sum(count[0] for count in counts) + STARTING_COUNT_INSIDE
    total_count_outside = sum(count[1] for count in counts) + STARTING_COUNT_OUTSIDE

    pi_estimate = multiply(divide(str(total_count_inside), add(str(total_count_inside), str(total_count_outside))), str(4))
    accuracy = multiply(divide(subtract(pi_estimate, str(math.pi)), str(math.pi)), str(100))

    print(f"Estimated value of pi: {pi_estimate}")
    print(f"Pythonic  value of pi: {math.pi}")
    print(f"Accuracy: {accuracy} %")
    print(f"Final counts: inside = {total_count_inside}, outside = {total_count_outside}")
