.data
int : 5
.text
.globl main
main: 
    la $v0,int 
    lw $s1,int
    addi $t0,$0,1 
    addi $s3,$0,1    
    while:
    	
        add $s2,$t0,$t1  # s2=c   t0=a t1=b;  c= a+b
        add $t0,$0,$t1  # a=b;
        add $t1,$0,$s2  # b=c;
        sub $s1,$s1,$s3  #i--;
        beq $s1,$s5,done  # if i==0 done
        j while  #else 
    done: 
        sw $s2,4($v0)
