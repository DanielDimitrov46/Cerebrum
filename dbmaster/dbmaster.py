# Version 2.0
# Line 15 needs beauty recoding

import io, os, ast

class open:

    def __init__(self, fileName, arrangement='', spaceFill=''):
        self.fileName = fileName

        if arrangement == '': # Check if user tries to load or create database and if file with fileName already exists
            if os.path.exists(self.fileName): # Load database
                file = io.open(self.fileName, 'r', encoding='utf-8')
                self.spaceFill = file.read(1)

                num, i = '', ''
                while True:
                    i = file.read(1)
                    if i == '{':
                        file.seek(file.tell() -1)
                        break
                    num += i

                self.arrangement = ast.literal_eval(file.read(int(num)))
                file.close()
                
            else:
                raise Exception('Trying to create empty database')
        else:
            if os.path.exists(self.fileName):
                raise Exception('Giving create argument/s wilst a file with this name already exists')
            else: # New database
                self.arrangement = arrangement
                self.spaceFill = spaceFill
                with io.open(self.fileName, 'w', encoding='utf-8') as file:
                    file.write(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement))
    

    def insert(self, toInsert):

        for key in toInsert: # Validates that insert info format is equal to database format
            if key != list(self.arrangement)[list(toInsert).index(key)]:
                raise Exception("Insert format doesn't match database format at <" + key + '>')
            if len(toInsert[key]) > self.arrangement[key]:
                raise Exception('Length of ' + key + ' is larger than the allowed size of ' + self.arrangement[key])

        write = '' # Converts insert dictionary into insertable string and inserts into database
        for key in toInsert:
            if len(toInsert[key]) > self.arrangement[key]:
                raise Exception('Value of <' + key + '> is larger than the allowed size of ' + self.arrangement[key])

            write = write + toInsert[key]
            for i in range(self.arrangement[key] - len(toInsert[key])): # spaceFill writing
                write = write + self.spaceFill

        with io.open(self.fileName, 'a', encoding='utf-8') as file:
            file.write('\n' + write)