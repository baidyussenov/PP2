lst = [int(x) for x in input().split()]
def unique(lst):
    new_array = []
    for i in lst:
        if i not in new_array:
            new_array.append(i)
    print(new_array)
unique(lst)