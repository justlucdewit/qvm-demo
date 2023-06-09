import time
from qvm_debug_repl import debug_repl

DEBUG = False

instruction_mapping = {
    0x00: "halt",
    0x01: "debug", # Debug opens a REPL for reading the registers and stack and heap
    0x02: "push <lit>", # Push a value onto the stack
    0x03: "push <reg>", # Push a value from a register onto the stack
    0x04: "pop", # Pop a value off the stack and void it
    0x05: "pop <reg>", # Pop a value off the stack and store it in a register
    0x06: "swap", # Swap the top two values on the stack
    0x07: "dup", # Duplicate the top value on the stack
    0x10: "nprint", # numeric print
    0x11: "nprint <lit>", # ascii print
    0x12: "nprint <reg>", # ascii print
    0x13: "aprint", # numeric print
    0x14: "aprint <lit>", # ascii print
    0x15: "aprint <reg>", # ascii print
    0x16: "sprint", # string print
    0x17: "sprint <lit> <lit>", # string print
    0x18: "sprint <lit> <reg>", # string print
    0x19: "sprint <reg> <lit>", # string print
    0x1A: "sprint <reg> <reg>", # string print
    0x20: "add", # stack addition
    0x21: "sub", # stack subtraction
    0x22: "mul", # stack multiplication
    0x23: "div", # stack division
    0x24: "mod", # stack modulus
    0x25: "add <reg> <reg>", # register addition
    0x26: "sub <reg> <reg>", # register subtraction
    0x27: "mul <reg> <reg>", # register multiplication
    0x28: "div <reg> <reg>", # register division
    0x29: "mod <reg> <reg>", # register modulus
    0x30: "jmp <lit>", # jump to an address
    0x31: "jmp <reg>", # jump to a register address
    0x32: "jnz <lit>", # jump to an address if the top of the stack is not zero
    0x33: "jnz <reg>", # jump to a register address if the top of the stack is not zero
    0x34: "jz <lit>", # jump to an address if the top of the stack is zero
    0x35: "jz <reg>", # jump to a register address if the top of the stack is zero
    0x36: "jg <lit>", # jump to an address if the first value on the stack is greater than the second
    0x37: "jg <reg>", # jump to a register address if the first value on the stack is greater than the second
    0x38: "js <lit>", # jump to an address if the first value on the stack is smaller than the second
    0x39: "js <reg>", # jump to a register address if the first value on the stack is smaller than the second
    0x3A: "je <lit>", # jump to an address if the first value on the stack is equal to the second
    0x3B: "je <reg>", # jump to a register address if the first value on the stack is equal to the second
    0x3C: "jne <lit>", # jump to an address if the first value on the stack is not equal to the second
    0x3D: "jne <reg>", # jump to a register address if the first value on the stack is not equal to the second
    0x40: "cmp", # compare two values on the stack
    0x41: "cmp <reg> <reg>", # compare two registers
    0x42: "sleep", # sleep for a number of milliseconds on the stack
    0x43: "sleep <reg>", # sleep for a number of milliseconds in a register
    0x44: "sleep <lit>" # sleep for a number of milliseconds in a literal
}

def run_instruction(instruction, vm):
    if DEBUG:
        instruction_name = instruction_mapping[instruction]
        print(f"[DEBUG] Instruction: {instruction_name} ({hex(instruction)})")
        
    if instruction == 0x00:
        vm.flags['halt'] = True

    elif instruction == 0x01:
        debug_repl(vm)
    
    elif instruction == 0x02:
        num = vm.get_u32()
        vm.stack.append(num)

    elif instruction == 0x03:
        reg_name = vm.get_register()
        vm.stack.append(vm.registers[reg_name])

    elif instruction == 0x04:
        vm.stack.pop()

    elif instruction == 0x05:
        reg_name = vm.get_register()
        vm.registers[reg_name] = vm.stack.pop()

    elif instruction == 0x06:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1)
        vm.stack.append(num2)

    elif instruction == 0x07:
        vm.stack.append(vm.stack[-1])

    elif instruction == 0x10:
        num = vm.stack.pop()
        print(num, end="")
        
    elif instruction == 0x11:
        num = vm.get_u32()
        print(num, end="")
        
    elif instruction == 0x12:
        reg = vm.get_register()
        num = vm.registers[reg]
        print(num, end="")
    
    elif instruction == 0x13:
        num = vm.stack.pop()
        print(chr(num), end="")
    
    elif instruction == 0x14:
        num = vm.get_u32()
        print(chr(num), end="")
    
    elif instruction == 0x15:
        reg = vm.get_register()
        num = vm.registers[reg]
        print(chr(num), end="")

    elif instruction == 0x16:
        address = vm.stack.pop()
        str_len = vm.stack.pop()

        string = vm.code[address:address+str_len]
        print(string.decode("utf-8"), end="")

    elif instruction == 0x17:
        address = vm.get_u32()
        str_len = vm.get_u32()

        string = "".join(list(map(lambda x: chr(x), vm.code[address:address+str_len])))
        print(string, end="")

    elif instruction == 0x18:
        address = vm.get_u32()
        reg = vm.get_register()
        str_len = vm.registers[reg]

        string = vm.code[address:address+str_len]
        print(string.decode("utf-8"), end="")
    
    elif instruction == 0x19:
        reg = vm.get_register()
        address = vm.registers[reg]
        str_len = vm.get_u32()

        string = vm.code[address:address+str_len]
        print(string.decode("utf-8"), end="")
    
    elif instruction == 0x1A:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        address = vm.registers[reg1]
        str_len = vm.registers[reg2]

        string = vm.code[address:address+str_len]
        print(string.decode("utf-8"), end="")

    elif instruction == 0x20:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 + num2)

    elif instruction == 0x21:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 - num1)

    elif instruction == 0x22:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num1 * num2)

    elif instruction == 0x23:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 // num1)

    elif instruction == 0x24:
        num1 = vm.stack.pop()
        num2 = vm.stack.pop()
        vm.stack.append(num2 % num1)

    elif instruction == 0x25:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        vm.registers[reg2] += vm.registers[reg1]

    elif instruction == 0x26:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        vm.registers[reg2] -= vm.registers[reg1]

    elif instruction == 0x27:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        vm.registers[reg2] *= vm.registers[reg1]

    elif instruction == 0x28:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        vm.registers[reg2] //= vm.registers[reg1]

    elif instruction == 0x29:
        reg1 = vm.get_register()
        reg2 = vm.get_register()
        vm.registers[reg2] %= vm.registers[reg1]

    elif instruction == 0x30:
        addr = vm.get_u32()
        vm.registers["pc"] = addr
    
    elif instruction == 0x31:
        addr = vm.registers[vm.get_register()]
        vm.registers["pc"] = addr

    elif instruction == 0x32:
        addr = vm.get_u32()
        if vm.flags["notZero"]:
            vm.registers["pc"] = addr

    elif instruction == 0x33:
        addr = vm.registers[vm.get_register()]
        if vm.flags["notZero"]:
            vm.registers["pc"] = addr

    elif instruction == 0x34:
        addr = vm.get_u32()
        if vm.flags["zero"]:
            vm.registers["pc"] = addr

    elif instruction == 0x35:
        addr = vm.registers[vm.get_register()]
        if vm.flags["zero"]:
            vm.registers["pc"] = addr

    elif instruction == 0x36:
        addr = vm.get_u32()
        if vm.flags["greaterThan"]:
            vm.registers["pc"] = addr

    elif instruction == 0x37:
        addr = vm.registers[vm.get_register()]
        if vm.flags["greaterThan"]:
            vm.registers["pc"] = addr

    elif instruction == 0x38:
        addr = vm.get_u32()
        if vm.flags["smallerThan"]:
            vm.registers["pc"] = addr

    elif instruction == 0x39:
        addr = vm.registers[vm.get_register()]
        if vm.flags["smallerThan"]:
            vm.registers["pc"] = addr

    elif instruction == 0x3A:
        addr = vm.get_u32()
        if vm.flags["equal"]:
            vm.registers["pc"] = addr

    elif instruction == 0x3B:
        addr = vm.registers[vm.get_register()]
        if vm.flags["equal"]:
            vm.registers["pc"] = addr

    elif instruction == 0x3C:
        addr = vm.get_u32()
        if vm.flags["notEqual"]:
            vm.registers["pc"] = addr

    elif instruction == 0x3D:
        addr = vm.registers[vm.get_register()]
        if vm.flags["notEqual"]:
            vm.registers["pc"] = addr

    elif instruction == 0x40:
        # Reset the vm flags
        vm.flags = {
            'halt': False,
            'notZero': False,
            'zero': False,
            'greaterThan': False,
            'smallerThan': False,
            'equal': False,
            'notEqual': False,
        }

        num1 = vm.stack.pop()
        num2 = vm.stack.pop()

        if num1 > num2:
            vm.flags['greaterThan'] = True
        if num1 < num2:
            vm.flags['smallerThan'] = True
        if num1 == num2:
            vm.flags['equal'] = True
        if num1 != num2:
            vm.flags['notEqual'] = True

    elif instruction == 0x41:
        # Reset the vm flags
        vm.flags = {
            'halt': False,
            'notZero': False,
            'zero': False,
            'greaterThan': False,
            'smallerThan': False,
            'equal': False,
            'notEqual': False,
        }

        num1 = vm.registers[vm.get_register()]
        num2 = vm.registers[vm.get_register()]

        if num1 > num2:
            vm.flags['greaterThan'] = True
        if num1 < num2:
            vm.flags['smallerThan'] = True
        if num1 == num2:
            vm.flags['equal'] = True
        if num1 != num2:
            vm.flags['notEqual'] = True

    elif instruction == 0x42:
        time.sleep(vm.stack.pop() / 1000)

    elif instruction == 0x43:
        time.sleep(vm.registers[vm.get_register()] / 1000)

    elif instruction == 0x44:
        time.sleep(vm.get_u32() / 1000)
