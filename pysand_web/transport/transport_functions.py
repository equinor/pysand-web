import logging
from io import StringIO
from pysand_web.transport.transport_forms import TransportStokesForm, TransportHydroForm
from pysand.transport import stokes, hydro
from flask import request

def getTransportForm(transport_model='hydro'):
    if transport_model == 'stokes':
        form = TransportStokesForm()
    else:
        transport_model = 'hydro'
        form = TransportHydroForm(formdata=None)  # Empty form, insert defaults
    return form


def calcTransportVelocity(transport_model='hydro'):
    # general input all transport models
    d_p = float(request.form['d_p'])
    rho_p = float(request.form['rho_p'])

    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.WARNING)
    error = ''

    try:
        if transport_model == 'stokes':
            rho_m = float(request.form['rho_m'])
            mu_m = float(request.form['mu_m'])/1000  # convert to kg/ms
            angle = float(request.form['angle'])
            v1 = (stokes(rho_m=rho_m, mu_m=mu_m, d_p=d_p, angle=angle, rho_p=rho_p))
            v2 = -999.0

        elif transport_model == 'hydro':
            D = float(request.form['D'])
            rho_l = float(request.form['rho_l'])
            mu_l = float(request.form['mu_l'])/1000  # convert to kg/ms
            e = float(request.form['e'])
            v1, v2 = hydro(D=D, rho_l=rho_l, mu_l=mu_l, d_p=d_p, e=e, rho_p=rho_p)
        
        else:
            v1 = v2 = -999.0
        
        status = 'Success'
        warning = log_stream.getvalue()
    
    except Exception as error:
        status = 'Error'
        warning = None
        error = error
        v1 = v2 = -999.0
        return (format(v1, '.2f'), format(v2, '.2f'), status, warning, error)

    return (format(v1, '.2f'), format(v2, '.2f'), status, warning, error)
   
    
