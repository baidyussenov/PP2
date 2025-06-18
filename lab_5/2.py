import re

txt = "Примеры: abb, abbb, но не ab или abbbb"
matches = re.findall(r'ab{2,3}', txt)
print("Найдены:", matches)