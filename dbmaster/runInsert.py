import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

params = {
    'name': input(),
    'family': input(),
    'num': input(),
    'town': input(),
    'G' : input(),
    'rUm' : input(),
    'birthDate' : input(),
    'scor' : input()
}

f = dbmaster.open('db.txt')
f.insert(params)