import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

name = input("Enter a database name:")
params = {
    'name': input("Enter a name:"),
    'family': input("Enter a family:"),
    'num': input("Enter a course number:"),
    'town': input("Enter a town:"),
    'G' : input("Enter a gender"),
    'rUm' : input("Enter a room:"),
    'birthDate' : input("Enter a birth date:"),
    'scor' : input("Enter average scor")
}

f = dbmaster.open(f'{name}.txt')
f.insert(params)