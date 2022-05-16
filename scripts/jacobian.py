import numpy as np

def get_jacobian(myarray, jikeiretu_arr):
    jacobian = np.zeros([7, 7])

    a = jikeiretu_arr[0]
    b = jikeiretu_arr[1]
    a_b_alone = jikeiretu_arr[2]
    a_b_in = jikeiretu_arr[3]
    a_b_out = jikeiretu_arr[4]
    a_b_both = jikeiretu_arr[5]
    a_b_ext = jikeiretu_arr[6]

    # constants
    polVm = 1050
    polKm = 80
    polKmBoth = 5.5

    exoVm = 300
    exoKmSimple = 440
    exoKmInhib = 150
    exoKmTemplate = 10

    nickVm = 80
    nickKm = 30
    nickKmBoth = nickKm

    kdup = 0.2
    displ = 0.2

    Ka = myarray[0]
    Kb = myarray[1]
    
    stack = 0.2 # dimensionless
    pol = polVm / (polKm * (1 + a_b_in / polKm + a_b_both / polKmBoth))
    pol_both = polVm / (polKmBoth * (1 + a_b_in / polKm + a_b_both / polKmBoth))
    pol_displ = pol_both * displ
    exo = exoVm / (exoKmSimple * (1 + a / exoKmSimple))
    nick = nickVm / (nickKm + a_b_ext)

    # a, b, alone, in, out, both, ext
    # ~ / d[a]
    jacobian[0, 0] = -kdup * (a_b_alone + a_b_out) - exo
    jacobian[0, 1] = 0
    jacobian[0, 2] = -kdup * a
    jacobian[0, 3] = kdup * Ka
    jacobian[0, 4] = -kdup * a
    jacobian[0, 5] = kdup * Ka * stack
    jacobian[0, 6] = 0 

    # ~ / d[b]
    jacobian[1, 0] = 0
    jacobian[1, 1] = -kdup * (a_b_alone + a_b_in) - exo
    jacobian[1, 2] = -kdup * b
    jacobian[1, 3] = -kdup * b
    jacobian[1, 4] = kdup * Kb
    jacobian[1, 5] = kdup * stack + pol_displ
    jacobian[1, 6] = 0

    # ~ / d[a_b_alone]
    jacobian[2, 0] = -kdup * a_b_alone
    jacobian[2, 1] = -kdup * a_b_alone
    jacobian[2, 2] = -kdup * (a * b)
    jacobian[2, 3] = kdup * Ka
    jacobian[2, 4] = kdup * Kb
    jacobian[2, 5] = 0
    jacobian[2, 6] = 0

    # ~ / d[a_b_in]
    jacobian[3, 0] = kdup * a_b_alone
    jacobian[3, 1] = -kdup * a_b_in
    jacobian[3, 2] = kdup * a
    jacobian[3, 3] = -kdup * (b + Ka) - pol
    jacobian[3, 4] = 0
    jacobian[3, 5] = kdup * Kb * stack
    jacobian[3, 6] = 0

    # ~ / d[a_b_out]
    jacobian[4, 0] = -kdup * a_b_out
    jacobian[4, 1] = kdup * a_b_alone
    jacobian[4, 2] = kdup * b
    jacobian[4, 3] = 0
    jacobian[4, 4] = -kdup * (a + Kb)
    jacobian[4, 5] = kdup * Ka * stack
    jacobian[4, 6] = 0

    # ~ / d[a_b_both]
    jacobian[5, 0] = kdup * a_b_out
    jacobian[5, 1] = kdup * a_b_out
    jacobian[5, 2] = 0
    jacobian[5, 3] = 0
    jacobian[5, 4] = kdup * (a + b)
    jacobian[5, 5] = -kdup * stack * (Ka + Kb)
    jacobian[5, 6] = 0

    # ~ / d[a_b_ext]
    jacobian[6, 0] = 0
    jacobian[6, 1] = 0
    jacobian[6, 2] = 0
    jacobian[6, 3] = pol
    jacobian[6, 4] = pol_both
    jacobian[6, 5] = 0
    jacobian[6, 6] = nick

    return jacobian

