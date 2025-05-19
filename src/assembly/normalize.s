#define STDOUT 0xd0580000

.section .text
.global normalize_values

# Function: normalize_values
# computes the normalized version of real and imaginary values as the formuale output[[i] = sqrt( real[i]^2 + imag[i]^2 )
# Input: arrays for real and imaginary values are provided in a1 and a3
# Output: a normalized arrays of values given in a1

normalize_values:
     vsetvli t0, a0, e32, m1
     li t4, 0
     slli t5, t0, 2  # VLEN * 4  mem offset
normalize_loop:
     bge t4, a0, end_normalize
     
     vle32.v v1, (a1)    # load real values
     vle32.v v2, (a3)    # load imag values
     
     vfmul.vv v3, v1, v1  # (real[i])^2
     vfmul.vv v4, v2, v2  # (imag[i])^2
     
     vfadd.vv v5, v3, v4  # real^2 + imag^2
     
     vfsqrt.v v6, v5  # sqrt( real^2 + imag^2 )
      
     vse32.v v6, (a1)  # store the normalized vals
     
     add a1, a1, t5    # update pointers
     add a3, a3, t5    # update pointers
     
     add t4, t4, t0  # t4 = t4 + vlen  
     
     j normalize_loop
end_normalize:

   ret
    
.data