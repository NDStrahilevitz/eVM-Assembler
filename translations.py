from enum import auto, Enum

data_seg_start = 0x6000
code_seg_start = 0x8000

def is_reg(arg):
    return arg in reg_dict.keys()

def validate_address(arg):
    return str.isdigit(arg) and int(arg) <= 0xffff

def validate_num_val(arg):
    return str.isdigit(arg) and int(arg) <= 0xffffffff

def rirlrr_validation(args):
    return len(args) == 2 and is_reg(args[0]) and (validate_num_val(args[1]) or is_reg(args[1]))

class OPCODES(Enum):
    END = 0 
    NOP = auto()
    PUSHI = auto()
    PUSHL = auto()
    PUSHR = auto()
    POP = auto()
    LDR = auto()
    STR = auto()
    MOVRI = auto() 
    MOVRL = auto() 
    MOVRR = auto()
    ADDRI = auto() 
    ADDRL = auto() 
    ADDRR = auto()
    SUBRI = auto() 
    SUBRL = auto() 
    SUBRR = auto()
    MULRI = auto() 
    MULRL = auto() 
    MULRR = auto()
    DIVRI = auto() 
    DIVRL = auto() 
    DIVRR = auto()
    IMULRI  = auto()
    IMULRL  = auto()
    IMULRR = auto()
    IDIVRI  = auto()
    IDIVRL  = auto()
    IDIVRR  = auto()
    CMPRI  = auto()
    CMPRL   = auto()
    CMPRR = auto()
    JMP  = auto()
    JNZ  = auto()
    JZ  = auto()
    JG  = auto()
    JGE  = auto()
    JL  = auto()
    JLE  = auto()
    JA  = auto()
    JAE  = auto()
    JB  = auto()
    JBE = auto()
    NOT = auto()
    ANDRI  = auto()
    ANDRL  = auto()
    ANDRR = auto()
    ORRI  = auto()
    ORRL  = auto()
    ORRR = auto()
    XORRI  = auto()
    XORRL = auto()
    XORRR = auto()

label_table = {}

reg_dict = {
    "R0": "0", 
    "R1": "1", 
    "R2": "2", 
    "R3": "3", 
    "R4": "4", 
    "R5": "5", 
    "R6": "6", 
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "a",
    "R11": "b",
    "R12": "c",
    "R13": "d",
    "R14": "e",
    "R15": "f",
    "FL": "c",
    "PC": "d",
    "BP": "e",
    "SP": "f"
    }

mov_dict ={
    "ri": OPCODES.MOVRI.value,
    "rl": OPCODES.MOVRL.value,
    "rr": OPCODES.MOVRR.value
}
add_dict ={
    "ri": OPCODES.ADDRI.value,
    "rl": OPCODES.ADDRL.value,
    "rr": OPCODES.ADDRR.value
}
sub_dict ={
    "ri": OPCODES.SUBRI.value,
    "rl": OPCODES.SUBRL.value,
    "rr": OPCODES.SUBRR.value
}
mul_dict ={
    "ri": OPCODES.MULRI.value,
    "rl": OPCODES.MULRL.value,
    "rr": OPCODES.MULRR.value
}
imul_dict ={
    "ri": OPCODES.IMULRI.value,
    "rl": OPCODES.IMULRL.value,
    "rr": OPCODES.IMULRR.value
}
div_dict ={
    "ri": OPCODES.DIVRI.value,
    "rl": OPCODES.DIVRL.value,
    "rr": OPCODES.DIVRR.value
}
idiv_dict ={
    "ri": OPCODES.IDIVRI.value,
    "rl": OPCODES.IDIVRL.value,
    "rr": OPCODES.IDIVRR.value
}
cmp_dict ={
    "ri": OPCODES.CMPRI.value,
    "rl": OPCODES.CMPRL.value,
    "rr": OPCODES.CMPRR.value
}
and_dict ={
    "ri": OPCODES.ANDRI.value,
    "rl": OPCODES.ANDRL.value,
    "rr": OPCODES.ANDRR.value
}
or_dict ={
    "ri": OPCODES.ORRI.value,
    "rl": OPCODES.ORRL.value,
    "rr": OPCODES.ORRR.value
}
xor_dict ={
    "ri": OPCODES.XORRI.value,
    "rl": OPCODES.XORRL.value,
    "rr": OPCODES.XORRR.value
}

arg_rules = {
    "PUSH": lambda args: len(args) == 1 and (validate_num_val(args[0]) or is_reg(args[0])),
    "POP":  lambda args: len(args) == 1 and is_reg(args[0]),
    "LDR":  lambda args: len(args) == 2 and is_reg(args[0]) and is_reg(args[1]),
    "STR":  lambda args: len(args) == 2 and is_reg(args[0]) and is_reg(args[1]),
    "MOV":  rirlrr_validation,
    "ADD":  rirlrr_validation,
    "SUB":  rirlrr_validation,
    "MUL":  rirlrr_validation,
    "IMUL": rirlrr_validation,
    "DIV":  rirlrr_validation,
    "IDIV": rirlrr_validation,
    "CMP":  rirlrr_validation,
    "JMP":  lambda args: len(args) == 1 and validate_address(args[0]),
    "NOT":  lambda args: len(args) == 1 and is_reg(args[0]),
    "AND":  rirlrr_validation,
    "OR":  rirlrr_validation,
    "XOR":  rirlrr_validation,
}
