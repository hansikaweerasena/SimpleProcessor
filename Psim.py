dataMemory = []
instructionsMemory = []
registerFile = []

instructionsBuffer = []
arithmeticInstructionBuffer = []
loadInstructionBuffer = []
resultBuffer = []
addressBuffer = []


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
        instructionsMemory.append(item)


def decodeAndRead(instructionsMemoryCurrent, registerFileCurrent):
    if instructionsMemoryCurrent:
        instruction = instructionsMemory.pop(0)
        operand1 = int(instruction[2].replace("R", ""))
        operand2 = int(instruction[3].replace("R", ""))
        if registerFileCurrent[operand1]:
            instruction[2] = int(registerFileCurrent[operand1][1])
        if registerFileCurrent[operand2]:
            instruction[3] = int(registerFileCurrent[operand2][1])
        instructionsBuffer.append(instruction)



def issue1(instructionsBufferCurrent):
    if instructionsBufferCurrent:
        i = 0
        for instruction in instructionsBufferCurrent:
            if instruction[0] in ["ADD", "SUB", "AND", "OR"]:
                instructionsBuffer.pop(i)
                arithmeticInstructionBuffer.append(instruction)
                break
            else:
                i += 1


def issue2(instructionsBufferCurrnet):
    if instructionsBufferCurrnet:
        i = 0
        for instruction in instructionsBufferCurrnet:
            if instruction[0] == "LD":
                instructionsBuffer.pop(i)
                loadInstructionBuffer.append(instruction)
                break
            else:
                i += 1


def alu(arithmeticInstructionBufferCurrent):
    if arithmeticInstructionBufferCurrent:
        arithmeticInstruction = arithmeticInstructionBufferCurrent[0]
        if arithmeticInstruction[0] == "ADD":
            result = arithmeticInstruction[2] + arithmeticInstruction[3]
        elif arithmeticInstruction[0] == "SUB":
            result = arithmeticInstruction[2] - arithmeticInstruction[3]
        elif arithmeticInstruction[0] == "AND":
            result = arithmeticInstruction[2] and arithmeticInstruction[3]
        else:
            result = arithmeticInstruction[2] or arithmeticInstruction[3]
        arithmeticInstructionBuffer.pop(0)
        resultBuffer.append([arithmeticInstruction[1], result])


def addressCalculation(loadInstructionBufferCurrent):
    if loadInstructionBufferCurrent:
        loadInstruction = loadInstructionBufferCurrent[0]
        dataMemoryAddress = loadInstruction[2] + loadInstruction[3]
        addressBuffer.append([loadInstruction[1], dataMemoryAddress])
        loadInstructionBuffer.pop(0)


def load(addressBufferCurrent):
    if addressBufferCurrent:
        addressBufferInstruction = addressBufferCurrent[0]
        data = dataMemory[addressBufferInstruction[1]]
        resultBuffer.append([addressBufferInstruction[0], data])
        addressBuffer.pop(0)


def write(resultBufferCurrent):
    if resultBufferCurrent:
        result = resultBufferCurrent[0]
        registerFile[int(result[0].replace("R", ""))] = result[1]
        resultBuffer.pop(0)


def printResults(step):
    print("Step" + str(step) + ":")
    print(instructionsMemory)
    print(instructionsBuffer)
    print(arithmeticInstructionBuffer)
    print(loadInstructionBuffer)
    print(addressBuffer)
    print(resultBuffer)
    print(registerFile)
    print(dataMemory)


stepCount = 0
initialize()
printResults(stepCount)
stepCount += 1

while instructionsMemory or loadInstructionBuffer or arithmeticInstructionBuffer or addressBuffer or resultBuffer:
    dataMemoryCurrent = list.copy(dataMemory)
    instructionsMemoryCurrent = list.copy(instructionsMemory)
    registerFileCurrent = list.copy(registerFile)
    instructionsBufferCurrent = list.copy(instructionsBuffer)
    arithmeticInstructionBufferCurrent = list.copy(arithmeticInstructionBuffer)
    loadInstructionBufferCurrent = list.copy(loadInstructionBuffer)
    resultBufferCurrent = list.copy(resultBuffer)
    addressBufferCurrent = list.copy(addressBuffer)

    decodeAndRead(instructionsMemoryCurrent, registerFileCurrent)
    issue1(instructionsBufferCurrent)
    issue2(instructionsBufferCurrent)
    alu(arithmeticInstructionBufferCurrent)
    addressCalculation(loadInstructionBufferCurrent)
    load(addressBufferCurrent)
    write(resultBufferCurrent)

    printResults(stepCount)
    stepCount += 1
