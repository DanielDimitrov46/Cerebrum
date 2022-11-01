import dbmaster, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

obj = dbmaster.open('databaseName')
