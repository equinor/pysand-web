import logging
import os
from io import StringIO
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap4
from pysand import __version__ as pysand_version, erosion
from forms import BaseForm, Bend, Reducer, BlindTee, Manifold # TODO: remove after not needed
from modules import calcErosion, getErosionForm

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object('config.DevConfig')

# Flask-Bootstrap requires this line
Bootstrap4(app)

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('erosionform', erosion_model='bend'))

@app.route('/erosion/<erosion_model>', methods=['GET', 'POST'])
def erosionform(erosion_model):
    form = getErosionForm(erosion_model)
    form.erosion_model.data = erosion_model
    return render_template('erosion.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model)


@app.route('/calculate/<erosion_model>/<material>/<internal_diameter>/<erosive_agent>/<particle_diameter>', defaults={'material': 'quartz', })
def erosioncalc(erosion_model, material, internal_diameter, erosive_agent, particle_diameter):#, internal_diameter, particle_diameter, mass_sand, rho_l, mu_l, rho_g, mu_g, v_l_s, v_g_s, R, GF, D2, alpha, Dman):
    return jsonify(
        erosion_model = erosion_model,
        material = material,
        internal_diameter = float(internal_diameter),
        erosive_agent = erosive_agent,
        particle_diameter = float(particle_diameter)

    )  

@app.route('/erosion', methods=['GET', 'POST'])
def erosion():

    if request.method == 'POST':
        erosion_model = request.form['erosion_model']
        form = getErosionForm(erosion_model)
    else:
        erosion_model = 'bend'
        form = Bend(formdata=None)  # Empty form, insert defaults
     
    if form.validate_on_submit():
        
        try:
            log_stream = StringIO()   
            logging.basicConfig(stream=log_stream, level=logging.WARNING)
            erosion_rate = calcErosion(form, erosion_model)
            warnings = log_stream.getvalue()

            mass_sand = float(request.form['mass_sand'])
            if mass_sand > 0:
                erosion = mass_sand/1000 * erosion_rate  
            else:
                erosion = -999             
            
            return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, status='success', title='Calculation Successful', erosion_rate=erosion_rate, erosion=erosion, warnings=warnings)

        except Exception as error:
            app.logger.info(error)
            return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, status='failed', title='Error', error=error)

    else: 
        return render_template('erosion.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model)


# 2 routes to handle errors - they have templates too
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run()