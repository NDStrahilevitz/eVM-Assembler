import sys
import re
from enum import auto, Enum

class OPCODES(Enum):
    END = "0" 
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

def exit_error(msg):
    print(msg)
    sys.exit(msg)

def translate_register(reg):
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

    return reg_dict[reg]

def translate_instruction(instruction):
    return

def main():
    print(translate_register("R15"))
    return


if __name__ == '__main__':
    main()
