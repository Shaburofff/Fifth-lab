# Вариант 33. IT-предприятие набирает сотрудников: 2 мидла, 2 синьера, 2 юниора. Сформировать все возможные варианты заполнения вакантных мест, если имеются 7 претендентов.
# Задание на л.р. №6 Задание состоит из двух частей. 
# 1 часть – написать программу в соответствии со своим вариантом задания. Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.

import timeit
from itertools import combinations

candidates = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def generate_algo(cands): # алг. метод
    result = []
    n = len(cands)
    for i in range(n):
        for j in range(i+1, n):
            mids = (cands[i], cands[j])
            rem1 = [x for x in cands if x not in mids]
            for k in range(len(rem1)):
                for l in range(k+1, len(rem1)):
                    srs = (rem1[k], rem1[l])
                    rem2 = [x for x in rem1 if x not in srs]
                    for m in range(len(rem2)):
                        for o in range(m+1, len(rem2)):
                            jrs = (rem2[m], rem2[o])
                            result.append((mids, srs, jrs))
    return result

def generate_itertools(cands): #метод через comb itertools
    return [
        (mids, srs, jrs)
        for mids in combinations(cands, 2)
        for srs in combinations([x for x in cands if x not in mids], 2)
        for jrs in combinations([x for x in cands if x not in mids and x not in srs], 2)
    ]

def main():
    algo_list = generate_algo(candidates)
    py_list = generate_itertools(candidates)
    print("Всего вариантов (алгоритм):", len(algo_list))
    print("Всего вариантов (itertools):", len(py_list))
    print("\nПервые 5 (алгоритм):")
    for combo in algo_list[:5]:
        print("  Мидлы =", combo[0], "; Сениоры =", combo[1], "; Джуниоры =", combo[2])
    print("\nПервые 5 (itertools):")
    for combo in py_list[:5]:
        print("  Мидлы =", combo[0], "; Сениоры =", combo[1], "; Джуниоры =", combo[2])
    runs = 1000
    t_alg = timeit.timeit(lambda: generate_algo(candidates), number=runs)
    t_py = timeit.timeit(lambda: generate_itertools(candidates), number=runs)
    print(f"\nВремя за {runs} запусков:")
    print(f"  Алгоритмический способ = {t_alg:.4f} s")
    print(f"  itertools.combinations = {t_py:.4f} s")
    if t_alg < t_py:
        print("\nРезультат: алгоритмический способ работает быстрее.")
    elif t_py < t_alg:
        print("\nРезультат: способ с itertools.combinations работает быстрее.")
    else:
        print("\nРезультат: оба способа работают с одинаковой скоростью.")

if __name__ == "__main__":
    main()
