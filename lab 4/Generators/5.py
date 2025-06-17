def Chisla(a,b):
    for num in range(a, b + 1):
        yield num

a = int(input("Ввидите чсило а: "))

b = int(input("Ввидите чсило b: "))


for numbers in Chisla(a,b):
    print(numbers, end=", ")