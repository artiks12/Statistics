import json
import os
from os import listdir
from os.path import isfile, join
import re
from pyquery import PyQuery as pq
from transformers import AutoTokenizer

def GetAnswerWordCounts(path):
    tokenizer = AutoTokenizer.from_pretrained("utter-project/EuroLLM-9B-Instruct")

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    answers = []
    for file in onlyfiles:
        fullPath = path + '/' + file
        with open(fullPath, encoding='utf-8') as f:
            entries: list = json.load(f)

        for entry in entries:
            answer = re.sub(r'(\n)+', ' ', pq(entry['Saturi'][1]['Saturs']).text())
            tokens = tokenizer.tokenize(answer)
            answers.append({
                'text':answer,
                'token_count':len(tokens)
            })
    answers.sort(key=lambda a: a['token_count'])

    with open('AnswerWordCounts.json', 'wt', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

def GetAnswerWordCountStats(file='AnswerWordCounts.json'):
    with open(file, encoding='utf-8') as f:
        answers: list = json.load(f)

    print('3 smallest texts:',[answer['token_count'] for answer in answers[0:3]])

    count = len(answers)
    if count % 2 == 0:
        half_right = count // 2
        half_left = half_right - 1

        median = (answers[half_left]['token_count'] + answers[half_right]['token_count'])/2
        print('Token median:',median)
    else: print('Token median:',answers[(count-1)//2]['token_count'])

    print('Token average:',round(sum([answer['token_count'] for answer in answers])/count,0)) # average

    for c in range(len(answers)):
        if answers[c]['token_count'] > 8192:
            print(c,'out of',len(answers),'have less than 2048 tokens.')
            print(round(c/len(answers),4),'percent of all answers.')
            break

    groups = {
        '500':0,
        '1000':0,
        '1500':0,
        '2000':0,
        '2500':0,
        '3000':0,
        '3500':0,
        '4000':0,
        '>4000':0,
    }
    for c in range(len(answers)):
        if answers[c]['token_count'] <= 500: groups['500'] += 1
        elif answers[c]['token_count'] <= 1000: groups['1000'] += 1
        elif answers[c]['token_count'] <= 1500: groups['1500'] += 1
        elif answers[c]['token_count'] <= 2000: groups['2000'] += 1
        elif answers[c]['token_count'] <= 2500: groups['2500'] += 1
        elif answers[c]['token_count'] <= 3000: groups['3000'] += 1
        elif answers[c]['token_count'] <= 3500: groups['3500'] += 1
        elif answers[c]['token_count'] <= 4000: groups['4000'] += 1
        else: groups['>4000'] += 1

    print(groups)

if __name__ == '__main__':
    GetAnswerWordCounts('lvportals')
    GetAnswerWordCountStats()