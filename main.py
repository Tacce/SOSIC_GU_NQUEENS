import random


def queen_search(queens):
    k = initial_search(queens)
    final_search(queens, k)


def initial_search(queens):
    n = len(queens)
    for i in range(n):
        queens[i] = i
    j = 0

    # place queens without collisions
    for i in range(int(3.08 * n)):
        if j == n:
            break
        m = random.randint(j, n - 1)
        swap(queens, j, m)
        if partial_collision(queens, j) == 0:
            j = j + 1
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
                    it = it + 1
                else:
                    break


# auxiliary functions
def swap(queens, a, b):
    tmp = queens[a]
    queens[a] = queens[b]
    queens[b] = tmp


def partial_collision(queens, i):
    count = 0
    for j in range(i):
        if (i - j) == abs(queens[i] - queens[j]):
            count = count + 1
    return count


def total_collisions(queens, i):
    count = 0
    for j in range(len(queens)):
        if i != j and (abs(i - j) == abs(queens[i] - queens[j])):
            count = count + 1
    return count


def board_collision(queens):
    count = 0
    for i in range(len(queens)):
        count = count + partial_collision(queens, i)
    return count


size = 10000
queen = [0] * size
queen_search(queen)
print(queen)
print(board_collision(queen))
