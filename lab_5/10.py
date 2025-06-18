import re
print(re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', input()).lower())
