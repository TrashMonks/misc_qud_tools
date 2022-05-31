from random import randint
import os

def get_num_psychic_hunters(glimmer: int):
    roll = randint(1, 1000)
    num_hunters = 0
    if glimmer < 20:
        return 0
    if 20 <= glimmer <= 49:
        if roll >= (glimmer - 20 + 15) * 2:
            return 0
    else:
        if roll >= (glimmer - 40 + 105) * 0.666:
            return 0

    num_hunters += 1
    if glimmer >= 35 and num_hunters > 0:
        if randint(1, 1000) >= (glimmer - 20) * 5:
            return num_hunters
        num_hunters += 1

    if glimmer >= 50 and randint(1, 1000) < (glimmer - 20) * 5:
        num_hunters += 1
        if randint(1, 1000) >= (glimmer - 20) * 5:
            return num_hunters
        num_hunters += 1
        if glimmer >= 80 and randint(1, 1000) < (glimmer - 50) * 5:
            num_hunters += 1
    return num_hunters


results = {}
trials = 100000
for trial in range(0, trials):
    for i in range(0, 200, 20):
        if i not in results:
            results[i] = {}
        for num in range(6):
            if num not in results[i]:
                results[i][num] = 0
        num = get_num_psychic_hunters(i)
        results[i][num] += 1
print(results)
glimmer_table = """
{|class="wikitable"
!Glimmer
!0 Hunters
!1 Hunter
!2 Hunters
!3 Hunters
!4 Hunters
!5 Hunters
|-"""
for glimmer, counts in results.items():
    glimmer_table += f'\n|-\n|{glimmer}'
    for num_hunters, count in counts.items():
        glimmer_table += f'\n|{count/trials:.2%}'
glimmer_table += "\n|}"
with open(os.path.join('Outputs', 'glimmer_stats.txt'), 'w') as file:
    file.write(glimmer_table)
print('Done')
