dataMemory = []
instructionMemory = []
registerFile = []

def initialize():
    initializeDataMemory()
    initializeRegisters()
    initializeInstructions()

def readFileLineByLine(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    itemList = []
    for line in Lines:
        itemList.append(line.strip())
    return itemList

def initializeDataMemory():
    itemList = readFileLineByLine("datamemory.txt")
    for item in itemList:
        temp = item.split(",")
        item = [temp[0].replace("<", ""), temp[1].replace(">", "")]
        dataMemory.append(item)

def initializeRegisters():
    itemList = readFileLineByLine("registers.txt")
    for item in itemList:
        temp = item.split(",")
        item = [temp[0].replace("<", ""), temp[1].replace(">", "")]
        registerFile.append(item)

def initializeInstructions():
    itemList = readFileLineByLine("instructions.txt")
    for item in itemList:
        temp = item.split(",")
        item = [temp[0].replace("<", ""), temp[1], temp[2], temp[3].replace(">", "")]
        instructionMemory.append(item)

initialize()
print(dataMemory)
print(registerFile)
print(instructionMemory)


