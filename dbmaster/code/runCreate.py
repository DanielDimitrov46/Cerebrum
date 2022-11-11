import dbmaster

params = {
    'name': 15,
    'family': 20,
    'num': 5,
    'town': 20,
    'gender': 1,
    'room': 3,
    'birthDate': 10,
    'scor': 4
}

obj = dbmaster.open('databse', params, '*')