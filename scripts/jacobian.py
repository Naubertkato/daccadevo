import numpy as np
import sympy
import math
from sympy import Matrix
from individual import *

def get_jacobian(daccadIndiv, myarray, jikeiretu):
    jikeiretu_arr = [[float(a) for a in line.split(',')] for line in jikeiretu.split('\n')[3003:-1]]
    last_jikeiretu_arr = jikeiretu_arr[-1]
    jacobian = np.zeros([len(last_jikeiretu_arr), len(last_jikeiretu_arr)])

    nNodes = daccadIndiv.nb_nodes
    nTemplates = len([a for a in myarray[nNodes: nNodes + nNodes * nNodes] if a != 0])
    nInhibitors = len([a for a in myarray[nNodes + nNodes*nNodes:] if a != 0])
    
    myarray_activation = myarray[nNodes: nNodes + nNodes * nNodes].reshape([nNodes, nNodes])
    myarray_inhibition = myarray[nNodes + nNodes*nNodes:].reshape([nNodes, nNodes, nNodes])

    ### concentration of a, b, ...
    species = last_jikeiretu_arr[0: nNodes]
    
    ### concentration of inhibitors
    inhibitors = last_jikeiretu_arr[nNodes: nNodes+nInhibitors]

    ### Ka, Kb, Ki...
    K_species = myarray[0: nNodes]
    for i in range(nInhibitors):
        for j in range(nInhibitors):
            for k in range(nInhibitors):
                if myarray_inhibition[i, j, k] != 0: # nInhibitors 回該当する
                    K_inhibitors = 1 / 100 * math.exp((math.log(K_species[i]) + math.log(K_species[k])) / 2)

    ### concentration of templates
    temp_alone = []
    temp_in = []
    temp_out = []
    temp_both = []
    temp_ext = []
    temp_inhib = []
    for i in range(nTemplates):
        temp_alone.append(last_jikeiretu_arr[i*5 + (nNodes+nInhibitors)])
        temp_in.append(last_jikeiretu_arr[i*5 + 1 + (nNodes+nInhibitors)])
        temp_out.append(last_jikeiretu_arr[i*5 + 2 +(nNodes+nInhibitors)])
        temp_both.append(last_jikeiretu_arr[i*5 + 3 + (nNodes+nInhibitors)])
        temp_ext.append(last_jikeiretu_arr[i*5 + 4 + (nNodes+nInhibitors)])

    for i in range(nInhibitors):
        temp_alone.append(last_jikeiretu_arr[i*6 + nTemplates*5 + nNodes+nInhibitors])
        temp_in.append(last_jikeiretu_arr[i*6 + + nTemplates*5 +nNodes+nInhibitors+1])
        temp_out.append(last_jikeiretu_arr[i*6  + nTemplates*5 +nNodes+nInhibitors+2])
        temp_both.append(last_jikeiretu_arr[i*6  + nTemplates*5 +nNodes+nInhibitors+3])
        temp_ext.append(last_jikeiretu_arr[i*6  + nTemplates*5 +nNodes+nInhibitors+4])
        temp_inhib.append(last_jikeiretu_arr[i*6  + nTemplates*5 +nNodes+nInhibitors+4])


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

    alpha = 3
    labmda_in = 0.002
    lambda_out = 0.01
    
    ### d[s] / dt
    ds_dt = [0] * nNodes

    ### d[i] / dt
    di_dt = [0] * nInhibitors

    ### d[template] / dt
    dtemplate_alone_dt = [0] *(nTemplates + nInhibitors)
    dtemplate_in_dt = [0] *(nTemplates + nInhibitors)
    dtemplate_out_dt = [0] *(nTemplates + nInhibitors)
    dtemplate_both_dt = [0] *(nTemplates + nInhibitors)
    dtemplate_ext_dt = [0] *(nTemplates + nInhibitors)
    dtemplate_inhib_dt = [0] *nInhibitors

    ## set symbols
    species_symbol = []
    inhibitors_symbol = []
    temp_alone_symbol = []
    temp_in_symbol = []
    temp_out_symbol = []
    temp_both_symbol = []
    temp_ext_symbol = []
    temp_inhib_symbol = []

    for i in range(nNodes):
        species_symbol.append(sympy.Symbol('species_' + str(i)))

    for i in range(nInhibitors):
        inhibitors_symbol.append(sympy.Symbol('inhibitors_' + str(i)))

    for i in range(nTemplates+nInhibitors):
        temp_alone_symbol.append(sympy.Symbol('temp_alone_' + str(i)))
        temp_in_symbol.append(sympy.Symbol('temp_in_' + str(i)))
        temp_out_symbol.append(sympy.Symbol('temp_out_' + str(i)))
        temp_both_symbol.append(sympy.Symbol('temp_both_' + str(i)))
        temp_ext_symbol.append(sympy.Symbol('temp_ext_' + str(i)))

    for i in range(nInhibitors):
        temp_inhib_symbol.append(sympy.Symbol('temp_inhib_' + str(i)))
    
    ### set exprs
    count_temp = 0
    for i in range(nNodes): # in
        for j in range(nNodes): # out
            if myarray_activation[i, j] != 0: # nTemplates 回該当する

                pol = polVm / (polKm * (1 + temp_in_symbol[count_temp] / polKm + temp_both_symbol[count_temp] / polKmBoth))
                pol_both = polVm / (polKmBoth * (1 + temp_in_symbol[count_temp] / polKm + temp_both_symbol[count_temp] / polKmBoth))
                pol_displ = pol_both * displ
                exo = exoVm / (exoKmSimple * (1 + species[i] / exoKmSimple))
                nick = nickVm / (nickKm + temp_ext_symbol[count_temp])

                # activation : i -> j
                # pht_in
                ds_dt[i] += kdup*(K_species[i]*(temp_in_symbol[count_temp]+stack*temp_both_symbol[count_temp])-(temp_alone_symbol[count_temp]+temp_out_symbol[count_temp])*species_symbol[i])
                # phi_out
                ds_dt[j] += kdup*(K_species[j]*(temp_out_symbol[count_temp]+stack*temp_both_symbol[count_temp])-(temp_alone_symbol[count_temp]+temp_in_symbol[count_temp])*species_symbol[j])+pol_displ*temp_both_symbol[count_temp]

                dtemplate_alone_dt[count_temp] = kdup*(K_species[i]*temp_in_symbol[count_temp]+K_species[j]*temp_out_symbol[count_temp]-(species_symbol[i]+species_symbol[j])*temp_alone_symbol[count_temp])
                dtemplate_in_dt[count_temp] = kdup*(species_symbol[i]*temp_alone_symbol[count_temp]+K_species[j]*stack*temp_both_symbol[count_temp]-temp_in_symbol[count_temp]*(species_symbol[j]+K_species[i]))-pol*temp_in_symbol[count_temp]
                dtemplate_out_dt[count_temp] = kdup*(species_symbol[j]*temp_alone_symbol[count_temp]+K_species[i]*stack*temp_both_symbol[count_temp]-temp_out_symbol[count_temp]*(species_symbol[i]+K_species[j]))
                dtemplate_both_dt[count_temp] = kdup*(species_symbol[i]*temp_out_symbol[count_temp]+species_symbol[j]*temp_out_symbol[count_temp]-stack*temp_both_symbol[count_temp]*(K_species[i]+K_species[j]))
                dtemplate_ext_dt[count_temp] = pol*temp_in_symbol[count_temp]+pol_both*temp_out_symbol[count_temp]+nick*temp_ext_symbol[count_temp]
                
                count_temp += 1
    
    count_inhib = 0
    for i in range(nInhibitors):
        for j in range(nInhibitors):
            for k in range(nInhibitors):
                if myarray_inhibition[i, j, k] != 0: # nInhibitors 回該当する

                    pol = polVm / (polKm * (1 + temp_in_symbol[count_temp] / polKm + temp_both_symbol[count_temp] / polKmBoth))
                    pol_both = polVm / (polKmBoth * (1 + temp_in_symbol[count_temp] / polKm + temp_both_symbol[count_temp] / polKmBoth))
                    pol_displ = pol_both * displ
                    nick = nickVm / (nickKm + temp_ext_symbol[count_temp])

                    #in
                    ds_dt[i] += kdup*(K_species[i]*(temp_in_symbol[count_temp]+stack*temp_both_symbol[count_temp])-(temp_alone_symbol[count_temp]+temp_out_symbol[count_temp])*species_symbol[i]+(inhibitors_symbol[count_inhib]*temp_in_symbol[count_temp]-labmda_in*species_symbol[i]*temp_inhib_symbol[count_inhib]))
                    
                    #out
                    di_dt[count_inhib] += kdup*(K_species[k]*(temp_out_symbol[count_temp]+stack*temp_both_symbol[count_temp])-(temp_alone_symbol[count_temp]+temp_in_symbol[count_temp])*species_symbol[k]+(inhibitors_symbol[count_inhib]*temp_out_symbol[count_temp]-lambda_out*species_symbol[k]*temp_inhib_symbol[count_inhib]))+pol_displ*temp_both_symbol[count_temp]
                    
                    #inhib
                    di_dt[count_inhib] += alpha*kdup*K_species[j]*temp_inhib_symbol[count_inhib]-kdup*inhibitors_symbol[count_inhib]*(temp_alone_symbol[count_temp]+temp_in_symbol[count_temp]+temp_out_symbol[count_temp])+kdup*temp_inhib_symbol[count_inhib]*(labmda_in*species_symbol[j]+lambda_out*species_symbol[k])

                    dtemplate_alone_dt[count_temp] = kdup*(K_species[j]*temp_in_symbol[count_temp]+K_species[k]*temp_out_symbol[count_temp]-(species_symbol[j]+species_symbol[k])*temp_alone_symbol[count_temp]+K_inhibitors[count_inhib]*temp_inhib_symbol[count_inhib]-inhibitors_symbol[count_inhib]*temp_alone_symbol[count_temp])
                    dtemplate_in_dt[count_temp] = kdup*(species_symbol[j]*temp_alone_symbol[count_temp]+K_species[k]*stack*temp_both_symbol[count_temp]-temp_in_symbol[count_temp]*(species_symbol[k]+K_species[j])+labmda_in*species_symbol[k]*temp_inhib_symbol[count_inhib]-inhibitors_symbol[count_inhib]*temp_in_symbol[count_temp])-pol*temp_in_symbol[count_temp]
                    dtemplate_out_dt[count_temp] = kdup*(species_symbol[k]*temp_alone_symbol[count_temp]+K_species[j]*stack*temp_both_symbol[count_temp]-temp_out_symbol[count_temp]*(species_symbol[j]+K_species[k])+lambda_out*species_symbol[k]*temp_inhib_symbol[count_inhib]-inhibitors_symbol[count_inhib]*temp_out_symbol[count_temp])
                    dtemplate_both_dt[count_temp] = kdup*(species_symbol[j]*temp_out_symbol[count_temp]+species_symbol[k]*temp_out_symbol[count_temp]-stack*temp_both_symbol[count_temp]*(K_species[j]+K_species[k]))+nick*temp_ext_symbol[count_temp]-pol_both*temp_both_symbol[count_temp]
                    dtemplate_ext_dt[count_temp] = pol*temp_in_symbol[count_temp]+pol_both*temp_out_symbol[count_temp]+nick*temp_ext_symbol[count_temp]
                    dtemplate_inhib_dt[count_temp] = kdup*inhibitors_symbol[count_inhib]*(temp_alone_symbol[count_temp]+temp_in_symbol[count_temp]+temp_out_symbol[count_temp])-kdup*temp_inhib_symbol[count_inhib]*(K_inhibitors[count_inhib]+labmda_in*species_symbol[j]+lambda_out*species_symbol[k])

                    count_temp += 1
                    count_inhib += 1
    
    for i in range(nNodes):
        exo = exoVm / (exoKmSimple * (1 + species_symbol[i] / exoKmSimple))
        ds_dt[i] -= exo * species_symbol[i]

    for i in range(nInhibitors):
        exo = exoVm / (exoKmSimple * (1 + inhibitors_symbol[i] / exoKmSimple))
        di_dt[i] -= exo * inhibitors_symbol[i]
    
    ### calculate jacobian matrix
    # https://docs.sympy.org/latest/modules/matrices/matrices.html#sympy.matrices.matrices.MatrixCalculus.jacobian
    x = []
    for i in range(nNodes):
        x.append(ds_dt[i])
    for i in range(nInhibitors):
        x.append(di_dt[i])
    for i in range(nTemplates):
        x.append(dtemplate_alone_dt[i])
        x.append(dtemplate_in_dt[i])
        x.append(dtemplate_out_dt[i])
        x.append(dtemplate_both_dt[i])
        x.append(dtemplate_ext_dt[i])
    for i in range(nInhibitors):
        x.append(dtemplate_alone_dt[nTemplates+i])
        x.append(dtemplate_in_dt[nTemplates+i])
        x.append(dtemplate_out_dt[nTemplates+i])
        x.append(dtemplate_both_dt[nTemplates+i])
        x.append(dtemplate_ext_dt[nTemplates+i])
        x.append(dtemplate_inhib_dt[i])
    X = Matrix(x)
    
    y = []
    for i in range(nNodes):
        y.append(species_symbol[i])
    for i in range(nInhibitors):
        y.append(inhibitors_symbol[i])
    for i in range(nTemplates):
        y.append(temp_alone_symbol[i])
        y.append(temp_in_symbol[i])
        y.append(temp_out_symbol[i])
        y.append(temp_both_symbol[i])
        y.append(temp_ext_symbol[i])
    for i in range(nInhibitors):
        y.append(temp_alone_symbol[nTemplates+i])
        y.append(temp_in_symbol[nTemplates+i])
        y.append(temp_out_symbol[nTemplates+i])
        y.append(temp_both_symbol[nTemplates+i])
        y.append(temp_ext_symbol[nTemplates+i])
        y.append(temp_inhib_symbol[i])

    Y = Matrix(y)
    
    jacobian = X.jacobian(Y)

    ### substrate each value
    for i in range(nNodes):
        jacobian = jacobian.subs(species_symbol[i], species[i])
    for i in range(nInhibitors):
        jacobian = jacobian.subs(inhibitors_symbol[i], inhibitors[i])
    for i in range(nTemplates):
        jacobian = jacobian.subs(temp_alone_symbol[i], temp_alone[i])
        jacobian = jacobian.subs(temp_in_symbol[i], temp_in[i])
        jacobian = jacobian.subs(temp_out_symbol[i], temp_out[i])
        jacobian = jacobian.subs(temp_both_symbol[i], temp_both[i])
        jacobian = jacobian.subs(temp_ext_symbol[i], temp_ext[i])
    for i in range(nInhibitors):
        jacobian = jacobian.subs(temp_alone_symbol[nTemplates+i], temp_alone[nTemplates+i])
        jacobian = jacobian.subs(temp_in_symbol[nTemplates+i], temp_in[nTemplates+i])
        jacobian = jacobian.subs(temp_out_symbol[nTemplates+i], temp_out[nTemplates+i])
        jacobian = jacobian.subs(temp_both_symbol[nTemplates+i], temp_both[nTemplates+i])
        jacobian = jacobian.subs(temp_ext_symbol[nTemplates+i], temp_ext[nTemplates+i])
        jacobian = jacobian.subs(temp_inhib_symbol[i], temp_inhib[i])
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

