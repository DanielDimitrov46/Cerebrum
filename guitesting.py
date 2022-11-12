
params = {
    'name': "",
    'family': "",
    'num': "",
    'town': "",
    'G': "",
    'rUm': "",
    'birthDate': "",
    'scor': ""
}

print(params.keys())

text = "1,2,3,4,5,6,7,8"
l=text.split(",")
index = 0

for i in params.keys():
    params[i] = l[index]
    index += 1
    print(params[i])
