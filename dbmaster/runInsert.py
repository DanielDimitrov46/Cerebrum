import dbmaster

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

obj = dbmaster.open('db')
obj.insert(params)

