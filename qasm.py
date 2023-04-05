import json

inp_file = "test.qasm"
out_file = "test.qvm"

code = open(inp_file, "r").read()









# ====================================== #
#   _____               _                #
#  |  __ \             (_)               #
#  | |__) |_ _ _ __ ___ _ _ __   __ _    #
#  |  ___/ _` | '__/ __| | '_ \ / _` |   #
#  | |  | (_| | |  \__ \ | | | | (_| |   #
#  |_|   \__,_|_|  |___/_|_| |_|\__, |   #
#                                __/ |   #
#                               |___/    #
# ====================================== #

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
labels = []
opcodes = ["halt", "debug", "push", "pop", "swap", "dup", "nprint", "aprint", "sprint", "add", "sub", "mul", "div", "mod", "jmp", "jnz", "jz", "jg", "js", "je", "jne", "cmp", "sleep"]
registers = ["a", "b", "c", "d", "pc"]
keywords = ["raw"]
current_offset = 0
token_index = 0
while token_index < len(code):
    curr_token = code[token_index]
    
    operands = []
    token_index += 1
    
    while token_index < len(code) and code[token_index] not in opcodes and code[token_index] not in keywords and not code[token_index].endswith(":"):
        is_register = code[token_index] in registers
        is_numeric = code[token_index].isnumeric()
        curr_type = "register" if is_register else "numeric" if is_numeric else "unknown"
        operands.append({
            "type": curr_type,
            "value": code[token_index]
        })

        if curr_type == "unknown":
            current_offset += 4
        
        token_index += 1
        
    if curr_token in opcodes:
        tokens.append({
            "type": "instruction",
            "value": curr_token,
            "operands": operands
        })
        current_offset += 1

        for operand in operands:
            if operand["type"] == "register":
                current_offset += 1
            elif operand["type"] == "numeric":
                current_offset += 4

    elif curr_token.endswith(":"):
        labels.append({
            "type": "label",
            "value": curr_token[:-1],
            "points_to": current_offset
        })
    else:
        tokens.append({
            "type": "keyword",
            "value": curr_token,
            "string_value": operands[0]["value"][1:-1]
        })

        if curr_token == "raw":
            current_offset += len(operands[0]["value"][1:-1])  - 4
    

# Loop trough all the instruction operands and replace unknowns with labels if they exist
for token in tokens:
    if token["type"] == "instruction":
        for operand in token["operands"]:
            if operand["type"] == "unknown":
                found = False

                for label in labels:
                    if label["value"] == operand["value"]:
                        operand["type"] = "numeric"
                        operand["value"] = label["points_to"]
                        found = True
                        break

                if found == False:
                    print("[error] Unknown label: " + operand["value"])
                    exit(1)


# =============================================================================== #
#    _____          _         _____                           _   _               #
#   / ____|        | |       / ____|                         | | (_)              #
#  | |     ___   __| | ___  | |  __  ___ _ __   ___ _ __ __ _| |_ _  ___  _ __    #
#  | |    / _ \ / _` |/ _ \ | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \   #
#  | |___| (_) | (_| |  __/ | |__| |  __/ | | |  __/ | | (_| | |_| | (_) | | | |  #
#   \_____\___/ \__,_|\___|  \_____|\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_|  #
# ==============================================================================  #

print("[info] Parsing completed")

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
    "dup": [
        [0x07],
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
    ],
    "add": [
        [0x20],
        [0x25, "register", "register"]
    ],
    "sub": [
        [0x21],
        [0x26, "register", "register"]
    ],
    "mul": [
        [0x22],
        [0x27, "register", "register"]
    ],
    "div": [
        [0x23],
        [0x28, "register", "register"]
    ],
    "mod": [
        [0x24],
        [0x29, "register", "register"]
    ],
    "jmp": [
        [0x30, "numeric"],
        [0x31, "register"]
    ],
    "jnz": [
        [0x32, "numeric"],
        [0x33, "register"]
    ],
    "jz": [
        [0x34, "numeric"],
        [0x35, "register"]
    ],
    "jg": [
        [0x36, "numeric"],
        [0x37, "register"]
    ],
    "js": [
        [0x38, "numeric"],
        [0x39, "register"]
    ],
    "je": [
        [0x3A, "numeric"],
        [0x3B, "register"]
    ],
    "jne": [
        [0x3C, "numeric"],
        [0x3D, "register"]
    ],
    "cmp": [
        [0x40],
        [0x41, "register", "register"]
    ],
    "sleep": [
        [0x42],
        [0x43, "register"],
        [0x44, "numeric"]
    ]
}

generated_bytecode = []
token_index = 0

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
    
# Write the bytecode to the output file
with open(out_file, "wb") as f:
    f.write(bytes(generated_bytecode))

print("[info] Code generation completed")