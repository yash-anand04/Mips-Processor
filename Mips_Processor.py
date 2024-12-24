class Registerfile:
    def __init__(self):
        self.read_register1 = 0
        self.read_register2 = 0
        self.write_register = 0
        self.data = {"$zero": 0,
                     "$at": 0,
                     "$v0": 0, "$v1": 0,
                     "$a0": 0, "$a1": 0, "$a2": 0, "$a3": 0,
                     "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0, "$t4": 0, "$t5": 0, "$t6": 0, "$t7": 0,
                     "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0, "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,
                     "$t8": 0, "$t9": 0,
                     "$k0": 0, "$k1": 0,
                     "$gp": 0,
                     "$sp": 0,
                     "$fp": 0,
                     "$ra": 0}          #list representing 32 registers
        self.mapping = {
    "00000": '$zero',
    "00001": '$at',
    "00010": '$v0',
    "00011": '$v1',
    "00100": '$a0',
    "00101": '$a1',
    "00110": '$a2',
    "00111": '$a3',
    "01000": '$t0',
    "01001": '$t1',
    "01010": '$t2',
    "01011": '$t3',
    "01100": '$t4',
    "01101": '$t5',
    "01110": '$t6',
    "01111": '$t7',
    "10000": '$s0',
    "10001": '$s1',
    "10010": '$s2',
    "10011": '$s3',
    "10100": '$s4',
    "10101": '$s5',
    "10110": '$s6',
    "10111": '$s7',
    "11000": '$t8',
    "11001": '$t9',
    "11010": '$k0',
    "11011": '$k1',
    "11100": '$gp',
    "11101": '$sp',
    "11110": '$fp',
    "11111": '$ra',
}



class ControlCircuit():
    def __init__(self):
        self.Jump = False
        self.MemRead = False
        self.MemtoReg = False
        self.MemWrite = False
        self.Branch = False
        self.ALUControl = False
        self.ALUSrc = False
        self.RegDst = False
        self.RegWrite = False


def decoder(inst):
    print(inst)
    cc.MemRead = False
    cc.Jump = False
    cc.MemtoReg = False
    cc.MemWrite = False
    cc.Branch = False
    cc.ALUControl = '000'
    cc.ALUSrc = False
    cc.RegDst = False
    cc.RegWrite = False

    if inst == "addi":
        cc.ALUControl = '000'
        cc.ALUSrc = True
        cc.RegWrite = True
    elif inst == 'beq':
        cc.Branch = True
        cc.ALUControl = '001'
    elif inst == 'bne':
        cc.Branch = True
        cc.ALUControl = '1001'
    elif inst == 'add':
        cc.ALUControl = '000'
        cc.RegDst = True
        cc.RegWrite = True
    elif inst == 'and':
        cc.ALUControl = '110'
        cc.RegDst = True
        cc.RegWrite = True
    elif inst == 'or':
        cc.ALUControl = '100'
        cc.RegDst = True
        cc.RegWrite = True
    elif inst == 'sub':
        cc.ALUControl = '001'
        cc.RegDst = True
        cc.RegWrite = True
    elif inst == 'lw':
        cc.MemRead = True
        cc.MemtoReg = True
        cc.ALUControl = '000'
        cc.ALUSrc = True
        cc.RegWrite = True
    elif inst == 'sw':
        cc.MemWrite = True
        cc.ALUControl = '000'
        cc.ALUSrc = True
    elif inst == 'j':
        cc.Jump = True
    elif inst == 'xor':
        cc.ALUControl = '100'
        cc.RegDst = True
        cc.RegWrite = True
    elif inst == "mult":
        cc.RegDst = True
        cc.RegWrite = True
        cc.ALUControl = '010'
    elif inst == "div":
        cc.ALUControl = "011"
    elif inst == "lui":
        cc.RegWrite = True
        cc.ALUSrc = True
        cc.ALUControl = "1000"
    elif inst == "ori":
        cc.RegWrite = True
        cc.ALUSrc = True
        cc.ALUControl = '110'
    elif inst == "mfhi":
        cc.RegDst = True
        cc.RegWrite = True
        cc.ALUControl = "1111"
    elif inst == "mflo":
        cc.RegDst = True
        cc.RegWrite = True
        cc.ALUControl = "1110"


def alu(a, b):
    global lo, hi
    zero = 0
    x = 0
    if cc.ALUControl == '000':
        x = a+b
    elif cc.ALUControl == '001':
        x = a-b
    elif cc.ALUControl == '010':
        x = a*b
    elif cc.ALUControl == '011':
        hi, lo = (int(a/b), a%b)
    elif cc.ALUControl == '100':
        x = a^b
    elif cc.ALUControl == '101':
        x = a&b
    elif cc.ALUControl == '110':
        x = a|b
    elif cc.ALUControl == "1000":
        x = b << 16
    elif cc.ALUControl == "1001":
        x = ~(a^b)
    elif cc.ALUControl == "1110":
        x = hi
    elif cc.ALUControl == "1111":
        x = lo
    if x == 0:
        zero = 1
    return x, zero

def memread(address):
    address = int(address,2)
    index = int(address/4) % 8
    file = open("data memory", "r")
    for lines in file.readlines():
        addresses = int(lines[2:10], 16)
        if int(addresses/32) == int(address/32):
            return hextobin(lines[16:-1].split(" ")[index])
    file.close()


def memwrite(data,address):
    address = int(address,2)
    index = int(address/4) % 8
    data = "0x" + hex(int(data,2))[2:].zfill(8)
    file = open("data memory", "r")
    line = 0
    for lines in file.readlines():
        addresses = int(lines[2:10], 16)
        if int(addresses/32) == int(address/32):
            break
        line += 1
    file.close()
    with open("data memory", "r") as file1:
        lines = file1.readlines()
        list_of_data = lines[line].split(" ")[4:]
        list_of_data[index] = data
        changed_line = lines[line][:14] + " ".join(list_of_data)
        lines[line] = changed_line
    with open("data memory", "w") as file2:
        file2.write("".join(lines))
    file1.close()
    file2.close()


def signextend(str):
    m=len(str)
    h=32-m 
    temp=''
    for i in range(h):
        temp+='0'
    str=temp+str
    return str


def shiftlx(x, samnt):         #written like this better to use the binary string and simply append zeroes at the starting
    n=int(x)
    for i in range(samnt):
        n=n*2
    x=bin(n)
    return x


def shiftrx(x, samnt):
    n=int(x)
    for i in range(samnt):
        n=n/2 
    x=bin(n)


def mux(selectline, a, b):
    if selectline:
        return a
    else:
        return b


def regwrite(write_data):
    regfile.data[regfile.mapping[regfile.write_register]] = write_data


def readregfile(instruction):            #part of the id stage
    regfile.read_register1 = instruction[6:11]
    regfile.read_register2 = instruction[11:16]
    regfile.write_register = mux(cc.RegDst, instruction[16:21], instruction[11:16])
    return regfile.data[regfile.mapping[regfile.read_register1]], regfile.data[regfile.mapping[regfile.read_register2]]


def instructionread(address):    # it takes a hexadcimal value(8 bit string) as an input
    address = address.zfill(8)
    file = open("instruction memory", "r")
    for lines in file.readlines()[2:]:
        if lines[2:10] == address:
            return hextobin(lines[14:22])
    file.close()


def fetch(read_address):                #if-instruction fetch
    instruction = instructionread(hex(read_address)[2:])
    global pc
    pc = pc + 4
    id(instruction)


def id(instruction):
    if instruction[0:6] == '000000':
        if instruction[26:32] == '100000':
            decoder('add')
        elif instruction[26:32] == '100010':
            decoder('sub')
        elif instruction[26:32] == '100100':
            decoder('and')
        elif instruction[26:32] == '100101':
            decoder('or')
        elif instruction[26:32] == '100110':
            decoder('xor')
        elif instruction[26:32] == '100111':
            decoder('nor')
        elif instruction[26:32] == '011000':
            decoder('mult')
        elif instruction[26:32] == '011010':
            decoder('div')
        elif instruction[26:32] == "010000":
            decoder('mfhi')
        elif instruction[26:32] == "010010":
            decoder('mflo')
    elif instruction[0:6] == '000100':
        decoder('beq')
    elif instruction[0:6] == '000010':
        decoder('j')
    elif instruction[0:6] == '100011':
        decoder('lw')
    elif instruction[0:6] == '101011':
        decoder('sw')
    elif instruction[0:6] == '001000':
        decoder('addi')
    elif instruction[0:6] == '011100':
        decoder('mult')
    elif instruction[0:6] == "001111":
        decoder("lui")
    elif instruction[0:6] == "001101":
        decoder("ori")

    read_data1, read_data2 = readregfile(instruction)
    sign_extended_value = signextend(instruction[16:])
    jump_address = instruction[6:]

    ex(read_data1, read_data2, sign_extended_value, jump_address)


def ex(read_data1, read_data2, sign_extended_value, jump_address):
    second_value = mux(cc.ALUSrc, int(sign_extended_value, 2), read_data2)
    alu_result, zero = alu(read_data1, second_value)
    global pc
    if cc.Jump:
        pc = int(shiftlx(int(jump_address, 2), 2), 2)
        return
    if cc.Branch:
        if zero == 1:
            pc += int(shiftlx(int(sign_extended_value, 2), 2), 2)
            return
    memaccess(alu_result, read_data2)


def memaccess(address, write_data):
    read_data = 0
    if cc.MemWrite:
        print(write_data)
        memwrite(bin(write_data), bin(address))

    if cc.MemRead:
        read_data = memread(bin(address))
        read_data = int(read_data, 2)
    write_data = mux(cc.MemtoReg, read_data, address)  # address is the alu result
    # regfile.write_data = mux(cc.MemtoReg, read_data, address)

    writeback(write_data)


def writeback(write_data):              #register writeback
    if cc.RegWrite:
        regwrite(write_data)


def hextobin(num, num_bits=32):     # converts a number to its binary representation
    return bin(int(num,16))[2:].zfill(num_bits)


cc = ControlCircuit()
regfile = Registerfile()
pc = int("00400000", 16)
hi = 0
lo = 0
while pc <= int("00400048", 16):
    fetch(pc)

