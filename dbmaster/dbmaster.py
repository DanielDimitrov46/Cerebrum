# Version 2.0
# Lines 18-24 needs beauty recoding

import io, os, ast

class main(object):



    def __init__(self):
        self = self
            


<<<<<<< Updated upstream
    def create(fileName, arrangement, spaceFill): # Create database

        if os.path.exists(fileName):
            raise Exception('Giving create argument/s wilst a file with this name already exists')
        else:
            with io.open(fileName, 'w', encoding='utf-8') as file:
                file.write(spaceFill + str(len(str(arrangement))) + str(arrangement))


        
    def load(self, fileName): # Load database
=======
    def __init__(self, fileName, arrangement='', spaceFill='`'):
>>>>>>> Stashed changes

        self.fileName = fileName

        if os.path.exists(self.fileName):
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
<<<<<<< Updated upstream
                file.close()  
        else:
            raise Exception('No such file exists')
=======
                file.close()
                
            else:
                raise Exception("Dbmaster: Can't create database without formatting arguments")
        else:
            if os.path.exists(self.fileName):
                raise Exception('Dbmaster: Giving create argument/s wilst a file with this name already exists')
            else: # New database
                if fileName == '':
                    raise Exception("Dbmaster: Database name can't be empty")
                self.arrangement = arrangement
                self.spaceFill = spaceFill
                with io.open(self.fileName, 'w', encoding='utf-8') as file:
                    file.write(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement))
        
        self.start = len(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement))
>>>>>>> Stashed changes
    


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
<<<<<<< Updated upstream
        with open(self.fileName, 'a', encoding='utf-8') as file:
            file.write('\n' + write)
=======

        with io.open(self.fileName, 'a', encoding='utf-8') as file:
            file.write(write)




    def search(self, toSearch): # Search in database

        file = io.open(self.fileName, 'r', encoding='utf-8') # Open file for further use

        for key in toSearch: # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('Dbmaster: <' + key + '> is not a valid column in <' + self.fileName + '>')

        entryLength = sum(i for i in self.arrangement.values()) # Get length of one entry

        if ((os.stat(self.fileName).st_size - self.start) / entryLength) % 1 != 0: # Check if database is corrupt by deviding all of the entries's length by the length of a non-corrupt entry
            raise Exception('Dbmaster: Database is corrupt')


        found = [] # Searches entries for passed filter and gives matching entries
        for entry in range(int((os.stat(self.fileName).st_size - self.start) / entryLength)):

            try:
                for key in toSearch:

                    columnOffset = 0 # Calculate where in each entry it needs to start reading
                    for i in self.arrangement:
                        if i == key:
                            break
                        columnOffset += self.arrangement[i]

                    file.seek(self.start + (entryLength * entry) + columnOffset) 
                    if not file.read(self.arrangement[key]).count(toSearch[key]):
                        raise Exception('genius way of breaking multiple loops')
            except:
                continue
            found.append(entry)

        result = dict.fromkeys(self.arrangement, [])
        for i in found:
            file.seek(self.start + (entryLength * i))
            for key in result:
                read = file.read(self.arrangement[key])
                toList = list(result[key])
                toList.append(read[:read.find(self.spaceFill)])
                result[key] = toList
        return result   



    def infoColumns(self):
        return self.arrangement.keys()
>>>>>>> Stashed changes
