import logging
from io import StringIO
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap4
from pysand import __version__ as pysand_version
from forms import BaseForm, Bend, Reducer, BlindTee, Manifold # TODO: remove after not needed
from modules import calcErosion, getErosionForm, getVariables, materialProperties

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object('config.ProdConfig')

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
    q_s = float(form.q_s.data)

    if form.validate_on_submit():
        try:
            log_stream = StringIO()
            logging.basicConfig(stream=log_stream, level=logging.WARNING)
            erosion_rate, erosion_rate_abs = calcErosion(form, erosion_model, q_s)
            warnings = log_stream.getvalue()
            
            return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, status='success', title='Calculation Successful', erosion_rate=erosion_rate, erosion_rate_abs = erosion_rate_abs, warnings=warnings)

        except Exception as error:
            app.logger.info(error)
            return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, status='failed', title='Error', error=error)


    return render_template('erosion.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model)


#  API routes below
@app.route('/api/erosion/<erosion_model>', methods=['GET'])
def erosioncalc(erosion_model):
    from pysand import erosion
    inputDict={'erosion_model': erosion_model, 'input': getVariables(erosion_model)}  # get all supported variables
    outputDict={'erosion_rate': {'uom': 'mm/ton'}}

    for variable in inputDict['input']:  
        inputDict['input'][variable]['value'] = request.args.get(variable)  # add input variables values to dictionary

    #inputOutputDict = {inputDict, 'output': outputDict}
    return jsonify(inputDict)

@app.route('/api/materials', methods=['GET'])
def getMaterials():
    material = request.args.get('material')
    matDict = materialProperties('properties')

    if material != None:
        try:
            return matDict[material]
        except:
            return 'Material not found'
    else:
        return jsonify(matDict)


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