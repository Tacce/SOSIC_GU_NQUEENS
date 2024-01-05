import random
import time
import matplotlib.pyplot as plt

MAX_POWER_10 = 8


def queen_search(queens):
    while True:
        neg_diagonal, pos_diagonal = initialize_diagonal_arrays(len(queens))
        k = initial_search(queens, neg_diagonal, pos_diagonal)
        if len(queens) > 400:
            final_search(queens, k, neg_diagonal, pos_diagonal)
            break
        else:
            final_search_reduced(queens, k, neg_diagonal, pos_diagonal)
            if not board_collision(neg_diagonal, pos_diagonal):
                break


def initial_search(queens, neg_diagonal, pos_diagonal):
    n = len(queens)
    queens[:] = list(range(n))
    j = 0

    # place queens without collisions
    for i in range(int(3.08 * n)):
        if j == n:
            break
        m = random.randint(j, n - 1)
        swap(queens, j, m)
        add_conflict(queens, j, neg_diagonal, pos_diagonal)
        if total_collisions(queens, j, neg_diagonal, pos_diagonal) == 0:
            j += 1
        else:
            remove_conflict(queens, j, neg_diagonal, pos_diagonal)
            swap(queens, j, m)

    # place queens with possible collisions
    for i in range(j, n):
        m = random.randint(i, n - 1)
        swap(queens, i, m)
        add_conflict(queens, i, neg_diagonal, pos_diagonal)

    # return the number of queens with possible collisions
    return n - j


def final_search(queens, k, neg_diagonal, pos_diagonal):
    n = len(queens)
    it = 0
    for i in range(n - k, n):
        if total_collisions(queens, i, neg_diagonal, pos_diagonal) > 0:
            while it < 7000:
                j = random.randint(0, n - 1)
                swap_collision(queens, i, j, neg_diagonal, pos_diagonal)
                b = (total_collisions(queens, i, neg_diagonal, pos_diagonal) > 0) or\
                    (total_collisions(queens, j, neg_diagonal, pos_diagonal) > 0)
                if b:
                    swap_collision(queens, i, j, neg_diagonal, pos_diagonal)
                    it += 1
                else:
                    break


def final_search_reduced(queens, k, neg_diagonal, pos_diagonal):
    n = len(queens)
    for i in range(n - k, n):
        if total_collisions(queens, i, neg_diagonal, pos_diagonal) > 0:
            for j in range(n):
                swap_collision(queens, i, j, neg_diagonal, pos_diagonal)
                b = (total_collisions(queens, i, neg_diagonal, pos_diagonal) > 0) or\
                    (total_collisions(queens, j, neg_diagonal, pos_diagonal) > 0)
                if b:
                    swap_collision(queens, i, j, neg_diagonal, pos_diagonal)
                else:
                    break


# auxiliary functions
def initialize_diagonal_arrays(n):
    neg_diagonal = [0] * (2 * n - 1)
    pos_diagonal = [0] * (2 * n - 1)
    return neg_diagonal, pos_diagonal


def swap(queens, i, j):
    queens[i], queens[j] = queens[j], queens[i]


def swap_collision(queens, i, j, neg_diagonal, pos_diagonal):
    remove_conflict(queens, i, neg_diagonal, pos_diagonal)
    remove_conflict(queens, j, neg_diagonal, pos_diagonal)
    swap(queens, i, j)
    add_conflict(queens, i, neg_diagonal, pos_diagonal)
    add_conflict(queens, j, neg_diagonal, pos_diagonal)


def remove_conflict(queens, i, neg_diagonal, pos_diagonal):
    neg_diagonal[i + queens[i]] -= 1
    pos_diagonal[i - queens[i] + len(queens) - 1] -= 1


def add_conflict(queens, i, neg_diagonal, pos_diagonal):
    neg_diagonal[i + queens[i]] += 1
    pos_diagonal[i - queens[i] + len(queens) - 1] += 1


def total_collisions(queens, i, neg_diagonal, pos_diagonal):
    n = len(queens)
    return neg_diagonal[i + queens[i]] + pos_diagonal[i - queens[i] + n - 1] - 2  # Exclude self-collision


def board_collision(neg_diagonal, pos_diagonal):
    for i in range(len(neg_diagonal)):
        if neg_diagonal[i] > 1 or pos_diagonal[i] > 1:
            return True
    return False


def test():
    ex_time = [0] * MAX_POWER_10
    for i in range(MAX_POWER_10):
        queens = [0] * (10 ** (i + 1))
        start = time.perf_counter()
        queen_search(queens)
        end = time.perf_counter()
        ex_time[i] = end - start
        print("n = 10^{} : {} s".format(i + 1, ex_time[i]))
    generateTable(ex_time)


def generateTable(ex_time):
    power = ["10^{}".format(i + 1) for i in range(MAX_POWER_10)]
    fig, ax = plt.subplots()
    data = [[p, f"{et:.4f}"] for p, et in zip(power, ex_time)]
    ax.table(cellText=data,
             colLabels=["n", "Execution Time (s)"],
             loc='center', colWidths=[0.1, 0.3])
    ax.axis('off')
    fig = plt.gcf()
    plt.title("Execution Times for Powers of 10")
    plt.show()
    fig.savefig("test_table", bbox_inches='tight')


if __name__ == '__main__':
    while True:
        x = input("Insert board size or type 'test' to measure execution times on powers of 10:")
        if x == "end":
            break
        elif x == "test":
            test()
        else:
            x = int(x)
            if x >= 4:
                queens = [0] * x
                start = time.perf_counter()
                queen_search(queens)
                end = time.perf_counter()
                print("Solution: " + str(queens))
                print("Execution Time: " + str(end - start) + " s")
