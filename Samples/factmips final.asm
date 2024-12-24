.data
    int : 7
.text
.global main

main:
    la $v0, int
    lw $s0 ,int
    addi $t0,$0,1
    addi $t1,$0,1
fact:
    mul $t0, $t0,$t1
    beq $t1, $s0,done
    addi $t1, $t1,1
    j fact
done:
    sw $t0, 4($v0)
