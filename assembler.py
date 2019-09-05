import sys
import re

def exit_error(msg):
    print(msg)
    sys.exit(msg)

#validates and fixes hex number
def fix_hex_num(n):
    res = ""
    num = hex(int(n))
    print(num)
    if(int(n) > 0xffff):
        exit_error("NUMBER TOO LARGE")
    res += num[2:]
    return res

#fixes decimal to 16bit form hex number
def fix_to_16bit(n):
    res = fix_hex_num(n)
    return (4-len(res))*'0' + res

def is_valid_register(reg):
    regre = re.compile("r(([0-9])|(1[0-5]))\\b")
    return regre.match(reg) != None

#use only if register is validated
def get_register_number(reg):
    num = int(re.findall('\d+', reg)[0])
    print("reg" + str(num))
    return num

src = open("code.ec", 'r')
asm = open("res.evm", 'w')

for line in src:
    instr = line.split()
    opr = instr[0]
    if opr == "END":
        print("end")
        asm.write("0x00000000\n")
    if opr == "NOP":
        print("nop")
        asm.write("0x01000000\n")
    if opr == "PUSH":
        print("push")
        res = "0x0a00"
        if(instr[1]):
            value = fix_to_16bit(instr[1])
            res += value
        else:
            exit_error("NO VALUE IN PUSH INSTRUCTION")
        asm.write(res + '\n')
    if opr == "POP":
        print("pop")
        res = "0x0b00000"
        if(instr[1]):
            dest = fix_hex_num(instr[1])
            res += dest
        else:
            exit_error("NO VALUE IN POP INSTRUCTION")
        asm.write(res + '\n')
    if opr == "MOV":
        print("mov")
        res = "0x02"
        if(len(instr) == 3):
            dest = 0
            if(is_valid_register(instr[1])):
                dest = get_register_number(instr[1])
                dest = fix_hex_num(dest)
            else:
                exit_error("MISSING REGISTER IN MOV INSTRUCTION")
            if(instr[2] == 'sp'):
                res += "1" + dest + "0000"
            elif(instr[2].isdigit()):
                res += "0" + dest
                val = fix_to_16bit(instr[2])
                res += val
                print(val)
            elif(is_valid_register(instr[2])):
                res+="2" + dest + "000"
                regnum = get_register_number(instr[2])
                regnum = fix_hex_num(regnum)
                res += regnum
            else:
                exit_error("INVALID INPUT IN MOV INSTRUCTION")
            asm.write(res + '\n')
        else:
            exit_error("MISSING PARAMETERS IN MOV INSTRUCTION")

src.close()
asm.close()
