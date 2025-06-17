def even_numbers_generator(n):
    for num in range(0, n + 1, 2):
        yield str(num)  

n = int(input())
even_numbers = even_numbers_generator(n)
print(", ".join(even_numbers))