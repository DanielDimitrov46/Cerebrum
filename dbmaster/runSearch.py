import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

params = {
    'town': 'Pravets'
}

f = dbmaster.open('db')
print(f.search(params))