import re

txt = "hello_world python_is_cool a_b_c"
matches  =re.findall(r'\b[a-z]+(?:_[a-z]+)+\b', txt)

print("Найдено:", matches)