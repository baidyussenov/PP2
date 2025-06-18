import re

snake = "test_string_for_snake_case"
parts = snake.split("_")  
camel = parts[0] + "".join(p.title() for p in parts[1:])
print(camel)