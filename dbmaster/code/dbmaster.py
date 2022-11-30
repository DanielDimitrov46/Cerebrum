import io, os, sys, ast
os.chdir(os.path.dirname(os.path.dirname(__file__))) # Optional. Sets directory to be a folder one up

def getDbs() -> list: # Returns a list of all databases in the current directory
    Return = list(value[:value.find(".dbmd" if value.endswith(".dbmd") else ".dbmm")] for value in os.listdir() if value.endswith(".dbmd") or value.endswith(".dbmm"))
    Return = list(set(value for value in Return if Return.count(value) == 2))
    return Return   

class open(object):
        
    def __init__(self, fileName:str, arrangement:dict=None, spaceFill:chr='~'):

        if arrangement == None: # Check if user tries to load or create database and if file with fileName already exists

            if os.path.exists(fileName + ".dbmd"): # If data file exists
                if os.path.exists(fileName + ".dbmm"): # Load
                    self.fileData = io.open(fileName + ".dbmd", "r+", encoding='utf-8') # Open data file
                    self.fileMeta = io.open(fileName + ".dbmm", "r+", encoding='utf-8') # Open meta file
                    self.spaceFill = self.fileMeta.read(1)
                    self.arrangement = ast.literal_eval(self.fileMeta.read(os.stat(fileName + ".dbmm").st_size-1)) # Parses it to dictionary
                    
                else: raise Exception("Dbmaster: Meta file with such name doesn't exit")
            else: raise Exception("Dbmaster: Data file with such name doesn't exit")

        else:
            if os.path.exists(fileName + ".dbmd") or os.path.exists(fileName + ".dbmm"):
                raise Exception('Dbmaster: Giving formatting arguments wilst a file/s with this name already exists')

            else: # New database
                if fileName == '': raise Exception("Dbmaster: Name can't be empty")
                try: self.arrangement = dict(arrangement)
                except: raise Exception("Dbmaster: Invalid create arguments")
                if len(spaceFill) != 1: raise Exception("Dbmaster: Invalid filler byte")
                self.spaceFill = spaceFill
                self.fileData = io.open(fileName + ".dbmd", "w+", encoding='utf-8') # Create data file
                self.fileMeta = io.open(fileName + ".dbmm", "w+", encoding='utf-8') # Create meta file
                self.fileMeta.write(self.spaceFill + str(self.arrangement)) # Write database formatting to meta file
        
        self.entryLength = sum(i for i in self.arrangement.values()) + 1 # Get length of one entry. Plus 1 for the <active> column
        self.numOfEntries = int(os.stat(fileName + ".dbmd").st_size / self.entryLength) # Get number of entries 
        if (os.stat(fileName + ".dbmd").st_size / self.entryLength) % 1 != 0: raise Exception('Dbmaster: Data is corrupt') # Check if database is corrupt by deviding all of the entries's length by the length of a non-corrupt entry

    def insert(self, toInsert:dict): # Insert to database

        for key in toInsert: # Arguments checks
            if key not in self.arrangement: raise Exception("Dbmaster: Column <" + key + "> is not a valid column in this database")
        for key in self.arrangement:
            if key not in toInsert: raise Exception("Dbmaster: Must include all columns() while inserting")

        write = ''
        for key in self.arrangement: # Converts insert dictionary argument into insertable string and inserts into database
            write += toInsert[key] + ("".join(self.spaceFill for _ in range(self.arrangement[key]-len(toInsert[key]))))

        self.fileData.seek(0,2)
        self.fileData.write("1" + write)
        self.entryLength += 1

    def search(self, toSearch:dict) -> tuple: # Search in database

        for key in toSearch: # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('Dbmaster: <' + key + '> is not a valid column in the database')

        found = []
        for entry in range(self.numOfEntries): # Searches entries for passed filter and gives matching entries
            
            self.fileData.seek(self.entryLength * entry) # \
            if self.fileData.read(1) == "0": continue    #  Check if entry is deleted. If so, skip it.

            try:
                for key in toSearch:
                    columnOffset = 0 # Calculate where in each entry it needs to start reading
                    for i in self.arrangement:
                        if i == key:
                            break
                        columnOffset += self.arrangement[i]
                    self.fileData.seek(self.entryLength * entry + 1 + columnOffset)
                    if not self.fileData.read(self.arrangement[key]).count(toSearch[key]):
                        raise Exception('genius way of breaking multiple loops')
            except:
                continue
            found.append(entry)

        result = dict.fromkeys(self.arrangement, [])
        for i in found:
            self.fileData.seek(self.entryLength * i + 1)
            for key in result:
                read = self.fileData.read(self.arrangement[key])
                toList = list(result[key])
                toList.append(read.strip(self.spaceFill))
                result[key] = toList

        return found, result
    
    def get(self, start:int = 0, end:int = None) -> dict: # Get specified entries startng at <start> and ending at <start + end>
        if end == None: end = start + 1; endSpecified = False
        else: end = start + end; endSpecified = True
        if start >= self.numOfEntries or start < 0: raise Exception('Dbmaster: Start index is out of bounds')
        if end < 0: raise Exception('Dbmaster: End index is out of bounds')
        if end >= self.numOfEntries: end = self.numOfEntries # Guarantees entries to display

        data = dict.fromkeys(self.arrangement, [])
        indexes, i = [], start

        while i < end: # For every entry specified in the calling of get()
            self.fileData.seek(self.entryLength * i)
            if self.fileData.read(1) == "0": # Don't include deleted entries
                end += (1 if end + 1 <= self.numOfEntries and endSpecified else 0)
                i += 1
                continue
            for key in data:
                read = self.fileData.read(self.arrangement[key])
                toList = list(data[key])
                toList.append(read.strip(self.spaceFill))
                data[key] = toList
            indexes.append(i)
            i += 1

        return indexes, data

    def columns(self) -> list: # Returns a list of the columns names
        return list(self.arrangement.keys())

    def delete(self, index:int): # Delete an entry
        if index >= self.numOfEntries: raise Exception("Dbmaster: Index out of range whilst deleting entry")
        self.fileData.seek(self.entryLength * index)
        if self.fileData.read(1) == "0": raise Exception("Dbmaster: Entry already deleted")
        else: self.fileData.seek(self.entryLength * index); self.fileData.write("0")

    def phoenix(self, index:int): # Bring back an entry
        if index >= self.numOfEntries: raise Exception("Dbmaster: Index out of range whilst deleting entry")
        self.fileData.seek(self.entryLength * index)
        if self.fileData.read(1) == "1": raise Exception("Dbmaster: Entry isn't deleted")
        else: self.fileData.seek(self.entryLength * index); self.fileData.write("1")
 
    def update(self, index:int, params:dict): # Update an entry

        for key in params: # Arguments checks
            if key not in self.arrangement.keys(): raise Exception("Dbmaster: Column <" + key + "> is not a valid column in this database")
            if len(params[key]) > self.arrangement[key]: raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')
        self.fileData.seek(self.entryLength * index)
        if self.fileData.read(1) == "0": raise Exception("Dbmaster: Cannot update deleted entry")
        if index < 0 or  index >= self.numOfEntries: raise Exception("Dbmaster: Index out of bounds")

        for key in params:
            if len(key) > self.arrangement[key]: raise Exception('Dbmaster: Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')
            columnOffset = 0 # Calculate where in each entry it needs to start reading
            for i in self.arrangement:
                if i == key:
                    break
                columnOffset += self.arrangement[i]
            self.fileData.seek(self.entryLength * index + columnOffset) # Seek to the correct position
            self.fileData.write(params[key] + ("".join(self.spaceFill for _ in range(self.arrangement[key]-len(params[key])))))

    def close(self): # Should close everything needed to be closed
        self.fileData.close()
        self.fileMeta.close()
        del self

    def __enter__(self): # Support for "with" expression
        return self

    def __exit__(self, type, value, traceback): # Support for "with" expression
        self.close()