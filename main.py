import sys
import os
import re
import translations
from translations import *

"""
TODO:
1. Add support for labels
2. Add support for the data segment
"""

def exit_error(msg):
    print(msg)
    sys.exit(msg)

def fix_n_bit_hex(num, n):
    hex_val = hex(num)[2:]
    return '0' * (n - len(str(hex_val))) + hex_val

def translate_push(arg):
    if str.isdigit(arg):
        val = int(arg)
        if val <= 0xfffff:
            instruction = append_opcode(OPCODES.PUSHI.value) + '0'
            return append_immediate(instruction, val) 
        else:
            instruction = append_opcode(OPCODES.PUSHL.value) + '0'
            return append_large_val(instruction, val) 
    elif is_reg(arg):
        instruction = append_opcode(OPCODES.PUSHR.value)
        return append_first_reg_operand(instruction, arg) + (5*'0') + '\n'

def translate_rirlrr(args, instr_dict):
    reg = args[0]
    arg2 = args[1]
    if str.isdigit(arg2):
        val = int(arg2)
        if val <= 0xfffff:
            instruction = append_opcode(instr_dict['ri'])
            instruction = append_first_reg_operand(instruction, reg)
            return append_immediate(instruction, val) 
        else:
            instruction = append_opcode(instr_dict['rl'])
            instruction = append_first_reg_operand(instruction, reg)
            return append_large_val(instruction, val) 
    elif is_reg(arg2):
        instruction = append_opcode(instr_dict['rr'])
        instruction = append_first_reg_operand(instruction, reg)
        return append_second_reg_operand(instruction, arg2)

def translate_jump(opcode, arg):
    instruction = append_opcode(opcode)
    instruction = append_address(instruction, arg)
    return instruction

def append_opcode(opcode):
    return fix_n_bit_hex(opcode, 2)

def append_immediate(instruction, val):
    return instruction + fix_n_bit_hex(int(val), 5) + '\n'

def append_large_val(instruction, val):
    return instruction + (5*'0') + '\n' + fix_n_bit_hex(int(val), 8) + '\n'

#we append two zeroes in the middle since only jump instructions append addresses
def append_address(instruction, addr):
    return instruction + ('0' * 2) + fix_n_bit_hex(int(addr), 4) + '\n'

def append_first_reg_operand(instruction, reg):
    return instruction + reg_dict[reg]

def append_second_reg_operand(instruction, reg):
    return instruction + ('0' * 4) + reg_dict[reg] + '\n'

def translate_instruction(line):
    tokens = line.split()
    mnemonic = tokens[0]
    args = tokens[1:]
    if mnemonic == "END":
        return fix_n_bit_hex(OPCODES.END.value, 8) + '\n'
    if mnemonic == "NOP":
        return fix_n_bit_hex(OPCODES.NOP.value, 8) + '\n'
    if mnemonic == "PUSH":
        if arg_rules["PUSH"](args):
            return translate_push(args[0])
    if mnemonic == "POP":
        if arg_rules["POP"](args):
            instruction = append_opcode(OPCODES.POP.value)
            instruction = append_first_reg_operand(instruction, args[0])
            return instruction + 5 * '0' + '\n'
    if mnemonic == "LDR":
        if arg_rules["LDR"](args):
            instruction = append_opcode(OPCODES.LDR.value)
            instruction = append_first_reg_operand(instruction, args[0])
            instruction = append_second_reg_operand(instruction, args[1])
            return instruction
    if mnemonic == "STR":
        if arg_rules["STR"](args):
            instruction = append_opcode(OPCODES.STR.value)
            instruction = append_first_reg_operand(instruction, args[0])
            instruction = append_second_reg_operand(instruction, args[1])
            return instruction
    if mnemonic == "MOV":
        if arg_rules["MOV"](args):
            return translate_rirlrr(args, mov_dict)
    if mnemonic == "ADD":
        if arg_rules["ADD"](args):
            return translate_rirlrr(args, add_dict)
    if mnemonic == "SUB":
        if arg_rules["SUB"](args):
            return translate_rirlrr(args, sub_dict)
    if mnemonic == "MUL":
        if arg_rules["MUL"](args):
            return translate_rirlrr(args, mul_dict)
    if mnemonic == "IMUL":
        if arg_rules["IMUL"](args):
            return translate_rirlrr(args, imul_dict)
    if mnemonic == "DIV":
        if arg_rules["DIV"](args):
            return translate_rirlrr(args, div_dict)
    if mnemonic == "IDIV":
        if arg_rules["IDIV"](args):
            return translate_rirlrr(args, idiv_dict)
    if mnemonic == "CMP":
        if arg_rules["CMP"](args):
            return translate_rirlrr(args, cmp_dict)
    if mnemonic == "JMP":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JMP.value, args[0])
    if mnemonic == "JNZ":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JNZ.value, args[0])
    if mnemonic == "JZ":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JZ.value, args[0])
    if mnemonic == "JG":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JG.value, args[0])
    if mnemonic == "JGE":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JGE.value, args[0])
    if mnemonic == "JL":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JL.value, args[0])
    if mnemonic == "JLE":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JLE.value, args[0])
    if mnemonic == "JA":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JA.value, args[0])
    if mnemonic == "JAE":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JAE.value, args[0])
    if mnemonic == "JB":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JB.value, args[0])
    if mnemonic == "JBE":
        if arg_rules["JMP"](args):
            return translate_jump(OPCODES.JBE.value, args[0])
    if mnemonic == "NOP":
        if arg_rules["NOP"](args):
            instruction = append_opcode(OPCODES.NOP.value)
            instruction = append_first_reg_operand(instruction, args[0])
            return instruction + 5 * '0' + '\n'
    if mnemonic == "AND":
        if arg_rules["AND"](args):
            return translate_rirlrr(args, and_dict)
    if mnemonic == "OR":
        if arg_rules["OR"](args):
            return translate_rirlrr(args, or_dict)
    if mnemonic == "XOR":
        if arg_rules["XOR"](args):
            return translate_rirlrr(args, xor_dict)


def main():
    if len(sys.argv) != 2:
        exit_error("INVALID NUMBER OF ARGUEMENTS")
    file_name = sys.argv[1]
    if file_name[-5:] != ".easm":
        exit_error("INVALID ASSEMBLY FILE")
    if not os.path.exists(file_name):
        exit_error("FILE NOT FOUND")
    
    with open(file_name, 'r') as f:
        code = f.readlines()
        asm_result = ""
        for line in code:
            asm_result += translate_instruction(line)

    print (asm_result)




if __name__ == '__main__':
    main()
