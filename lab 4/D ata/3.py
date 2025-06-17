import datetime

x = datetime.datetime.now()

y=x.replace(microsecond=0)

print(y)