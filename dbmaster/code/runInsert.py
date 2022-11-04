import dbmaster

params = {
    'name': 'Goshko',
    'family': 'Petrov',
    'num': '20105',
    'town': 'Mezdra',
    'G': 'M',
    'rUm': '408',
    'birthDate': '2006-04-24',
    'scor': '5.10'
}

obj = dbmaster.open('database')
obj.insert(params)