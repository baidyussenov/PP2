import filmdar
def solve(movies, my_list):
    total = 0
    for x in movies:
         for y in my_list:
              if x["name"]==y:
                   total += x["imdb"]
    print(total/len(my_list))

my_list=["Usual Suspects", "Hitman", "Dark Knight", "The Help", "The Choice", "Colonia", "Love", "Bride Wars", "AlphaJet",
         "Ringing Crime", "Joking muck", "What is the name", "Detective", "Exam", "We Two"]

solve(filmdar.movies, my_list)