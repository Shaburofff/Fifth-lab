import timeit
from itertools import combinations

# Список из шести претендентов
candidates = ['A', 'B', 'C', 'D', 'E', 'F']

# Алгоритмический способ формирования вариантов:
def generate_algo(cands):
    result = []
    for mid_pair in combinations(cands, 2):
        rem1 = [c for c in cands if c not in mid_pair]
        for jun_pair in combinations(rem1, 2):
            result.append((mid_pair, jun_pair))
    return result

# Способ через itertools:
def generate_python(cands):
    return [
        (mids, juns)
        for mids in combinations(cands, 2)
        for juns in combinations([c for c in cands if c not in mids], 2)
    ]

salary = {'A': 50, 'B': 55, 'C': 45, 'D': 60, 'E': 40, 'F': 65}
skill  = {'A': 80, 'B': 85, 'C': 75, 'D': 90, 'E': 70, 'F': 95}
budget = 220

def filter_and_optimize(assignments):
    valid = []
    for mids, juns in assignments:
        total_sal = sum(salary[m] for m in mids) + sum(salary[j] for j in juns)
        if total_sal <= budget:
            valid.append((mids, juns, total_sal))
    best = []
    max_skill = -1
    for mids, juns, _ in valid:
        total_sk = sum(skill[m] for m in mids) + sum(skill[j] for j in juns)
        if total_sk > max_skill:
            max_skill = total_sk
            best = [(mids, juns)]
        elif total_sk == max_skill:
            best.append((mids, juns))
    return best, max_skill

def main():
    algo_list = generate_algo(candidates)
    py_list   = generate_python(candidates)

    print("Первые 5 (алгоритмический):")
    for mids, juns in algo_list[:5]:
        print(f"  Mids={mids}, Juniors={juns}")
    print("\nПервые 5 (Python/itertools):")
    for mids, juns in py_list[:5]:
        print(f"  Mids={mids}, Juniors={juns}")

    print(f"\nВсего вариантов: {len(py_list)}\n")

    t_alg = timeit.timeit(lambda: generate_algo(candidates), number=1000)
    t_py  = timeit.timeit(lambda: generate_python(candidates), number=1000)
    print(f"Скорость (1000 повторов): алгоритмический = {t_alg:.4f}s, python = {t_py:.4f}s\n")

    print(f"Ограничение: суммарная зарплата ≤ {budget}")
    print("Целевая функция: максимизация суммарного навыка\n")

    # Здесь вывод всех оптимальных вариантов
    best, max_skill = filter_and_optimize(py_list)
    print(f"Найдено допустимых вариантов с макс. навыком {max_skill}: {len(best)}\n")
    if best:
        print("Все оптимальные распределения:")
        for mids, juns in best:
            total_sal = sum(salary[x] for x in mids + juns)
            print(f"  Mids={mids}, Juniors={juns}, Salary={total_sal}, Skill={max_skill}")
    else:
        print("Нет вариантов, вписывающихся в бюджет.")

if __name__ == "__main__":
    main()
