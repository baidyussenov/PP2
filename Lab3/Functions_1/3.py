def solve(numheads, numlegs):
    rabbits = numheads
    chickens = 0
    while(True):
        if(chickens * 2 + rabbits * 4 == numlegs):
            break
        chickens = chickens + 1
        rabbits = rabbits - 1
    return rabbits, chickens

print(solve(35, 94))