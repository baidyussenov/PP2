def squares(n):
    for num in range(1, n + 1):
        yield num**2

N = int(input())
for square in squares(N):
    print(square, end=", ")