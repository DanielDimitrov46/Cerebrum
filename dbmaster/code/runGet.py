import dbmaster

with dbmaster.open('database') as obj:
    print(obj.get(1,2))