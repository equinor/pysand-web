# functions to be used by the routes
import logging
from io import StringIO
from flask import request
from pysand import erosion
from data import materialDict, erosiveAgentDict
from forms import BaseForm, Bend, Tee, WeldedJoint, Reducer, Manifold, ChokeGallery, Probes, Flexible, NozzlevalveWall

def getErosionForm(erosion_model):
    
    if erosion_model == 'bend':
        form = Bend()
    elif erosion_model == 'tee':
        form = Tee()
    elif erosion_model == 'straight_pipe':
        form = BaseForm()
    elif erosion_model == 'welded_joint':
        form = WeldedJoint()
    elif erosion_model == 'manifold':
        form = Manifold()
    elif erosion_model == 'reducer':
        form = Reducer()
    elif erosion_model == 'probes':
        form = Probes()
    elif erosion_model == 'flexible':
        form = Flexible()
    elif erosion_model == 'choke_gallery':
        form = ChokeGallery()
    elif erosion_model == 'nozzlevalve_wall':
        form = NozzlevalveWall()
    
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


def calcRelErosion(erosion_model):
    # General input for all erosion models
    v_l_s = float(request.form['v_l_s'])
    v_g_s = float(request.form['v_g_s'])
    v_m = v_l_s + v_g_s

    D = float(request.form['internal_diameter'])

    erosive_agent = request.form['erosive_agent']

    material = request.form['material']

    if erosion_model in ['bend', 'tee', 'welded_joint', 'manifold', 'reducer', 'probes', 'flexible', 'choke_gallery']:
        rho_l = float(request.form['rho_l'])
        rho_g = float(request.form['rho_g'])
        if (v_l_s+v_g_s) > 0:
            rho_m = (rho_l * v_l_s + rho_g * v_g_s) / (v_l_s + v_g_s)
        else:
            rho_m = None

    if erosion_model in ['bend', 'tee', 'manifold', 'flexible', 'choke_gallery']:
        mu_l = float(request.form['mu_l'])
        mu_g = float(request.form['mu_g'])
        if (v_l_s+v_g_s) > 0:
            mu_m = (mu_l * v_l_s + mu_g * v_g_s) / (v_l_s + v_g_s)/1000  # convert to kg/ms
        else:
            mu_m = None
            
    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.WARNING)
    error = ''
    try:
        if erosion_model == 'bend':  
            E_rel = erosion.bend(
                v_m=v_m, 
                rho_m=rho_m, 
                mu_m=mu_m, 
                R=float(request.form['R']), 
                GF=float(request.form['GF']), 
                D=float(request.form['internal_diameter']), 
                d_p=float(request.form['particle_diameter']), 
                material=material, 
                rho_p=erosiveAgentDict[erosive_agent]['rho_p']
                )

        elif erosion_model == 'tee':
            E_rel = erosion.tee(
                v_m=v_m, 
                rho_m=rho_m, 
                mu_m=mu_m, 
                D=D, 
                GF=float(request.form['GF']), 
                d_p=float(request.form['particle_diameter']), 
                material=material, 
                rho_p=erosiveAgentDict[erosive_agent]['rho_p']
                )

        elif erosion_model == 'straight_pipe':
            E_rel = erosion.straight_pipe(
                v_m=v_m, 
                D=D
                )

        elif erosion_model == 'welded_joint':
            E_rel = erosion.welded_joint(
                v_m=v_m,
                rho_m=rho_m,
                D=D,
                d_p=float(request.form['particle_diameter']),
                h=float(request.form['h']),
                alpha=float(request.form['alpha']),
                location=request.form['Location'],
                material=material
            )

        elif erosion_model == 'manifold':
            E_rel = erosion.manifold(
                v_m=v_m, 
                rho_m=rho_m, 
                mu_m=mu_m, 
                GF=float(request.form['GF']), 
                D=D, 
                d_p=float(request.form['particle_diameter']), 
                Dm=float(request.form['Dman']), 
                rho_p=erosiveAgentDict[erosive_agent]['rho_p'], 
                material=material
                )

        elif erosion_model == 'reducer':
            E_rel = erosion.reducer(
                v_m=v_m, 
                rho_m=rho_m, 
                D1=D, 
                D2=float(request.form['D2']), 
                d_p=float(request.form['particle_diameter']), 
                GF=float(request.form['GF']), 
                alpha=float(request.form['alpha']), 
                material=material
                )

        elif erosion_model == 'probes':
            E_rel = erosion.probes(
                v_m=v_m,
                rho_m=rho_m,
                D=D,
                d_p=float(request.form['particle_diameter']),
                alpha=float(request.form['alpha']),
                material=material
                )

        elif erosion_model == 'flexible':
            E_rel = erosion.flexible(
                v_m=v_m,
                rho_m=rho_m,
                mu_m=mu_m,
                D=D,
                mbr=float(request.form['mbr']),
                d_p=float(request.form['particle_diameter']),
                material=material
                )
        
        elif erosion_model == 'choke_gallery':
            E_rel = erosion.choke_gallery(
                v_m=v_m,
                rho_m=rho_m,
                mu_m=mu_m,
                D=D, 
                GF=float(request.form['GF']),
                d_p=float(request.form['particle_diameter']),
                R_c=float(request.form['R_c']),
                gap=float(request.form['gap']),
                H=float(request.form['H']),
                material=material
            )

        elif erosion_model == 'nozzlevalve_wall':
            E_rel = erosion.nozzlevalve_wall(
                v_m=v_m,
                d_p=float(request.form['particle_diameter']),
                GF=float(request.form['GF']),
                At=float(request.form['At']),
                material=material
            )

        else:
            E_rel = -999

        status = 'Success'
        warning = log_stream.getvalue()
        

    except Exception as error:
        status = 'Error'
        warning = None
        error = error
        E_rel = -999
        return (format(E_rel, '.2E'), status, warning, error)
   
    return (format(E_rel, '.2E'), status, warning, error)
