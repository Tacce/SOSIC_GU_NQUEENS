import random
import time
import matplotlib.pyplot as plt

MAX_POWER_10 = 7


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


def test():
    size = 1
    ex_time = [0] * MAX_POWER_10
    for i in range(MAX_POWER_10):
        size *= 10
        queens = [0] * size
        start = time.perf_counter()
        queen_search(queens)
        end = time.perf_counter()
        ex_time[i] = end - start
        print("n = 10^{} : {} s".format(i + 1, ex_time[i]))
    generateTable(ex_time)


def generateTable(ex_time):
    power = ["10^{}".format(i+1) for i in range(MAX_POWER_10)]
    fig, ax = plt.subplots()
    data = [[p, f"{et:.3f}"] for p, et in zip(power, ex_time)]
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
                queen_search(queens)
                print("Soluzione: " + str(queens))
