import sys
import re

def exit_error(msg):
    print(msg)
    sys.exit(msg)

#validates and fixes hex number
def fix_hex_num(n):
    res= ""
    num = hex(int(n))
    if(int(n) > 0xffff):
        exit_error("NUMBER TOO LARGE")
    res += num[2:]
    return res


def is_valid_register(reg):
    regre = re.compile("r(([0-9])|(1[0-5]))\\b")
    return regre.match(reg) != None

#use only if register is validated
def get_register_number(reg):
    num = int(re.findall('\d+', reg)[0])
    print("reg" + str(num))
    return num

src = open("code.ec", 'r')
dest = open("res.evm", 'w')

for line in src:
    instr = line.split()
    opr = instr[0]
    if opr == "END":
        print("end")
        dest.write("0x0\n")
    if opr == "NOP":
        print("nop")
        dest.write("0x10000000\n")
    if opr == "PUSH":
        print("push")
        res = "0x2000"
        if(instr[1]):
            value = fix_hex_num(instr[1])
            res += '0'*(4-len(value))
            res += value
            dest.write(res + '\n')
        else:
            exit_error("NO VALUE IN PUSH INSTRUCTION")
    if opr == "MOV":
        print("mov")
        res = "0x4"
        if(len(instr) == 3):
            if(is_valid_register(instr[1])):
                regnum = get_register_number(instr[1])
                regnum = fix_hex_num(regnum)
                res += regnum + "0"
            else:
                exit_error("MISSING REGISTER IN MOV INSTRUCTION")
            if(instr[2] == 'sp'):
                res += "10000"
            elif(instr[2].isdigit()):
                res+="0"
                res+=fix_hex_num(instr[2])
            elif(is_valid_register(instr[2])):
                res+="2000"
                regnum = get_register_number(instr[2])
                regnum = fix_hex_num(regnum)
                res+=regnum
            else:
                exit_error("INVALID INPUT IN MOV INSTRUCTION")
            dest.write(res + '\n')
        else:
            exit_error("MISSING PARAMETERS IN MOV INSTRUCTION")
            

src.close()
dest.close()
