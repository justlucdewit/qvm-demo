push 0                  ; Init the counter

loop:
    push 1              ; Increment the counter
    add

    sprint prefix 3     ; Print the thing
    dup
    nprint
    sprint new_line 1
    
    jmp loop            ; Go back to the top

prefix: raw " - "       ; 3 chars
new_line: raw "\n"      ; 1 chars