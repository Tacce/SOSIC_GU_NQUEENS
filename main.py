import random
import time
import matplotlib.pyplot as plt

MAX_POWER_10 = 4


def queen_search(queens):
    while True:
        nd, pd = initialize_diagonal_arrays(len(queens))
        k = initial_search(queens, nd, pd)
        if len(queens) > 200:
            final_search(queens, k, nd, pd)
            break
        else:
            final_search_reduced(queens, k, nd, pd)
            if board_collision(queens) == 0:
                break


def initial_search(queens, nd, pd):
    n = len(queens)
    queens[:] = list(range(n))
    update_diagonal_arrays(queens, nd, pd)
    j = 0

    # place queens without collisions
    for i in range(int(3.08 * n)):
        if j == n:
            break
        m = random.randint(j, n - 1)
        swap(queens, j, m, nd, pd)
        if partial_collision(queens, j) == 0:
            j += 1
        else:
            swap(queens, j, m, nd, pd)

    # place queens with possible collisions
    for i in range(j, n):
        m = random.randint(i, n - 1)
        swap(queens, i, m, nd, pd)

    # return the number of queens with possible collisions
    return n - j


def final_search(queens, k, nd, pd):
    n = len(queens)
    it = 0
    for i in range(n - k, n):
        if total_collisions(queens, i, nd, pd) > 0:
            while it < 7000:
                j = random.randint(0, n - 1)
                swap(queens, i, j, nd, pd)
                b = (total_collisions(queens, i, nd, pd) > 0) or (total_collisions(queens, j, nd, pd) > 0)
                if b:
                    swap(queens, i, j, nd, pd)
                    it += 1
                else:
                    break


def final_search_reduced(queens, k, nd, pd):
    n = len(queens)
    for i in range(n - k, n):
        if total_collisions(queens, i, nd, pd) > 0:
            for j in range(n):
                swap(queens, i, j, nd, pd)
                b = (total_collisions(queens, i, nd, pd) > 0) or (total_collisions(queens, j, nd, pd) > 0)
                if b:
                    swap(queens, i, j, nd, pd)
                else:
                    break


# auxiliary functions
def initialize_diagonal_arrays(n):
    neg_diagonal = [0] * (2 * n - 1)
    pos_diagonal = [0] * (2 * n - 1)
    return neg_diagonal, pos_diagonal


def update_diagonal_arrays(queens, neg_diagonal, pos_diagonal):
    n = len(queens)
    for i in range(len(queens)):
        neg_diagonal[i + queens[i]] += 1
        pos_diagonal[i - queens[i] + n - 1] += 1


def swap(queens, a, b, neg_diagonal, pos_diagonal):
    original_a, original_b = queens[a], queens[b]
    queens[a], queens[b] = queens[b], queens[a]

    neg_diagonal[a + original_a] -= 1
    neg_diagonal[b + original_b] -= 1
    pos_diagonal[a - original_a + len(queens) - 1] -= 1
    pos_diagonal[b - original_b + len(queens) - 1] -= 1

    neg_diagonal[a + queens[a]] += 1
    neg_diagonal[b + queens[b]] += 1
    pos_diagonal[a - queens[a] + len(queens) - 1] += 1
    pos_diagonal[b - queens[b] + len(queens) - 1] += 1


def partial_collision(queens, i):
    return sum(1 for j in range(i) if (i - j) == abs(queens[i] - queens[j]))


def total_collisions(queens, i, neg_diagonal, pos_diagonal):
    n = len(queens)
    return neg_diagonal[i + queens[i]] + pos_diagonal[i - queens[i] + n - 1] - 2  # Exclude self-collision


def board_collision(queens):
    return sum(partial_collision(queens, i) for i in range(len(queens)))


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
             loc='center', colWidths=[0.3, 0.3])
    ax.axis('off')
    fig = plt.gcf()
    plt.title("Exectution Time for Powers of 10")
    plt.show()
    fig.savefig("test_table", bbox_inches='tight')


if __name__ == '__main__':
    while True:
        x = input("Inserisci dimensione scacchiera o digitare 'test' per misurare tempi di esecuzione "
                  "sulle potenze di 10:")
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
                print("Soluzione: " + str(queens))
                print("Tempo di esecuzione: " + str(end - start))
