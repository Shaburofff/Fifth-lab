# # Вариант 33. IT-предприятие набирает сотрудников: 2 мидла, 2 синьера, 2 юниора. Сформировать все возможные варианты заполнения вакантных мест, если имеются 7 претендентов.
#2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов)
# и целевую функцию для нахождения оптимального  решения.
import random
from itertools import combinations

candidates = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
total_variants = 630

# генерация случайных оценок для целевой функции
scores = {c: random.randint(50, 100) for c in candidates}

# параметры фильтрации
allowed_unused = random.sample(candidates, 3)   # допустимые «один неиспользованный»
mid_thr = random.randint(130, 160)      # порог по сумме score мидлов
sr_thr = random.randint(130, 160)      # порог по сумме score синьёров

# понятный вывод условий фильтрации
print("Условия фильтрации:")
print(f" Единственный неиспользованный кандидат должен быть одним из: {allowed_unused}")
print(f"  Минимально допустимая суммарная оценка двух мидлов: {mid_thr}")
print(f" Минимально допустимая суммарная оценка двух синьёров: {sr_thr}\n")

def generate_pruned(cands, scores, allowed_unused, mid_thr, sr_thr):
    result = []
    # 1) Выбираем мидлов и сразу проверяем их порог
    for mids in combinations(cands, 2):
        mids_score = scores[mids[0]] + scores[mids[1]]
        if mids_score < mid_thr:
            continue
        rem1 = [c for c in cands if c not in mids]

        # 2) выбираем синьёров и сразу проверяем их порог
        for srs in combinations(rem1, 2):
            srs_score = scores[srs[0]] + scores[srs[1]]
            if srs_score < sr_thr:
                continue
            rem2 = [c for c in rem1 if c not in srs]

            # 3) выбираем джуниоров и сразу проверяем условие по единственному неиспользованному
            for jrs in combinations(rem2, 2):
                unused = (set(rem2) - set(jrs)).pop()
                if unused not in allowed_unused:
                    continue

                # 4) всё прошло — считаем total_score и сохраняем
                jrs_score   = scores[jrs[0]] + scores[jrs[1]]
                total_score = mids_score + srs_score + jrs_score
                result.append((mids, srs, jrs, total_score))
    return result

# генерация вариантов по условиям
filtered = generate_pruned(candidates, scores, allowed_unused, mid_thr, sr_thr)
filtered_count = len(filtered)
reduction = total_variants - filtered_count

print(f"Всего вариантов без ограничений: {total_variants}")
print(f"Вариантов после «прореживания»: {filtered_count} (сокращено на {reduction})\n")

# первые 10 возможных вариантов после прореживания
print("Первые 10 возможных вариантов после прореживания (total_score):")
for mids, srs, jrs, ts in filtered[:10]:
    print(f"  mids={mids} srs={srs} jrs={jrs} total_score={ts}")
print()

seen = set()
unique = []
for mids, srs, jrs, ts in filtered:
    if ts not in seen:
        unique.append((mids, srs, jrs, ts))
        seen.add(ts)

print(f"Количество уникальных вариантов: {len(unique)}\n")

print("Первые 10 уникальных вариантов (total_score):")
for mids, srs, jrs, ts in unique[:10]:
    print(f"  mids={mids} srs={srs} jrs={jrs} total_score={ts}")
print()

# выбираем лучший по total_score
best = max(unique, key=lambda x: x[3]) if unique else None
if best:
    mids, srs, jrs, ts = best
    print(f"Лучший вариант: mids={mids} srs={srs} jrs={jrs} total_score={ts}")
else:
    print("Лучший вариант не найден")
