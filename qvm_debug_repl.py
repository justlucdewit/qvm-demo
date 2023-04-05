def debug_repl(vm):
    while True:
        cmd = input(">>> ")
        
        cmd_parts = cmd.split(" ")
        
        if cmd_parts[0] == "stop":
            print("")
            return
        elif cmd_parts[0] == "stack":
            max_stack_inspect_size = None
            if len(cmd_parts) > 1:
                max_stack_inspect_size = int(cmd_parts[1])
                
            print("Stack:")
            
            # print the stack
            rev_stack = vm.stack[::-1] 
            for i in range(len(rev_stack)):
                if max_stack_inspect_size != None and i >= max_stack_inspect_size:
                    break
                
                print(f"[{i}] {rev_stack[i]}")
            
            print("")
        elif cmd_parts[0] == "flag":
            flag_name = None
            if len(cmd_parts) >= 2:
                flag_name = cmd_parts[1]
            
            if flag_name == None: 
                print(f"flag halt: {vm.flags['halt']}")
                print(f"flag notZero: {vm.flags['notZero']}")
                print(f"flag zero: {vm.flags['zero']}")
                print(f"flag greaterThan: {vm.flags['greaterThan']}\n")
                print(f"flag smallerThan: {vm.flags['smallerThan']}\n")
                print(f"flag equal: {vm.flags['equal']}\n")
                print(f"flag notEqual: {vm.flags['notEqual']}\n")
            elif flag_name in vm.flags:
                print(f"flag {flag_name}: {vm.flags[flag_name]}\n")
            else:
                print(f"Invalid flag name: {flag_name}\n")
        elif cmd_parts[0] == "reg":
            reg_name = None
            if len(cmd_parts) >= 2:
                reg_name = cmd_parts[1]
            
            if reg_name == None: 
                print(f"reg a: {vm.registers['a']}")
                print(f"reg b: {vm.registers['b']}")
                print(f"reg c: {vm.registers['c']}")
                print(f"reg d: {vm.registers['d']}")
                print(f"reg pc: {vm.registers['pc']}\n")
            elif reg_name in vm.registers:
                print(f"reg {reg_name}: {vm.registers[reg_name]}\n")
            else:
                print(f"Invalid register name: {reg_name}\n")

        else:
            print("Invalid command\n")