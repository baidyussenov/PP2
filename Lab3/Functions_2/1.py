import filmdar
def solve(movies, name_of_movies):
    for x in movies:
            if x["name"] == name_of_movies:
                if x["imdb"] > 5.5:
                     return True
                else:
                     return False
    return False

name_of_movies=input()
print(solve(filmdar.movies, name_of_movies))