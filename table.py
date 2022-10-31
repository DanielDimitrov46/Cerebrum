from audioop import add
import io, os, ast
from typing import Dict, Any


class open(object):
    def __init__(self, fileName, arrangement=None, spaceFill='~'):
        if not arrangement:
            if os.path.exists(fileName):
                self.load(fileName)
            else:
                raise Exception('No such file')
        else:
            if os.path.exists(fileName):
                raise Exception('File already exists')
            else:  # New database
                self.create(fileName, arrangement, spaceFill)
                self.load(fileName)

    def create(self, fileName, arrangement, spaceFill):
        with io.open(fileName, 'w') as file:
            file.write(spaceFill + str(len(str(arrangement))) + str(arrangement))

    def load(self, fileName):
        self.fileName = fileName
        with io.open(self.fileName, 'r') as file:
            self.spaceFill = file.read(1)
            num, i = '', ''
            while True:
                i = file.read(1)
                if i == '{':
                    file.seek(file.tell() - 1)
                    break
                num += i
            self.arrangement = ast.literal_eval(file.read(int(num)))
            self.start = len(self.spaceFill + str(len(str(self.arrangement))) + str(self.arrangement))
        self.lineLength = 0
        for x in self.arrangement.values():
            self.lineLength += x;

    def insert(self, toInsert):  # Insert to database

        for key in toInsert.keys():  # Validates that insert argument format is equal to database format
            if not self.arrangement[key]:
                raise Exception("Insert format doesn't match database format at <" + key + '>')
            if len(toInsert[key]) > self.arrangement[key]:
                raise Exception(
                    'Length of <' + key + '> is larger than the allowed size of <' + str(self.arrangement[key]) + '>')

        write = ''  # Converts insert dictionary argument into insertable string and inserts into database
        for key in toInsert:
            write = write + toInsert[key]
            for i in range(self.arrangement[key] - len(toInsert[key])):  # spaceFill writing
                write = write + self.spaceFill

        with io.open(self.fileName, 'a') as file:
            file.write(write)

    def select(self, searchKey,compareKey=None):
        for key in searchKey:  # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('<' + key + '> is not a valid column in <' + self.fileName + '>')

        result: dict[Any, []] = {}
        for column in searchKey:
            result[column] = []

        with io.open(self.fileName, 'r') as file:
            file.seek(self.start)
            for i in range(500):
                for key in self.arrangement.keys():
                    element = file.read(self.arrangement[key]).replace("~", "")
                    if key in searchKey:
                        if not element == '':
                            result[key].append(element)
                        else:
                            break

        return result

    def select1(self, searchKey, compareKey=None):
        for key in searchKey:  # Check if search argument/s are valid
            if key not in self.arrangement:
                raise Exception('<' + key + '> is not a valid column in <' + self.fileName + '>')

        for key in compareKey:
            if key not in self.arrangement:
                raise Exception('<' + key + '> is not a valid column in <' + self.fileName + '>')

        result = list(list())
        result.append(searchKey)

        with io.open(self.fileName, 'r') as file:
            file.seek(self.start)
            for i in range(500):
                result.append(list())
                for key in self.arrangement.keys():
                    element = file.read(self.arrangement[key]).replace("~", "")

                    if key in searchKey:
                        if not element == '':
                            result[i+1].append(element)
                        else:
                            break
        return result
