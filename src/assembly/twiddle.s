#define STDOUT 0xd0580000

.section .text
.global compute_twiddle_vector

# total length of pair in t3, calculate twiddle from s5 upto s5+t5
compute_twiddle_vector:
     li s7, 1024
     li a7, 1023
     li s8, 4
     fcvt.s.w f1, t3  # i in float
     fcvt.s.w f2, s7  # 1024 in float 
     fcvt.s.w f3, s8
     vid.v     v2                 # v2[k]=k for k=0...vlen-1
     vadd.vx v2, v2, s5           # v2[k] = (k+s)
     vfcvt.f.xu.v v2, v2
     vfdiv.vf v2, v2, f1           # v2[k] = (k+s)/i for k = 0,1...vlen-1
     vfmul.vf v2, v2, f2           # v2[k] = (k+s/i)*1024 for k = 0,1...vlen-1
     vfcvt.xu.f.v v3, v2           # convert from floats to int
     mv s7, s9
     vmv.v.x   v4, a7               # Fill v1 with the value 1023
     vand.vv   v5, v4, v3            # v2[i] = v3[i] & 1023
     vfmul.vf v5, v5, f3          # multiply by 4 for byte segmentation
     
     vluxei32.v v6, (s0), v5           # load multiple cosine values
     vluxei32.v v7, (s1), v5           # load multiple sin values
     
     vse32.v v6, (t1)             # store at t0(real part)
     vse32.v v7, (t2)             # store at t1(imag part)
     ret