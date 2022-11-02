import dbmaster, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def search(column, parameter, name_of_database):
    params = {
        column: parameter,
        'rUm':'419'
    }

    f = dbmaster.open(f'{name_of_database}.txt')
    info = f.search(params)
    print(info)
    for key,value in info.items():
        print(f"{key}={value}")
    return info
