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
    file1.close()
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
            result = arithmeticInstruction[2] & arithmeticInstruction[3]
        else:
            result = arithmeticInstruction[2] | arithmeticInstruction[3]
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
        data = dataMemory[addressBufferInstruction[1]][1]
        resultBuffer.append([addressBufferInstruction[0], data])
        addressBuffer.pop(0)


def write(resultBufferCurrent):
    if resultBufferCurrent:
        result = resultBufferCurrent[0]
        registerFile[int(result[0].replace("R", ""))] = resultBufferCurrent[0]
        resultBuffer.pop(0)


def fromat2Elements(lst):
    return ["<" + str(item[0]) + "," + str(item[1]) + ">" for item in lst]

def fromat4Elements(lst):
    return ["<" + str(item[0]) + "," + str(item[1]) + "," + str(item[2]) + "," + str(item[3]) + ">" for item in lst]

def printResults(step):
    print("Step " + str(step) + ":")
    print("INM:" + ",".join(fromat4Elements(instructionsMemory)))
    print("INB:" + ",".join(fromat4Elements(instructionsBuffer)))
    print("AIB:" + ",".join(fromat4Elements(arithmeticInstructionBuffer)))
    print("LIB:" + ",".join(fromat4Elements(loadInstructionBuffer)))
    print("ADB:" + ",".join(fromat2Elements(addressBuffer)))
    print("REB:" + ",".join(fromat2Elements(resultBuffer)))
    print("RGF:" + ",".join(fromat2Elements(registerFile)))
    print("DAM:" + ",".join(fromat2Elements(dataMemory)))
    print("\n")

def writeResults(step,filez):
    filez.write("STEP " + str(step) + ":" + "\n")
    filez.write("INM:" + ",".join(fromat4Elements(instructionsMemory)) + "\n")
    filez.write("INB:" + ",".join(fromat4Elements(instructionsBuffer)) + "\n")
    filez.write("AIB:" + ",".join(fromat4Elements(arithmeticInstructionBuffer)) + "\n")
    filez.write("LIB:" + ",".join(fromat4Elements(loadInstructionBuffer)) + "\n")
    filez.write("ADB:" + ",".join(fromat2Elements(addressBuffer)) + "\n")
    filez.write("REB:" + ",".join(fromat2Elements(resultBuffer)) + "\n")
    filez.write("RGF:" + ",".join(fromat2Elements(registerFile)) + "\n")
    filez.write("DAM:" + ",".join(fromat2Elements(dataMemory)))

filez = open("simulation.txt", 'w')

stepCount = 0
initialize()
writeResults(stepCount, filez)
stepCount += 1

while instructionsMemory or loadInstructionBuffer or arithmeticInstructionBuffer or addressBuffer or resultBuffer:
    filez.write("\n")
    filez.write("\n")

    write(resultBuffer)
    load(addressBuffer)
    addressCalculation(loadInstructionBuffer)
    alu(arithmeticInstructionBuffer)
    issue2(instructionsBuffer)
    issue1(instructionsBuffer)
    decodeAndRead(instructionsMemory, registerFile)

    writeResults(stepCount, filez)
    stepCount += 1

filez.close()