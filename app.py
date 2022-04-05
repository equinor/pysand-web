import logging
import os
from io import StringIO
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from pysand import __version__ as pysand_version
from forms import BaseForm, Bend, Reducer, BlindTee, Manifold
from modules import calcErosion

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object('config.DevConfig')

# Flask-Bootstrap requires this line
Bootstrap(app)

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('erosion'))


@app.route('/erosion', methods=['GET', 'POST'])
def erosion():

    if request.method == 'POST':
        erosion_model = request.form['erosion_model']
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