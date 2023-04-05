push 10

loop:
    ; Print the number with a new line
    dup
    nprint
    sprint new_line 1

    push 1 ; Decrement the counter
    sub

    dup ; Check if the counter is 0
    push 0
    cmp

    sleep 1000 ; Wait 1 second
    jne loop

sprint lift_off 9 ; Print "lift off!"

halt

new_line: raw "\n" ; 1 chars
lift_off: raw "lift off!" ; 9 chars