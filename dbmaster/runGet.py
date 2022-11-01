import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

f = dbmaster.open('db.txt')
info = f.get()
print(info)