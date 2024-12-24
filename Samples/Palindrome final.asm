.data
    int: 321123
.text
.globl main

main:
    la $v1, int          # load the addresss into v1
    lw $s1, int	
    lw $s6, int 
  
    addi $s4,$0,10

     while:    
         div $s1,$s4
         mflo $s1
         mfhi $s5
         mul $s2,$s2,$s4      # s4 has the value 10 
         add $s2,$s5,$s2      # storing the reversed number in s2
         beq $s1,$0,done
         j while
    done:
    	beq $s2,$s6,pr
        j exit
    pr:
    	addi $v0,$0,1
    	j exit
    exit:
    	sw $v0 ,4($v1) 
