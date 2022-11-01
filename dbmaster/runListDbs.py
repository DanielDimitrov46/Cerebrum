import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(dbmaster.listDbs())
