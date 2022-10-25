import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

params = {
    'name': 15,
    'family': 20,
    'num': 5,
    'town': 20,
    'G' : 1,
    'rUm' : 3,
    'birthDate' : 10,
    'scor' : 4
}

f = dbmaster.open('db.txt', params, '~')