sprint s_one 5
sprint s_two 5
sprint s_three 5

jmp skip_to_here

; The next 3 will not be ran
sprint s_four 5
sprint s_five 5
sprint s_six 5

skip_to_here:
sprint s_seven 5
sprint s_eight 5
sprint s_nine 5
sprint s_ten 6
halt

s_one:   raw " - 1\n"
s_two:   raw " - 2\n"
s_three: raw " - 3\n"
s_four:  raw " - 4\n"
s_five:  raw " - 5\n"
s_six:   raw " - 6\n"
s_seven: raw " - 7\n"
s_eight: raw " - 8\n"
s_nine:  raw " - 9\n"
s_ten:  raw " - 10\n"