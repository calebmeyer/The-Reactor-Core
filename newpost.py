import os
import re
from inflection import parameterize # inflection library is from pip
from textwrap import dedent
from datetime import datetime


files = os.listdir('source/posts/')
files = [file for file in files if file.endswith('.md') and file is not None]

latest = 0
pattern = re.compile(r'\d+')
for file in files:
    match = pattern.match(file)
    if match is None:
        continue
    number = int(match.group())
    latest = max(latest, number)

print('Enter new blog title: ', end='')
title = input()

filename = f'source/posts/{latest + 1}-{parameterize(title)}.md'
page_title = f'{latest + 1} - {title}'
date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

with open(filename, 'w') as file:
    text = f'''
        ---
        date: {date}
        pageTitle: {page_title}
        tags: posts
        ---
    '''
    file.write(dedent(text).strip())
