import math
import random
from functools import reduce


# something thrown together, can definitely be optimized
def calculate_fitness(board: list) -> int:
    total_score = 0
    for num, queen in enumerate(board):
        for comp_num, comp_queen in enumerate(board[num + 1:]):
            comp_num += num + 1
            if queen == comp_queen:
                total_score += 1
                continue

            #find diagonal attack
            index_dif = abs(num - comp_num)
            if queen > comp_queen and queen - index_dif == comp_queen:
                total_score += 1
            elif queen + index_dif == comp_queen:
                total_score += 1

    if total_score == 0:
        print(board)
        raise Exception('Done')
    # 28 is the maximum number of queens that can attack each other
    return 28 - total_score


def get_offspring(a, b):
    if len(a) != len(b):
        raise Exception('different lengths')

    cutoff = random.randint(1, len(a) - 1)
    # always inherit at least one column

    return [a[:cutoff] + b[cutoff:], b[:cutoff] + a[cutoff:]]


def mutate(gene, percent: float):
    max_int = len(gene)
    return [mutate_one_column(x, percent, max_int) for x in gene]


def mutate_one_column(num, percent, max_int):
    result = random.randint(0, 1000)
    new = num
    if percent > result / 1000:
        while new == num:
            new = random.randint(1, max_int)

    return new


def select_parents(fitness_set):

    parents = []
    cutoffs = [reduce(lambda x, y: x + y[1], fitness_set[:i], 0) for i in range(1, len(fitness_set) + 1)]
    total_fitness = cutoffs[-1]

    while len(parents) * 2 < len(fitness_set):
        selector = random.randint(0, total_fitness)
        first_parent_index = 0
        parent1 = None
        parent2 = None

        for num, cutoff in enumerate(cutoffs):
            if selector <= cutoff:
                parent1 = fitness_set[num][0]
                first_parent_index = num
                break

        second_parent_index = first_parent_index

        while second_parent_index == first_parent_index:
            selector = random.randint(0, total_fitness)
            for num, cutoff in enumerate(cutoffs):
                if selector <= cutoff:
                    parent2 = fitness_set[num][0]
                    second_parent_index = num
                    break

        parents.append((parent1, parent2))

    return parents


def run_algorithm(starting_set, mutate_percentage):
    if len(starting_set) % 2 != 0:
        raise Exception('Starting set not divisible by two')

    iterations = 0
    try:
        while True:
            with_fitness = [(parent, calculate_fitness(parent)) for parent in starting_set]
            parent_sets = select_parents(with_fitness)
            offspring = []
            for parent_set in parent_sets:
                # done twice
                offspring += get_offspring(parent_set[0], parent_set[1])

            # mutate
            starting_set = [mutate(x, mutate_percentage) for x in offspring]
            iterations += 1

    except Exception as e:
        return iterations

if __name__ == '__main__':

    start = [[2, 4, 7, 4, 8, 5, 5, 2], [3, 2, 7, 5, 2, 4, 1, 1],
             [2, 4, 4, 1, 5, 1, 2, 4], [3, 2, 5, 4, 3, 2, 1, 3]]

    percentages = [.01, .02, .04, .06, .08, .1, .12, .14, .16, .18, .2, .22, .24, .26, .28, .3, .35, .4, .5, .6, .7]
    runs = 20
    with open('log.txt', 'w') as log:
        log.write("Mutation Percentage,Avg Iterations\n")
        for percentage in percentages:
            iterations = []
            for _ in range(runs):
                iterations.append(run_algorithm(start, percentage))

            avg = reduce(lambda x, y: x + y, iterations) / runs
            log.write("{},{}\n".format(percentage, avg))
