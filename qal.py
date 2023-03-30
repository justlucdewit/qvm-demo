import json

inp_file = "test.qal"
out_file = "test.qvm"

code = open(inp_file, "r").read()

# Remove the comments from the assembly code
temp_buffer = ""
skip_mode = False
for char in code:
    if char == ";":
        skip_mode = True
    elif char == "\n" and skip_mode == True:
        skip_mode = False
    
    if skip_mode == False:
        temp_buffer += char

code = temp_buffer

# Split by spaces, tabs, and newlines
code = code.replace("\t", " ")
code = code.replace("\n", " ")
code = [x for x in code.split(" ") if x != ""]

# Convert to tokens
tokens = []
opcodes = ["halt", "debug", "push", "pop", "swap", "nprint"]
token_index = 0
while token_index < len(code):
    curr_token = code[token_index]
    
    operands = []
    token_index += 1
    
    while token_index < len(code) and code[token_index] not in opcodes:
        registers = ["a", "b", "c", "d", "pc"]
        is_register = code[token_index] in registers
        is_numeric = code[token_index].isnumeric()
        
        operands.append({
            "type": "register" if is_register else "numeric" if is_numeric else "unknown",
            "value": code[token_index]
        })
        
        token_index += 1
          
    tokens.append({
        "type": "instruction",
        "value": curr_token,
        "operands": operands
    })
    
# Write the tokens to ast.json in a formatted way
with open("ast.json", "w") as f:
    f.write(json.dumps(tokens, indent=4))

possible_instructions = {
    "halt": [
        (0x00),
    ],
    "debug": [
        (0x01),
    ],
    "push": [
        (0x02, "numeric"),
        (0x03, "register"),
    ],
    "pop": [
        (0x04),
        (0x05, "register"),
    ],
    "swap": [
        (0x06),
    ],
    "nprint": [
        (0x69)
    ],
    "aprint": [
        (0x69)
    ]
}

generated_bytecode = []
for token in tokens:
    if not token["value"] in possible_instructions:
        print("Error: Unknown instruction '" + token["value"] + "'")
        exit(-1)

    possible_instructions = possible_instructions[token["value"]]
    
    print(possible_instructions)
    
    # if token["value"] == "halt":
    #     generated_bytecode.append(0x00)
    # elif token["value"] == "debug":
    #     generated_bytecode.append(0x01)
    # elif token["value"] == "swap":
    #     generated_bytecode.append(0x06)
        
    # elif token["value"] == "push":
    #     operands = token["operands"]
    #     if len(operands) == 1 and operands[0]["type"] == "numeric":
    #         generated_bytecode.append(0x02)
            
    #         operand_bytes = [] # 4 bytes
    #         operand = int(operands[0]["value"])
    #         operand_bytes.append(operand & 0xFF)
    #         operand_bytes.append((operand >> 8) & 0xFF)
    #         operand_bytes.append((operand >> 16) & 0xFF)
    #         operand_bytes.append((operand >> 24) & 0xFF)
    #         operand_bytes = operand_bytes[::-1]
            
    #         generated_bytecode.extend(operand_bytes)
    
    # elif token["value"] == "nprint":
    #     operands = token["operands"]
    #     if len(operands) == 0:
    #         generated_bytecode.append(0x10)
    #     elif len(operands) == 1 and operands[0]["type"] == "numeric":
    #         generated_bytecode.append(0x11)
            
    #         operand_bytes = [] # 4 bytes
    #         operand = int(operands[0]["value"])
    #         operand_bytes.append(operand & 0xFF)
    #         operand_bytes.append((operand >> 8) & 0xFF)
    #         operand_bytes.append((operand >> 16) & 0xFF)
    #         operand_bytes.append((operand >> 24) & 0xFF)
    #         operand_bytes = operand_bytes[::-1]
            
    #         generated_bytecode.extend(operand_bytes)
    #     elif len(operands) == 1 and operands[0]["type"] == "register":
    #         generated_bytecode.append(0x12)
            
    #         operand_bytes = [] # 1 byte
            
            
            
        
    
# Write the bytecode to the output file
with open(out_file, "wb") as f:
    f.write(bytes(generated_bytecode))