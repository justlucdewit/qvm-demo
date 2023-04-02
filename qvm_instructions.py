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
    0x10: "nprint", # numeric print
    0x11: "nprint <lit>", # ascii print
    0x12: "nprint <reg>", # ascii print
    0x13: "aprint", # numeric print
    0x14: "aprint <lit>", # ascii print
    0x15: "aprint <reg>", # ascii print
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

    elif instruction == 0x10:
        num = vm.stack.pop()
        print(num)
        
    elif instruction == 0x11:
        num = vm.get_u32()
        print(num)
        
    elif instruction == 0x12:
        reg = vm.get_register()
        num = vm.registers[reg]
        print(num)
    
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