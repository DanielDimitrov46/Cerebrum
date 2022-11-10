import io, os, ast

def getDbs(): # Returns a list of all databases in the current directory
    Return = list(value[:value.find(".dbmd" if value.endswith(".dbmd") else ".dbmm")] for value in os.listdir() if value.endswith(".dbmd") or value.endswith(".dbmm"))
    Return = set(value for value in Return if Return.count(value) == 2)
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

        for key in toInsert: # Arguments checks
            if key not in self.arrangement.keys(): raise Exception("Dbmaster: Column <" + key + "> is not a valid column in this database")
            if len(toInsert[key]) > self.arrangement[key]: raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')
        for key in self.arrangement:
            if key not in toInsert: raise Exception("Dbmaster: Must include all columns() while inserting")

        write = ''
        for key in toInsert: # Converts insert dictionary argument into insertable string and inserts into database
            write += toInsert[key] + ("".join('~' for _ in range(self.arrangement[key]-len(toInsert[key]))))

        deletedList = self.getDeletedList()
        if deletedList: # If there is a deleted entry it can replace
            self.fileData.seek(deletedList[0] * self.entryLength)
            self.updateDeletedList(deletedList.pop(0))
        else: 
            self.fileData.seek(0, 2)
            self.numOfEntries += 1

        self.fileData.write(write) # Write the information

    def search(self, toSearch:dict) -> tuple: # Search in database

        for key in toSearch: # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('Dbmaster: <' + key + '> is not a valid column in <' + self.fileName + '>')

        found = []
        for entry in range(self.numOfEntries): # Searches entries for passed filter and gives matching entries
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
    
    def get(self, start:int = 0, end:int = '') -> dict: # Get specified entries between start and end
        if end == '': end = self.numOfEntries - 1
        if start >= self.numOfEntries or start < 0: raise Exception('Dbmaster: Start index is out of bounds')
        if end < 0: raise Exception('Dbmaster: End index is out of bounds')
        if end >= self.numOfEntries: end = self.numOfEntries - 1
        if end < start: raise Exception('Dbmaster: End index is smaller than start index')

        data = dict.fromkeys(self.arrangement, [])
        indexi = []
        for i in range(start, end+1): # For every entry specified in the calling of get()
            if i in self.getDeletedList(): continue # Don't include deleted entries
            self.fileData.seek(self.entryLength * i)
            for key in data:
                read = self.fileData.read(self.arrangement[key])
                toList = list(data[key])
                toList.append((read[:read.find(self.spaceFill)]) if read.count(self.spaceFill) else read)
                data[key] = toList
            indexi.append(i)
        return indexi, data

    def columns(self) -> list: # Returns a list of the columns names
        return list(self.arrangement.keys())

    def delete(self, index:int): # Delete an entry
        if index >= self.numOfEntries: raise Exception("Dbmaster: Index out of range whilst deleting entry")

        deletedList = self.getDeletedList() # Get the list of deleted entries from meta file

        if index in deletedList: raise Exception("Dbmaster: Entry already deleted")

        self.fileData.seek(self.entryLength * index) # Seek to correct entry
        self.fileData.write("".join('~' for _ in range(self.entryLength))) # Do the deletion

        deletedList.append(index) # Append deleted entry to deletedList
        self.updateDeletedList(deletedList) # Write deletedList to meta file
 
    def update(self, index:int, params:dict): # Update an entry

        for key in params: # Arguments checks
            if key not in self.arrangement.keys(): raise Exception("Dbmaster: Column <" + key + "> is not a valid column in this database")
            if len(params[key]) > self.arrangement[key]: raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')
        if index in self.getDeletedList(): raise Exception("Dbmaster: Cannot update deleted entry")
        if index < 0 or  index >= self.numOfEntries: raise Exception("Dbmaster: Index out of bounds")

        for key in params:
            if len(key) > self.arrangement[key]: raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')
            columnOffset = 0 # Calculate where in each entry it needs to start reading
            for i in self.arrangement:
                if i == key:
                    break
                columnOffset += self.arrangement[i]
            self.fileData.seek(self.entryLength * index + columnOffset) # Seek to the correct position
            self.fileData.write(params[key] + ("".join('~' for _ in range(self.arrangement[key]-len(params[key])))))

    def getDeletedList(self) -> list:
        self.fileMeta.seek(self.deletedStart)
        deletedList = ""
        while True: # Gets deleted entries as string
            i = self.fileMeta.read(1)
            deletedList += i
            if i == ']':
                break
        deletedList = ast.literal_eval(deletedList) # Parses it to a list
        return deletedList

    def updateDeletedList(self, deletedList:list):
        self.fileMeta.seek(self.deletedStart) 
        self.fileMeta.write(str(deletedList)) # Update the list of deleted entries

    def close(self): # Should close everything needed to be closed
        self.fileData.close()
        self.fileMeta.close()
        del self

    def __enter__(self): # Support for "with" expression
        return self

    def __exit__(self, type, value, traceback): # Support for "with" expression
        self.close()