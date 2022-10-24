# Version 2.0

import io, os

class main:

    def __init__(self, fileName, arrangement='', spaceFill=''):
        self.fileName = fileName

        if arrangement == '': # Check if user tries to load or create database and if file with fileName already exists
            if os.path.exists(self.fileName):
                with open(fileName, 'r', encoding='utf-8') as file:
                    self.arrangement = file.readline() # Needs to be recoded so it can read database if it is a single line
            else:
                raise Exception('Trying to create empty database')
        else:
            if os.path.exists(self.fileName):
                raise Exception('Giving create argument/s wilst a file with this name already exists')
            else:
                self.arrangement = arrangement
                with open(self.fileName, 'w', encoding='utf-8') as file:
                    file.write(len(str(self.arrangement)) + str(self.arrangement) + "{'spaceFill':'" + spaceFill + "'}")
    





















    def insertOld(fileName, toInsert, spaceFill): # Database insertion method
    
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
