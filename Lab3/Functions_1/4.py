nums=[int(x) for x in input().split()]
newarray = []
def is_prime(n):
    i = 2
    while i * i <= n:
        if (n % i == 0):
            return False
        i += 1
    return True

def filter_primes(nums):
    for i in range (len(nums)):
        if(is_prime(nums[i])):
            newarray.append(nums[i])

filter_primes(nums)
print(newarray)