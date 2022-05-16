import numpy as np

def get_jacobian(myarray, jikeiretu_arr):
    jacobian = np.zeros([len(jikeiretu_arr[0]), len(jikeiretu_arr[0])])

    a = jikeiretu_arr[0]
    b = jikeiretu_arr[1]
    for i in range((len(jikeiretu_arr[0]) - 2) // 5):
        temp_alone = jikeiretu_arr[i+2]
        temp_in = jikeiretu_arr[i+3]
        temp_out = jikeiretu_arr[i+4]
        temp_both = jikeiretu_arr[i+5]
        temp_ext = jikeiretu_arr[i+6]

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

    for i in range((len(jikeiretu_arr[0]) - 2) // 5):

        # ~ / d[temp_alone]
        jacobian[i+2, 0] = -kdup * temp_alone
        jacobian[i+2, 1] = -kdup * temp_alone
        jacobian[i+2, 2] = -kdup * (a * b)
        jacobian[i+2, 3] = kdup * Ka
        jacobian[i+2, 4] = kdup * Kb
        jacobian[i+2, 5] = 0
        jacobian[i+2, 6] = 0

        # ~ / d[temp_in]
        jacobian[i+3, 0] = kdup * temp_alone
        jacobian[i+3, 1] = -kdup * temp_in
        jacobian[i+3, 2] = kdup * a
        jacobian[i+3, 3] = -kdup * (b + Ka) - pol
        jacobian[i+3, 4] = 0
        jacobian[i+3, 5] = kdup * Kb * stack
        jacobian[i+3, 6] = 0

        # ~ / d[temp_out]
        jacobian[i+4, 0] = -kdup * temp_out
        jacobian[i+4, 1] = kdup * temp_alone
        jacobian[i+4, 2] = kdup * b
        jacobian[i+4, 3] = 0
        jacobian[i+4, 4] = -kdup * (a + Kb)
        jacobian[i+4, 5] = kdup * Ka * stack
        jacobian[i+4, 6] = 0

        # ~ / d[temp_both]
        jacobian[i+5, 0] = kdup * temp_out
        jacobian[i+5, 1] = kdup * temp_out
        jacobian[i+5, 2] = 0
        jacobian[i+5, 3] = 0
        jacobian[i+5, 4] = kdup * (a + b)
        jacobian[i+5, 5] = -kdup * stack * (Ka + Kb)
        jacobian[i+5, 6] = 0

        # ~ / d[temp_ext]
        jacobian[i+6, 0] = 0
        jacobian[i+6, 1] = 0
        jacobian[i+6, 2] = 0
        jacobian[i+6, 3] = pol
        jacobian[i+6, 4] = pol_both
        jacobian[i+6, 5] = 0
        jacobian[i+6, 6] = nick

    return jacobian

