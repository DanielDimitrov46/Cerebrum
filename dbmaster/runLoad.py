import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

f = dbmaster.main
f. load(fileName ='db.txt')