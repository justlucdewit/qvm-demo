from qvm_instructions import run_instruction

class QuadiraVirtualMachine:
    def __init__(self, file):
        self.code = list(open(file, 'rb').read())
        
        self.registers = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "pc": 0
        }
        
        self.stack = [] # stack.append(number)  ------ number = stack.pop()
        
        self.flags = {
            'halt': False,
            'notZero': False,
            'zero': False,
            'greaterThan': False,
            'smallerThan': False,
            'equal': False,
            'notEqual': False,
        }
    
    def increment_program_counter(self, amount = 1):
        self.registers['pc'] += amount
    
    def get_u32(self):
        index = self.registers["pc"]
        self.increment_program_counter(4)
        return self.code[index + 3] + (self.code[index + 2] << 8) + (self.code[index + 1] << 16) + (self.code[index] << 24)
    
    def get_u8(self):
        index = self.registers["pc"]
        self.increment_program_counter()
        return self.code[index]
    
    def get_register(self):
        reg_names = ["a", "b", "c", "d", "pc"]
        reg_id = self.get_u8()
        return reg_names[reg_id % 5]
        
    def get_current_instruction(self):
        return self.code[self.registers['pc']]

# Create the virtual machine
vm = QuadiraVirtualMachine("test.qvm")

# Fetch-Decode-Execute loop
while vm.flags['halt'] == False:
    # Fetch instruction
    instruction = vm.get_current_instruction()
    
    # Increment program counter
    vm.increment_program_counter()

    # Decode & Execute instruction
    run_instruction(instruction, vm)    