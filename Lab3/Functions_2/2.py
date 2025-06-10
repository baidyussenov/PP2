import filmdar
def solve(movies):
    new_list = []
    for x in movies:
        if x["imdb"] > 5.5:
                new_list.append(x["name"])
    print(new_list)

solve(filmdar.movies)