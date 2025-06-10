import filmdar
def solve(movies, cat):
    total = 0
    number_of_movies=0
    for x in movies:
        if x["category"]==cat:
            total += x["imdb"]
            number_of_movies += 1
    avg=total/number_of_movies
    print(avg)

cat=input()

solve(filmdar.movies, cat)