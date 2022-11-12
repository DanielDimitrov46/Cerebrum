import dbmaster

params = {
    'name': 'Ganyo',
    'family': 'Petrov',
    'num': '20420',
    'town': 'Varna',
    'gender': 'M',
    'room': '403',
    'birthDate': '2006-04-24',
    'scor': '4.30'
}

obj = dbmaster.open('zaTedo')
obj.insert(params)