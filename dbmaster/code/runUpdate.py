import dbmaster

params = {
    'family':'Gorelski',
    'town': 'Sofia'
}

obj = dbmaster.open('database')
obj.update(0, params)