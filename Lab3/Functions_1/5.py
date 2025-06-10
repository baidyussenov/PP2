from itertools import permutations
def all_permutations(word):
    perms = permutations(word)
    for i in list(perms):
        print(i)
word = input()
all_permutations(word)