x=2

def myfunc():
    global x
    x = 5
    print(x)

myfunc()

print(x)