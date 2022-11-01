import dbmaster

params = {
    'name': 'Pesho',
    'family': 'Danchov',
    'num': '20601',
    'town': 'Pravets',
    'G' : 'M',
    'rUm' : '401',
    'birthDate' : '2006-01-24',
    'scor' : '5.31'
}

obj = dbmaster.open('db')
obj.insert(params)

