import re

Upper_case = "Hello world Python is_cool a_b_c"

matches  =re.findall(r'\b[A-Z][a-z]*\b', Upper_case)

print("Найдено:", matches)