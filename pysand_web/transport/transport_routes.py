from flask import Blueprint, render_template
from pysand_web.transport.transport_functions import getTransportForm, calcTransportVelocity
from pysand_web.transport.transport_data import transportModelsDict
from pysand import __version__ as pysand_version

transport_bp = Blueprint(
    'transport_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/transport/static'
    )

@transport_bp.route('/transport/<transport_model>', methods=['GET', 'POST'])
def transportform(transport_model):
    
    form = getTransportForm(transport_model)
    form.transport_model.data = transport_model
    model_comment = transportModelsDict[transport_model]['comment']

    if form.validate_on_submit():
        v0, v1, status, warning, error = calcTransportVelocity(transport_model)
        return render_template('transport_modal.html', pysand_version=pysand_version, form=form, transport_model=transport_model, v0=v0, v1=v1, status=status, warning=warning, error=error)

    return render_template('transport.html', pysand_version=pysand_version, form=form, transport_model=transport_model, model_comment=model_comment, active_page='transport')

