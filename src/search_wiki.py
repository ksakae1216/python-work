# coding: utf-8

import sys
import re
import requests
import urllib.parse

from bs4 import BeautifulSoup

def get_wiki_data(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    return soup.select_one('.mw-parser-output').select_one('p').find_all('a', href=re.compile('(^/wiki/)'))

def get_link_list(row_data, word_list):
    global uniq_list
    global nest_level
    sub_list = []
    
    parser_outputsub = get_wiki_data(SEARCH_URL + row_data.get('href'))

    for row_sub in parser_outputsub:
        get_word_from_url = urllib.parse.unquote(row_sub.get('href'))[6:]

        if is_finish_word(get_word_from_url):
            sub_list.append([nest_level, get_word_from_url + '$'])
        elif get_word_from_url in uniq_list:
            sub_list.append([nest_level, get_word_from_url + '@'])
        else:
            sub_list.append([nest_level, get_word_from_url + '$'])
            uniq_list.append(get_word_from_url)

            if len(uniq_list) == MAX_SEARCH_CNT:
                break
    
    word_list.append(sub_list)

    cnt = 0
    for word in sub_list:

        if word[1][-2:] != '語$' and word[1][-2:] != '学$' and word[1][-1] != '@':

            if len(uniq_list) < MAX_SEARCH_CNT:
                nest_level +=1
                get_link_list(parser_outputsub[cnt], word_list[len(word_list)-1][cnt])

        cnt+=1

    nest_level -=1

def is_finish_word(get_word_from_url):
    end_word = get_word_from_url[-1]
    if end_word == '語' or end_word == '学':
        return True
    return False

def output_word_list(cnt, word_list):
    for i in range(len(word_list)):
        output_word(i, word_list[i])
    
def output_word(cnt, list):
    if type(list[0]) is int:
        print(get_indent(list[0]) + '- ' + list[1])
        if list[1][-2:] != '語$' and list[1][-2:] != '学$' and list[1][-1] != '@' and len(list) >= 3:
            output_word_list(cnt, list[2])
    else:
        output_word_list(cnt, list)

def get_indent(nest):
    indent = ''
    for i in range(nest*4):
        indent += ' '
    
    return indent


# Main処理
if len(sys.argv) != 2:
    print('【使い方】 python search_wiki.py 探索したいキーワード')
    exit()

word_list = []
uniq_list = []
sub_list = []
nest_level = 0
MAX_SEARCH_CNT = 20
SEARCH_URL = 'https://ja.wikipedia.org'
load_url = 'https://ja.wikipedia.org/wiki/' + sys.argv[1]

parser_output = get_wiki_data(load_url)

word_list.append([nest_level, sys.argv[1]])

nest_level += 1
for row in parser_output:
    get_word_from_url = urllib.parse.unquote(row.get('href'))[6:]

    if is_finish_word(get_word_from_url):
        sub_list.append([nest_level, get_word_from_url + '$'])
    elif get_word_from_url in uniq_list:
        sub_list.append([nest_level, get_word_from_url + '@'])
    else:
        sub_list.append([nest_level, get_word_from_url + '$'])
        uniq_list.append(get_word_from_url)

word_list.append(sub_list)

nest_level += 1
row_cnt = 0
for row in parser_output:
    get_word_from_url = urllib.parse.unquote(row.get('href'))[6:]

    if not is_finish_word(get_word_from_url) and len(uniq_list) < MAX_SEARCH_CNT:
        get_link_list(row, word_list[1][row_cnt])
    
    row_cnt += 1

output_word_list(0, word_list)