import numpy as np
import sympy
from sympy import Matrix
from individual import *

def get_jacobian(daccadIndiv, myarray, jikeiretu):
    jikeiretu_arr = [[float(a) for a in line.split(',')] for line in jikeiretu.split('\n')[3003:-1]]
    last_jikeiretu_arr = jikeiretu_arr[-1]
    jacobian = np.zeros([len(last_jikeiretu_arr), len(last_jikeiretu_arr)])

    nNodes = daccadIndiv.nb_nodes
    nTemplates = (len(last_jikeiretu_arr) - nNodes) // 5 # todo : inhibitor を考慮
    nInhibitors = 0  # todo : inhibitor を考慮
    
    myarray_activation = myarray[nNodes: nNodes + nNodes * nNodes].reshape([nNodes, nNodes])
    myarray_inhibition = myarray[nNodes + nNodes*nNodes:].reshape([nNodes, nNodes, nNodes])

    ### concentration of a, b, ...
    species = last_jikeiretu_arr[0: nNodes]

    ### Ka, Kb, ...
    K_species = myarray[0: nNodes]

    ### concentration of templates
    temp_alone = []
    temp_in = []
    temp_out = []
    temp_both = []
    temp_ext = []
    for i in range(nTemplates):
        temp_alone.append(last_jikeiretu_arr[i+nNodes])
        temp_in.append(last_jikeiretu_arr[i+nNodes+1])
        temp_out.append(last_jikeiretu_arr[i+nNodes+2])
        temp_both.append(last_jikeiretu_arr[i+nNodes+3])
        temp_ext.append(last_jikeiretu_arr[i+nNodes+4])

    ### constants
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
    
    stack = 0.2 # dimensionless
    
    ### d[s] / dt
    count_temp = 0
    ds_dt = [0] *nNodes

    ### d[template] / dt
    dtemplate_alone_dt = [0] *nTemplates
    dtemplate_in_dt = [0] *nTemplates
    dtemplate_out_dt = [0] *nTemplates
    dtemplate_both_dt = [0] *nTemplates
    dtemplate_ext_dt = [0] *nTemplates

    ## set sympols
    species_sympol = []
    temp_alone_sympol = []
    temp_in_sympol = []
    temp_out_sympol = []
    temp_both_sympol = []
    temp_ext_sympol = []

    for i in range(nNodes):
        species_sympol.append(sympy.Symbol('species_' + str(i)))

    for i in range(nTemplates):
        temp_alone_sympol.append(sympy.Symbol('temp_alone_' + str(i)))
        temp_in_sympol.append(sympy.Symbol('temp_in_' + str(i)))
        temp_out_sympol.append(sympy.Symbol('temp_out_' + str(i)))
        temp_both_sympol.append(sympy.Symbol('temp_both_' + str(i)))
        temp_ext_sympol.append(sympy.Symbol('temp_ext_' + str(i)))

    ### set exprs
    for i in range(nNodes): # in
        for j in range(nNodes): # out
            if myarray_activation[i, j] != 0: # nTemplates 回該当する

                pol = polVm / (polKm * (1 + temp_in_sympol[count_temp] / polKm + temp_both_sympol[count_temp] / polKmBoth))
                pol_both = polVm / (polKmBoth * (1 + temp_in_sympol[count_temp] / polKm + temp_both_sympol[count_temp] / polKmBoth))
                pol_displ = pol_both * displ
                exo = exoVm / (exoKmSimple * (1 + species[i] / exoKmSimple))
                nick = nickVm / (nickKm + temp_ext_sympol[count_temp])

                # activation : i -> j
                # pht_in
                ds_dt[i] += kdup*(K_species[i]*(temp_in_sympol[count_temp]+stack*temp_both_sympol[count_temp])-(temp_alone_sympol[count_temp]+temp_out_sympol[count_temp])*species_sympol[i])
                # phi_out
                ds_dt[j] += kdup*(K_species[j]*(temp_out_sympol[count_temp]+stack*temp_both_sympol[count_temp])-(temp_alone_sympol[count_temp]+temp_in_sympol[count_temp])*species_sympol[j])

                dtemplate_alone_dt[count_temp] = kdup*(K_species[i]*temp_in_sympol[count_temp]+K_species[j]*temp_out_sympol[count_temp]-(species_sympol[i]+species_sympol[j])*temp_alone_sympol[count_temp])
                dtemplate_in_dt[count_temp] = kdup*(species_sympol[i]*temp_alone_sympol[count_temp]+K_species[j]*stack*temp_both_sympol[count_temp]-temp_in_sympol[count_temp]*(species_sympol[j]+K_species[i]))-pol*temp_in_sympol[count_temp]
                dtemplate_out_dt[count_temp] = kdup*(species_sympol[j]*temp_alone_sympol[count_temp]+K_species[i]*stack*temp_both_sympol[count_temp]-temp_out_sympol[count_temp]*(species_sympol[i]+K_species[j]))
                dtemplate_both_dt[count_temp] = kdup*(species_sympol[i]*temp_out_sympol[count_temp]+species_sympol[j]*temp_out_sympol[count_temp]-stack*temp_both_sympol[count_temp]*(K_species[i]+K_species[j]))
                dtemplate_ext_dt[count_temp] = pol*temp_in_sympol[count_temp]+pol_both*temp_out_sympol[count_temp]+nick*temp_ext_sympol[count_temp]
                
                count_temp += 1

    for i in range(nNodes):
        ds_dt[i] -= exo * species_sympol[i]
    
    ### calculate jacobian matrix
    # https://docs.sympy.org/latest/modules/matrices/matrices.html#sympy.matrices.matrices.MatrixCalculus.jacobian
    x = []
    for i in range(nNodes):
        x.append(ds_dt[i])
    for i in range(nTemplates):
        x.append(dtemplate_alone_dt[i])
        x.append(dtemplate_in_dt[i])
        x.append(dtemplate_out_dt[i])
        x.append(dtemplate_both_dt[i])
        x.append(dtemplate_ext_dt[i])
    X = Matrix(x)
    
    y = []
    for i in range(nNodes):
        y.append(species_sympol[i])
    for i in range(nTemplates):
        y.append(temp_alone_sympol[i])
        y.append(temp_in_sympol[i])
        y.append(temp_out_sympol[i])
        y.append(temp_both_sympol[i])
        y.append(temp_ext_sympol[i])
    Y = Matrix(y)
    
    jacobian = X.jacobian(Y)

    ### substrate each value
    for i in range(nNodes):
        jacobian = jacobian.subs(species_sympol[i], species[i])
    for i in range(nTemplates):
        jacobian = jacobian.subs(temp_alone_sympol[i], temp_alone[i])
        jacobian = jacobian.subs(temp_in_sympol[i], temp_in[i])
        jacobian = jacobian.subs(temp_out_sympol[i], temp_out[i])
        jacobian = jacobian.subs(temp_both_sympol[i], temp_both[i])
        jacobian = jacobian.subs(temp_ext_sympol[i], temp_ext[i])
    jacobian = np.array(jacobian)
    jacobian = np.array(jacobian, dtype=float)
    
    """
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

    for i in range(nTemplates):

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
    """

    return jacobian

