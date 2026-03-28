import pandas as pd
from tqdm import tqdm

line_numbers = []
with open('./parsons/parsons_codes.txt','r') as f:
    counter = 0
    for line in f.readlines():
        counter += 1
        if line.startswith('ps_'):
              line_numbers.append(counter)
    
with open('./parsons/parsons_codes.txt','r') as f:
    lines = f.readlines()
    for ind in tqdm(range(0,len(line_numbers))):
        line_number = line_numbers[ind]-1
        code_filename = lines[line_number]
        code  = lines[line_number+2:line_numbers[ind+1]-2] if ind+1 < len(line_numbers) else lines[line_number+2:]

        with open(f'./parsons/{code_filename.strip()}.py','w+') as f:
            for line in code:
                f.write(line)



quizpet_codes = pd.read_csv('./quizpet/quizpet_codes.csv')


for row, ind in tqdm(quizpet_codes.iterrows()):
    code = ind['code']
    code_filename = ind['rdfID']
    with open(f'./quizpet/{code_filename}.py','w+') as f:
        f.write(code)