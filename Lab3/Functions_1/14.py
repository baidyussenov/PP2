array = [int(x) for x in input().split()]
new_array = []
def unique(array):
    for i in array:
        if i not in new_array:
            new_array.append(i)

unique(array)

def spy_game(nums):
    cnt = 0
    for i in range(len(nums)):
        if(nums[i] == 0):
            cnt = cnt + 1
        if(nums[i] == 7 and cnt >= 2):
            return True
    return False

print(spy_game(new_array))

