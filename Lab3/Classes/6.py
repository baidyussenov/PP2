def is_prime(n):
    i = 2
    while i * i <= n:
        if (n % i == 0):
            return False
        i+=1
    return True


lst = [int(x) for x in input().split()]
new_list = list(filter(lambda x : (is_prime(x)), lst))
print(new_list)