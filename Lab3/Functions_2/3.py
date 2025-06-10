import filmdar
def solve(movies, category_of_movies):
    new_list = []
    for x in movies:
            if x["category"] == category_of_movies:
                  new_list.append(x["name"])
    print(new_list)

category_of_movies=input()

solve(filmdar.movies, category_of_movies)