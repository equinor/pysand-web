# functions to be used by the routes
import logging
from io import StringIO
from flask import request
from pysand import erosion
from data import materialDict, erosiveAgentDict


def getErosionForm(erosion_model):
    from forms import BaseForm, Bend, Reducer, BlindTee, Manifold

    if erosion_model == 'bend':
        form = Bend()
    elif erosion_model == 'reducer':
        form = Reducer()
    elif erosion_model == 'blindtee':
        form = BlindTee()
    elif erosion_model == 'smooth':
        form = BaseForm()
    elif erosion_model == 'manifold':
        form = Manifold()
    else:
        erosion_model = 'bend'
        form = Bend(formdata=None)  # Empty form, insert defaults
    return form


def getVariables(erosion_model=None):
    allVariables = {
        'internal_diameter': {'uom': 'mm', 'description': 'Internal diameter' }, 
        'particle_diameter': {'uom': 'mm', 'description': 'Particle diameter'}, 
        'material': {'uom': '', 'description': 'Material exposed to erosion'},
        'rho_p': {'uom': 'kg/m3', 'description': 'Particle density'},
        'q_sand' : {'uom': 'g/s', 'description': 'Sand production rate'}, 
        'rho_l': {'uom': 'kg/m3', 'description': 'Liquid density'}, 
        'mu_l': {'uom': 'kg/ms', 'description': 'Liquid viscosity'}, 
        'rho_g': {'uom': 'kg/m3', 'description': 'Gas density'}, 
        'mu_g': {'uom': 'kg/ms', 'description': 'Gas viscosity'}, 
        'v_l_s': {'uom': 'm/s', 'description': 'Superficial liquid velocity'}, 
        'v_g_s': {'uom': 'm/s', 'description': 'Superficial gas velocity'}, 
        'R': {'uom': '', 'description': 'Bend radius'}, 
        'GF': {'uom': '', 'description': 'Geometry factor'}, 
        'reduced_diameter': {'uom': 'm', 'description': 'Reduced diameter'}, 
        'alpha': {'uom': 'degrees'}, 
        'manifold_diameter': {'uom': 'm'},
        'h': {'uom': 'm', 'description': 'Height of weld'},
        'R_c': {'uom': 'm', 'description': 'Radius of choke gallery'},
        'gap': {'uom': 'm', 'description': 'Gap between the cage and choke body'},
        'H': {'uom': 'm', 'description': 'Height (effective) of gallery'},
        'location': {'uom': '', 'description': 'Location of erosion calculation'},
        'mbr': {'uom': '', 'description': 'Minimum bending radius in operation'},
        'At': {'uom': 'm2', 'description': 'Target area. Set to minimum flow area of the valve'}
        }

    bendDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_p', 'rho_l', 'mu_l', 'rho_g', 'mu_g', 'v_l_s', 'v_g_s', 'R', 'GF'}}
    teeDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_p', 'rho_l', 'mu_l', 'rho_g', 'mu_g', 'v_l_s', 'v_g_s', 'GF'}}
    straightDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'v_l_s', 'v_g_s'}}
    weldedDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'location', 'rho_l', 'rho_g', 'v_l_s', 'v_g_s', 'alpha'}}
    manifoldDict =  {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_p', 'rho_l', 'mu_l', 'rho_g', 'mu_g', 'v_l_s', 'v_g_s', 'manifold_diameter', 'GF'}}
    reducerDict =  {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_l', 'rho_g', 'v_l_s', 'v_g_s', 'reduced_diameter', 'GF', 'alpha'}}
    probeDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_l', 'rho_g', 'v_l_s', 'v_g_s', 'alpha'}}
    flexibleDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'rho_l', 'mu_l', 'rho_g', 'mu_g', 'v_l_s', 'v_g_s', 'mbr'}}
    chokeGalleryDict = {key: allVariables[key] for key in allVariables.keys()&{'internal_diameter', 'particle_diameter', 'material', 'R_c', 'rho_l', 'mu_l', 'rho_g', 'mu_g', 'v_l_s', 'v_g_s', 'gap', 'H', 'GF'}}
    nozzlevalveDict = {key: allVariables[key] for key in allVariables.keys()&{'particle_diameter', 'material', 'v_l_s', 'v_g_s', 'At', 'GF'}}

    if erosion_model == 'bend':
        return bendDict
    elif erosion_model == 'tee':
        return teeDict
    elif erosion_model == 'straight_pipe':
        return straightDict
    elif erosion_model == 'welded_joint':
        return weldedDict
    elif erosion_model == 'manifold':
        return manifoldDict
    elif erosion_model == 'reducer':
        return reducerDict
    elif erosion_model == 'probes':
        return probeDict
    elif erosion_model == 'flexible':
        return flexibleDict
    elif erosion_model == 'choke_gallery':
        return chokeGalleryDict
    elif erosion_model == 'nozzlevalve_wall':
        return nozzlevalveDict
    else:
        return bendDict

def materialProperties(material, returnvariable):

    properties = materialDict
    if material == 'list':
        return list(properties.keys())

    if material == 'properties':
        return properties

    return properties[material][returnvariable]


def calcRelErosion(form, erosion_model):
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
    d_p = float(request.form['particle_diameter'])

    erosive_agent = request.form['erosive_agent']
    rho_p = erosiveAgentDict[erosive_agent]['rho_p']

    material = request.form['material']

    #logger = logging.getLogger(erosion)
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.WARNING)

    try:
        if erosion_model == 'bend':  
            R = float(request.form['R'])
            GF = float(request.form['GF'])
            erosion_rate = erosion.bend(v_m, rho_m, mu_m, R, GF, D, d_p, material=material, rho_p=rho_p)
            
        elif erosion_model == 'reducer':
            GF = float(request.form['GF'])
            D2 = float(request.form['D2'])
            alpha = 60
            erosion_rate = erosion.reducer(v_m, rho_m, D, D2, d_p, GF=GF, alpha=alpha, material=material)

        elif erosion_model == 'blindtee':
            GF = float(request.form['GF'])
            D1 = D
            erosion_rate = erosion.tee(v_m, rho_m, mu_m, GF, D1, d_p, material=material, rho_p=rho_p)

        elif erosion_model == 'smooth':
            erosion_rate = erosion.straight_pipe(v_m, D)

        elif erosion_model == 'manifold':
            Dm = float(request.form['Dman'])
            GF = float(request.form['GF'])
            erosion_rate = erosion.manifold(v_m, rho_m, mu_m, GF, D, d_p, Dm, rho_p=rho_p, material=material)

        else:
            erosion_rate = -999

        status = 'success'
        warning = log_stream.getvalue()
        error = None

    except Exception as error:
        status = 'error'
        warning = None
        error = error
        erosion_rate = -999
        
   
    return (format(erosion_rate, '.2E'), status, warning, error)
