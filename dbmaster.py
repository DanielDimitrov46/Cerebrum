# Version 1.0

import io

class main:


    def create(fileName, arrangement, spaceFill): # Db creation method
        try:
            file = open(fileName, 'x')
            file.close()
        except:
            raise Exception('File with fileName ' + fileName + ' already exists')
        write = ''
        for key in arrangement:
            if len(key) > arrangement[key]:
                raise Exception('Length of column <' + key + '> is larger than the specified size of ' + arrangement[key])
            write = write + key
            for i in range(arrangement[key] - len(key)+1):
                write = write + spaceFill
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(write)
        print('Database', fileName, 'with', len(arrangement), 'columns has been created')
        
        
    def insert(fileName, toInsert, spaceFill): # Db insertion method
        with open(fileName, 'r', encoding='utf-8') as file:
            read = file.readline()
        arrangement = read.split(spaceFill)
        arrangement[:] = (value for value in arrangement if value != '')
        arrangement = dict.fromkeys(arrangement, 0)
        for key in arrangement:
            arrangement[key] = len(read[read.find(key):(len(read)) if (list(arrangement).index(key) == len(arrangement)-1) else (str(read).find(list(arrangement)[list(arrangement).index(key)+1]))])-1

        write = ''
        for key in toInsert:
            if key != arrangement[list(arrangement)[list(toInsert).index(key)]]:
                raise Exception("Insert format doesn't match database format")
            if len(toInsert[key]) > arrangement[key]:
                raise Exception('Length of ' + key + ' is bigger than the specified size of ' + arrangement[key])

