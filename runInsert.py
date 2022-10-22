import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

params = {
    'name': 'Pesho',
    'family': 'Goshev',
    'num': '20601',
    'town': 'Pravets',
    'G' : 'M',
    'rUm' : '401',
    'birthDate' : '2006-01-24',
    'scor' : '5.31'
}

test = dbmaster.main
test.insert('db.txt', params, '~')