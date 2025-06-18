import re

def match_pattern(text):
    pattern = r'ab*'
    if re.fullmatch(pattern, text):
        return True
    else:
        return False
    
test_strings = ['a','ab', 'abb', 'ac', 'b', 'abc', 'aaa']

for s in test_strings:
    if match_pattern(s):
        print(f"Строка '{s}' соответсвует шаблону.")
    else:
        print(f"Строка '{s}' не соответствует шаблону.")