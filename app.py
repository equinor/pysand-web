from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap4
from pysand import __version__ as pysand_version
from pysand.erosion import erosion_rate
from modules import calcRelErosion, getErosionForm, getVariables
from data import materialDict, erosionModelsDict

# Initialize Flask app and configure it
app = Flask(__name__)
app.config.from_object('config.ProdConfig')

# bootstrap-flask requires this line
Bootstrap4(app)


#####################
# Flask HTML routes #
#####################

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('erosionform', erosion_model='bend'))

@app.route('/erosion/<erosion_model>', methods=['GET', 'POST'])
def erosionform(erosion_model):

    form = getErosionForm(erosion_model)
    form.erosion_model.data = erosion_model
    model_comment = erosionModelsDict[erosion_model]['comment']
    Q_s = float(form.Q_s.data)

    if form.validate_on_submit():
        E_rel, status, warning, error = calcRelErosion(erosion_model)
        if (Q_s > 0 and float(E_rel) > 0):
            erosion_yearly = erosion_rate(float(E_rel), Q_s)
        else:
            erosion_yearly = 0

        return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, title=status, E_rel=E_rel, erosion_yearly=erosion_yearly, Q_s=Q_s, status=status, warnings=warning, error=error)

    return render_template('erosion.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, model_comment=model_comment)

# 2 error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


#####################
#  Flask API routes #
#####################
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
    matDict = materialDict

    if material != None:
        try:
            return matDict[material]
        except:
            return 'Material not found'
    else:
        return jsonify(matDict)


# keep this as is
if __name__ == '__main__':
    app.run()