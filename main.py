import random
import time


def queen_search(queens):
    while True:
        k = initial_search(queens)
        final_search(queens, k)
        if len(queens) > 200 or (board_collision(queens) == 0):
            break


def initial_search(queens):
    n = len(queens)
    queens[:] = list(range(n))
    j = 0

    # place queens without collisions
    for i in range(int(3.08 * n)):
        if j == n:
            break
        m = random.randint(j, n - 1)
        swap(queens, j, m)
        if partial_collision(queens, j) == 0:
            j += 1
        else:
            swap(queens, j, m)

    # place queens with possible collisions
    for i in range(j, n):
        m = random.randint(i, n - 1)
        swap(queens, i, m)

    # return the number of queens with possible collisions
    return n - j


def final_search(queens, k):
    n = len(queens)
    it = 0
    for i in range(n - k, n):
        if total_collisions(queens, i) > 0:
            while it < 7000:
                j = random.randint(0, n - 1)
                swap(queens, i, j)
                b = (total_collisions(queens, i) > 0) or (total_collisions(queens, j) > 0)
                if b:
                    swap(queens, i, j)
                    it += 1
                else:
                    break


# auxiliary functions
def swap(queens, a, b):
    queens[a], queens[b] = queens[b], queens[a]


def partial_collision(queens, i):
    return sum(1 for j in range(i) if (i - j) == abs(queens[i] - queens[j]))


def total_collisions(queens, i):
    return sum(1 for j in range(len(queens)) if i != j and abs(i - j) == abs(queens[i] - queens[j]))


def board_collision(queens):
    return sum(partial_collision(queens, i) for i in range(len(queens)))


if __name__ == '__main__':
    size = 1
    ex_time = [0] * 7
    for i in range(7):
        size *= 10
        queens = [0] * size
        start = time.perf_counter()
        queen_search(queens)
        end = time.perf_counter()
        ex_time[i] = end - start
        print("n = 10^{} : {} s".format(i + 1, ex_time[i]))
