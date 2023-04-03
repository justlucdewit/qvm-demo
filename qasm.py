import json

inp_file = "test.qasm"
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

code_arr = []
buffer = ""
string_mode = False
for char in code:
    if char == '"':
        buffer += "\""
        string_mode = not string_mode
    elif char == " " and string_mode == False:
        code_arr.append(buffer)
        buffer = ""
    else:
        buffer += char

if buffer != "":
    code_arr.append(buffer)

code = code_arr

# Remove empty strings, or strings with just whitespace
code = list(filter(lambda x: x.strip() != "", code))

# Remove special escape characters like \n \t \r etc.
for i, code_item in enumerate(code):
    if code_item[0] == '"' and code_item[-1] == '"':
        code_item = code_item[1:-1]
        code_item = code_item.replace("\\n", "\n")
        code_item = code_item.replace("\\t", "\t")
        code_item = code_item.replace("\\r", "\r")
        code_item = code_item.replace("\\", "\\")
        code_item = code_item.replace("\\\"", "\"")
        code_item = "\"" + code_item + "\""
        code[i] = code_item

# Convert to tokens
tokens = []
opcodes = ["halt", "debug", "push", "pop", "swap", "nprint", "aprint", "sprint"]
keywords = ["raw"]
token_index = 0
while token_index < len(code):
    curr_token = code[token_index]
    
    operands = []
    token_index += 1
    
    while token_index < len(code) and code[token_index] not in opcodes and code[token_index] not in keywords:
        registers = ["a", "b", "c", "d", "pc"]
        is_register = code[token_index] in registers
        is_numeric = code[token_index].isnumeric()
        
        operands.append({
            "type": "register" if is_register else "numeric" if is_numeric else "unknown",
            "value": code[token_index]
        })
        
        token_index += 1
        
    if curr_token in opcodes:
        tokens.append({
            "type": "instruction",
            "value": curr_token,
            "operands": operands
        })
    else:
        tokens.append({
            "type": "keyword",
            "value": curr_token,
            "string_value": operands[0]["value"][1:-1]
        })
    
# Write the tokens to ast.json in a formatted way
with open("ast.json", "w") as f:
    f.write(json.dumps(tokens, indent=4))

possible_instructions = {
    "halt": [
        [0x00],
    ],
    "debug": [
        [0x01],
    ],
    "push": [
        [0x02, "numeric"],
        [0x03, "register"],
    ],
    "pop": [
        [0x04],
        [0x05, "register"],
    ],
    "swap": [
        [0x06],
    ],
    "nprint": [
        [0x10],
        [0x11, "numeric"],
        [0x12, "register"],
    ],
    "aprint": [
        [0x13],
        [0x14, "numeric"],
        [0x15, "register"],
    ],
    "sprint": [
        [0x16],
        [0x17, "numeric", "numeric"],
        [0x18, "numeric", "register"],
        [0x19, "register", "numeric"],
        [0x1A, "register", "register"],
    ]
}

generated_bytecode = []
token_index = 0
# for token in tokens:
#     print(token)

while token_index < len(tokens):
    # print(token_index)
    token = tokens[token_index]

    if token["type"] == "keyword" and token["value"] == "raw":
        # print(token["string_value"])
        for char in token["string_value"]:
            generated_bytecode.append(ord(char))
        token_index += 1
    else:

        # print(possible_instructions["nprint"], token["value"])
        if not (token["value"] in possible_instructions):
            print("Error: Unknown instruction '" + token["value"] + "'")
            exit(-1)

        possible_instruction = possible_instructions[token["value"]]

        # find the correct instruction to use based on the next tokens
        current_instruction_footprint = list(map(lambda x: x["type"], token["operands"]))
        
        # see if the current instruction matches the current footprint
        for instruction in possible_instruction:
            # print(instruction[1:])
            if instruction[1:] == current_instruction_footprint:
                # we found the correct instruction
                generated_bytecode.append(instruction[0])

                # add the operands
                i = -1
                for operand in instruction[1:]:
                    i += 1
                    if operand == "numeric":
                        operand_bytes = [] # 4 bytes
                        operand = int(token["operands"][i]["value"])
                        operand_bytes.append(operand & 0xFF)
                        operand_bytes.append((operand >> 8) & 0xFF)
                        operand_bytes.append((operand >> 16) & 0xFF)
                        operand_bytes.append((operand >> 24) & 0xFF)
                        operand_bytes = operand_bytes[::-1]

                        generated_bytecode.extend(operand_bytes)
                        # token_index += 1
                    elif operand == "register":
                        operand_bytes = []
                        operand = token["operands"][i]["value"]

                        # Convert register name (a - d) to register number (0 - 3)
                        operand = ord(operand) - ord("a")

                        operand_bytes.append(operand)
                        generated_bytecode.extend(operand_bytes)

        token_index += 1
    
    # 
    
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