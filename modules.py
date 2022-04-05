# functions to be used by the routes
#from app import erosion

def calcErosion(form, erosion_model):
    from flask import request
    from pysand.erosion import bend, reducer, tee, straight_pipe, manifold

    # General input for all erosion models
    v_l_s = float(request.form['v_l_s'])
    v_g_s = float(request.form['v_g_s'])
    v_m = v_l_s + v_g_s

    rho_l = float(request.form['rho_l'])
    rho_g = float(request.form['rho_g'])
    rho_m = (rho_l * v_l_s + rho_g * v_g_s) / (v_l_s + v_g_s)

    mu_l = float(request.form['mu_l'])
    mu_g = float(request.form['mu_g'])
    mu_m = (mu_l * v_l_s + mu_g * v_g_s) / (v_l_s + v_g_s)
    
    D = float(request.form['internal_diameter'])
    d_p = 0.1
    material = 'duplex'
    

    if erosion_model == 'bend':  
        R = float(request.form['R'])
        GF = float(request.form['GF'])
        rho_p = 2650
        return bend(v_m, rho_m, mu_m, R, GF, D, d_p, material=material, rho_p=2650)
    elif erosion_model == 'reducer':
        GF = float(request.form['GF'])
        D2 = float(request.form['D2'])
        return reducer(v_m, rho_m, D, D2, d_p, GF=GF, alpha=60, material=material)
    elif erosion_model == 'blindtee':
        GF = float(request.form['GF'])
        D1 = D
        rho_p = 2650
        return tee(v_m, rho_m, mu_m, GF, D1, d_p, material=material, rho_p=rho_p)
    elif erosion_model == 'smooth':
        return straight_pipe(v_m, D)
    elif erosion_model == 'manifold':
        Dm = float(request.form['Dman'])
        GF = float(request.form['GF'])
        rho_p = 2650
        return manifold(v_m, rho_m, mu_m, GF, D, d_p, Dm, rho_p=rho_p, material=material)
    else:
        return 1
