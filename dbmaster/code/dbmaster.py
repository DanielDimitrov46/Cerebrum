import io, os, ast


def listDbs() -> list: # Returns a list of all databases in the current directory
    Return = []
    for file in os.listdir():
        if file.endswith(".dbm"):
            Return.append(file[:file.find(".dbm")])
    return Return



class open(object):



    def __init__(self, fileName:str, arrangement:dict='', spaceFill:chr='~'):

        if arrangement == '': # Check if user tries to load or create database and if file with fileName already exists

            if os.path.exists(fileName + ".dbmd"): # If data file exists
                if os.path.exists(fileName + ".dbmm"): # If meta file exists
                    self.fileData = io.open(fileName + ".dbmd", "r+", encoding='utf-8') # Open data file
                    self.fileMeta = io.open(fileName + ".dbmm", "r+", encoding='utf-8') # Open meta file
                    self.spaceFill = self.fileMeta.read(1)
                    self.arrangement = ''
                    while True: # Gets database formatting in string
                        i = self.fileMeta.read(1)
                        self.arrangement += i
                        if i == '}':
                            break
                        del i
                    self.arrangement = ast.literal_eval(self.arrangement) # Parses it to dictionary
                else: raise Exception("Dbmaster: Meta file with such name doesn't exit")
            else: raise Exception("Dbmaster: Data file with such name doesn't exit")

        else:
            if os.path.exists(fileName + ".dbmd") or os.path.exists(fileName + ".dbmm"):
                raise Exception('Dbmaster: Giving formatting arguments wilst a file/s with this name already exists')

            else: # New database
                if fileName == '': raise Exception("Dbmaster: Name can't be empty")
                try: self.arrangement = dict(arrangement)
                except: raise Exception("Dbmaster: Invalid create arguments")
                self.spaceFill = spaceFill
                self.fileData = io.open(fileName + ".dbmd", "w+", encoding='utf-8') # Create data file
                self.fileMeta = io.open(fileName + ".dbmm", "w+", encoding='utf-8') # Create meta file
                self.fileMeta.write(self.spaceFill + str(self.arrangement) + "[]") # Write database formatting to meta file
        
        self.entryLength = sum(i for i in self.arrangement.values()) # Get length of one entry
        self.numOfEntries = int(os.stat(fileName + ".dbmd").st_size / self.entryLength) # Get number of entries
        if (os.stat(fileName + ".dbmd").st_size / self.entryLength) % 1 != 0: # Check if database is corrupt by deviding all of the entries's length by the length of a non-corrupt entry
            raise Exception('Dbmaster: Data is corrupt')
        self.deletedStart = len(self.spaceFill + str(self.arrangement))



    def insert(self, toInsert:dict): # Insert to database

        for key in toInsert: # Validates that insert argument format is equal to database format
            if key != list(self.arrangement)[list(toInsert).index(key)]:
                raise Exception("Dbmaster: Insert format doesn't match database format at <" + key + '>')
            if len(toInsert[key]) > self.arrangement[key]:
                raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + self.arrangement[key] + '>')

        write = ''
        for key in toInsert: # Converts insert dictionary argument into insertable string and inserts into database
            write = write + toInsert[key]
            for _ in range(self.arrangement[key] - len(toInsert[key])): # spaceFill writing
                write = write + self.spaceFill

        self.fileData.seek(0, 2)
        self.fileData.write(write) # Write the information

        self.numOfEntries += 1



    def search(self, toSearch:dict) -> tuple: # Search in database

        for key in toSearch: # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('Dbmaster: <' + key + '> is not a valid column in <' + self.fileName + '>')

        found = [] # Searches entries for passed filter and gives matching entries
        for entry in range(self.numOfEntries):
            try:
                for key in toSearch:
                    columnOffset = 0 # Calculate where in each entry it needs to start reading
                    for i in self.arrangement:
                        if i == key:
                            break
                        columnOffset += self.arrangement[i]
                    self.fileData.seek(self.entryLength * entry + columnOffset)
                    if not self.fileData.read(self.arrangement[key]).count(toSearch[key]):
                        raise Exception('genius way of breaking multiple loops')
            except:
                continue
            found.append(entry)

        result = dict.fromkeys(self.arrangement, [])
        for i in found:
            self.fileData.seek(self.entryLength * i)
            for key in result:
                read = self.fileData.read(self.arrangement[key])
                toList = list(result[key])
                toList.append((read[:read.find(self.spaceFill)]) if read.count(self.spaceFill) else read)
                result[key] = toList

        return found, result


    
    def get(self, start:int = 0, end:int = '') -> dict:
        if end == '': end = self.numOfEntries - 1
        if start >= self.numOfEntries or start < 0: raise Exception('Dbmaster: Start index is out of bounds')
        if end >= self.numOfEntries or start < 0: raise Exception('Dbmaster: End index is out of bounds')
        if end < start: raise Exception('Dbmaster: End index is smaller than start index')

        data = dict.fromkeys(self.arrangement, [])
        for i in range(start, end+1): # For every entry specified in the calling of get()
            self.fileData.seek(self.entryLength * i)
            for key in data:
                read = self.fileData.read(self.arrangement[key])
                toList = list(data[key])
                toList.append((read[:read.find(self.spaceFill)]) if read.count(self.spaceFill) else read)
                data[key] = toList

        return data



    def columns(self) -> list: # Returns a list of the columns
        return list(self.arrangement.keys())



    def delete(self, index): # Delete an entry
        if index >= self.numOfEntries: raise Exception("Dbmaster: Index out of range whilst deleting entry")

        self.fileMeta.seek(self.deletedStart)
        deletedList = ""
        while True: # Gets deleted entries as string
            i = self.fileMeta.read(1)
            deletedList += i
            if i == ']':
                break
            del i
        deletedList = ast.literal_eval(deletedList) # Parses it to a list

        if index in deletedList: raise Exception("Dbmaster: Entry already deleted")

        self.fileData.seek(self.entryLength * index) # Seek to correct entry
        self.fileData.write("".join('~' for i in range(self.entryLength))) # Do the deletion

        deletedList.append(index)
        self.fileMeta.seek(self.deletedStart) 
        self.fileMeta.write(str(deletedList)) # Update the list of deleted entries



#
# Implement __del__ or whatever it is so your code can work with <with>
#



    def close(self):
        self.fileData.close()
        self.fileMeta.close()
        del self