import dbmaster

params = {
    'name': 'Qna-Mariq',
    'family': 'Verihovska',
    'num': '20302',
    'town': 'Varna',
    'gender': 'M',
    'room': '403',
    'birthDate': '2006-04-24',
    'score': '4.30'
}

obj = dbmaster.open('database')
obj.insert(params)