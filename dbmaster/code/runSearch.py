import dbmaster

params = {
    'name':'Goshko',
    'town':'Mezdra'
}

obj = dbmaster.open('database')
print(obj.search(params))