# Version 1.0

import io

class main:


    def create(fileName, arrangement, spaceFill): # Database creation method

        try: # Tries to create the file. If file already exists, throws exception.
            file = open(fileName, 'x')
            file.close()
        except:
            raise Exception('File with fileName ' + fileName + ' already exists')

        write = '' # Converts creation parameters to string and writes them to the database file.
        for key in arrangement:
            if len(key) > arrangement[key]:
                raise Exception('Length of column <' + key + '> is larger than the specified size of ' + arrangement[key])
            write = write + key
            for i in range(arrangement[key]): # spaceFill writing
                write = write + spaceFill
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(write)
        
        
    def insert(fileName, toInsert, spaceFill): # Database insertion method

        with open(fileName, 'r', encoding='utf-8') as file: # Reads first line of the database file and converts it back to the creation parameters so checks can be done.
            read = file.readline()
        arrangement = read.split(spaceFill)
        arrangement[:] = (value for value in arrangement if value != '')
        arrangement = dict.fromkeys(arrangement, 0)
        for key in arrangement:
            arrangement[key] = len(read[read.find(key):(len(read)) if (list(arrangement).index(key) == len(arrangement)-1) else (str(read).find(list(arrangement)[list(arrangement).index(key)+1]))])-len(key)

        for key in toInsert: # Validates that insert info format is equal to database format
            if key != list(arrangement)[list(toInsert).index(key)]:
                raise Exception("Insert format doesn't match database format at <" + key + '>')
            if len(toInsert[key]) > arrangement[key]:
                raise Exception('Length of ' + key + ' is larger than the allowed size of ' + arrangement[key])

        write = '' # Converts insert dictionary into insertable string and inserts into database
        for key in toInsert:
            if len(toInsert[key]) > arrangement[key]:
                raise Exception('Value of <' + key + '> is larger than the allowed size of ' + arrangement[key])
            write = write + toInsert[key]
            for i in range(arrangement[key] - len(toInsert[key]) + len(key)): # spaceFill writing
                write = write + spaceFill
        with open(fileName, 'a', encoding='utf-8') as file:
            file.write('\n' + write)