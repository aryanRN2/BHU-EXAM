import os
import json
import re

# Since js/exams-data.js is a javascript file exporting a large object, let's read it and count entries.
# Let's see what keys it has or search for "EXAMS = {"
with open('js/exams-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We can count how many "title" fields are in this JS file to find the number of exams or how many items
titles = re.findall(r'"title":\s*"([^"]+)"', content)
print(f"Number of titles: {len(titles)}")

# Let's count how many questions are in js/exams-data.js.
# Questions are usually objects inside arrays, let's see how many occurrences of "question" key there are
questions = re.findall(r'"question":\s*"', content)
print(f"Number of questions in exams-data: {len(questions)}")
