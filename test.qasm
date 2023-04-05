push 0 ; start with counter being 0

loop:
    sleep 1000

    ; Increment counter by 1
    push 1
    add

    ; Check if counter is divisable by 3
    dup
    push 3
    mod
    push 0
    cmp
    je div_by_3

    ; Check if counter is divisable by 5
    dup
    push 5
    mod
    push 0
    cmp
    je div_by_5

    ; Conclusion: its neither div by 3 or 5
    ; so, print the number
    dup
    nprint
    sprint new_line 1

    jmp loop ; Again!

div_by_3:
    ; its divisable by 3,
    ; BUT it might still be divisable by 5 too
    ; check to make sure

    ; Check if counter is divisable by 5
    dup
    push 5
    mod
    push 0
    cmp
    je fizzbuzz

    ; If not do fizz
    sprint fizz 4
    sprint new_line 1
    jmp loop

    fizzbuzz:
        sprint fizz 4
        sprint buzz 4
        sprint new_line 1
        jmp loop

div_by_5:
    ; its divisable by 5,
    ; so print buzz
    sprint buzz 4
    sprint new_line 1
    jmp loop

; String definitions
fizz: raw "fizz"
buzz: raw "buzz"
new_line: raw "\n"