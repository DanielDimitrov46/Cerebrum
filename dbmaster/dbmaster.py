import io, os, ast


class open(object):



    def __init__(self, fileName, arrangement='', spaceFill=''):

        self.fileName = fileName

        if arrangement == '':  # Check if user tries to load or create database and if file with fileName already exists
            if os.path.exists(self.fileName):  # Load database
                file = io.open(self.fileName, 'r', encoding='utf-8')
                self.spaceFill = file.read(1)
                
                num, i = '', '' # Gets size of formatting
                while True:
                    i = file.read(1)
                    if i == '{':
                        file.seek(file.tell() - 1)
                        break
                    num += i

                self.arrangement = ast.literal_eval(file.read(int(num))) # Reads the formatting
                file.close()
            else:
                raise Exception("Dbmaster: Database needs formatting arguments when creating one")
        else:
            if os.path.exists(self.fileName):
                raise Exception('Dbmaster: Giving formatting arguments wilst a file with this name already exists')
            else:  # New database
                if self.fileName == '':
                    raise Exception("Dbmaster: Name can't be empty")
                self.arrangement = arrangement
                self.spaceFill = spaceFill
                with io.open(self.fileName, 'w', encoding='utf-8') as file:
                    file.write(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement))
        
        self.start = len(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement)) # Get start of database data (end of database formatting)
        self.entryLength = sum(i for i in self.arrangement.values()) # Get length of one entry
        self.numOfEntries = int((os.stat(self.fileName).st_size - self.start) / self.entryLength) # Get number of entries
        if ((os.stat(self.fileName).st_size - self.start) / self.entryLength) % 1 != 0: # Check if database is corrupt by deviding all of the entries's length by the length of a non-corrupt entry
            raise Exception('Dbmaster: Database is corrupt')



    def insert(self, toInsert):  # Insert to database

        for key in toInsert:  # Validates that insert argument format is equal to database format
            if key != list(self.arrangement)[list(toInsert).index(key)]:
                raise Exception("Dbmaster: Insert format doesn't match database format at <" + key + '>')
            if len(toInsert[key]) > self.arrangement[key]:
                raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + self.arrangement[key] + '>')

        write = ''  # Converts insert dictionary argument into insertable string and inserts into database
        for key in toInsert:

            write = write + toInsert[key]
            for i in range(self.arrangement[key] - len(toInsert[key])):  # spaceFill writing
                write = write + self.spaceFill

        with io.open(self.fileName, 'a', encoding='utf-8') as file:
            file.write(write)



    def search(self, toSearch): # Search in database

        file = io.open(self.fileName, 'r', encoding='utf-8') # Open file

        for key in toSearch: # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('Dbmaster: <' + key + '> is not a valid column in <' + self.fileName + '>')

        found = [] # Searches entries for passed filter and gives matching entries
        for entry in range(int((os.stat(self.fileName).st_size - self.start) / self.entryLength)):
            try:
                for key in toSearch:
                    columnOffset = 0 # Calculate where in each entry it needs to start reading
                    for i in self.arrangement:
                        if i == key:
                            break
                        columnOffset += self.arrangement[i]
                    file.seek(self.start + (self.entryLength * entry) + columnOffset)
                    if not file.read(self.arrangement[key]).count(toSearch[key]):
                        raise Exception('genius way of breaking multiple loops')
            except:
                continue
            found.append(entry)

        result = dict.fromkeys(self.arrangement, [])
        for i in found:
            file.seek(self.start + (self.entryLength * i))
            for key in result:
                read = file.read(self.arrangement[key])
                toList = list(result[key])
                toList.append((read[:read.find(self.spaceFill)]) if read.count(self.spaceFill) else read)
                result[key] = toList

        file.close()
        return result


    
    def get(self, start = 0, end = ''):
        if end == '': end = self.numOfEntries - 1
        if start >= self.numOfEntries or start < 0: raise Exception('Dbmaster: Start index is out of bounds')
        if end >= self.numOfEntries or start < 0: raise Exception('Dbmaster: End index is out of bounds')
        if end < start: raise Exception('Dbmaster: End index is smaller than start index')

        file = io.open(self.fileName, 'r', encoding='utf-8') # Open file
        data = dict.fromkeys(self.arrangement, [])
        for i in range(start, end+1): # For every entry specified in the calling of get()
            print(i)
            file.seek(self.start + (self.entryLength * i))
            for key in data:
                read = file.read(self.arrangement[key])
                toList = list(data[key])
                toList.append((read[:read.find(self.spaceFill)]) if read.count(self.spaceFill) else read)
                data[key] = toList

        file.close()
        return data

    def columns(self):
        return list(self.arrangement.keys())