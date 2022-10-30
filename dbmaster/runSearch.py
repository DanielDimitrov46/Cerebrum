import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

params = {
    'town': 'Pravets'
    , 'name': 'Pesho'
}

f = dbmaster.open('db.txt')
print(f.search(params))