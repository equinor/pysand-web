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
    v = []

    try:
        if transport_model == 'stokes':
            rho_m = float(request.form['rho_m'])
            mu_m = float(request.form['mu_m'])
            angle = float(request.form['angle'])
            v[0] = stokes(rho_m=rho_m, mu_m=mu_m, d_p=d_p, angle=angle, rho_p=rho_p)
            v[1] = -999

        elif transport_model == 'hydro':
            D = float(request.form['D'])
            rho_l = float(request.form['rho_l'])
            mu_l = float(request.form['mu_l'])
            e = float(request.form['e'])
            v[0:2] = hydro(D=D, rho_l=rho_l, mu_l=mu_l, d_p=d_p, e=e, rho_p=rho_p)
        
        else:
            v = -999
        status = 'Success'
        warning = log_stream.getvalue()
    
    except Exception as error:
        status = 'Error'
        warning = None
        error = error
        v[0:2] = -999
        return (format(v, '.2E'), status, warning, error)

    return (format(v[0], '.2E'), format(v[1], '.2E'), status, warning, error)
   
    


