#define STDOUT 0xd0580000

.section .text
.global bit_reverse_indices


# === Bit Reverse Indices ===
# reverses a array values according to bit-reverse-permutation
# Input: a1 has the array and a0 has the size
# Output: a1 has now all the values adjusted in arra according to reverse indices

bit_reverse_indices:
    addi sp, sp, -52
    sw t4, 48(sp)
    sw t3, 44(sp)
    sw t2, 40(sp)
    sw t1, 36(sp)
    sw t0, 32(sp)
    sw a1, 28(sp)
    sw a0, 24(sp)
    sw ra, 20(sp)
    sw s0, 16(sp)
    sw s1, 12(sp)
    sw s2, 8(sp)
    sw s3, 4(sp)
    sw s4, 0(sp)

    mv s0, a1             # s0 = base address
    mv s1, a0             # s1 = n
    # Compute log2(n)
    mv t0, s1
    li s2, 0
    
# Function: log2 
# calculates log2 of a given number
# Input: size given as input in t0
# Output log2(size) outputted in s2

log2_loop:
    srli t0, t0, 1
    beq t0, zero, log2_done
    addi s2, s2, 1
    j log2_loop
log2_done:

    li s3, 1              # i = 1

reverse_loop:
    bge s3, s1, reverse_done

    mv a0, s3
    mv a1, s2
    jal bit_reverse_index
    mv s4, a0             # j

    bge s3, s4, next_index

    # Swap array[i] and array[j]
    slli t0, s3, 2
    add t0, s0, t0
    lw t1, 0(t0)

    slli t2, s4, 2
    add t2, s0, t2
    lw t3, 0(t2)

    sw t3, 0(t0)
    sw t1, 0(t2)

next_index:
    addi s3, s3, 1
    j reverse_loop

reverse_done:
    lw s4, 0(sp)
    lw s3, 4(sp)
    lw s2, 8(sp)
    lw s1, 12(sp)
    lw s0, 16(sp)
    lw ra, 20(sp)
    lw a0, 24(sp)
    lw a1, 28(sp)
    lw t0, 32(sp)
    lw t1, 36(sp)
    lw t2, 40(sp)
    lw t3, 44(sp)
    lw t4, 48(sp)
    addi sp, sp, 52
    ret


# === Bit Reverse Helper ===
# Reverses a single numbers binary digits
# Input: a single number in t1 register
# Output: reversed binary version of that number in a0
bit_reverse_index:
    li t0, 0
    mv t1, a0
    li t2, 0

reverse_bit_loop:
    beq t2, a1, reverse_bit_done
    andi t4, t1, 1
    slli t0, t0, 1
    or t0, t0, t4
    srli t1, t1, 1
    addi t2, t2, 1
    j reverse_bit_loop

reverse_bit_done:
    mv a0, t0
    ret

.data