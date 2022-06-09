from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app
from pysand_web.erosion.erosion_functions import calcRelErosion, getErosionForm
from pysand_web.erosion.erosion_data import erosionModelsDict
from pysand import __version__ as pysand_version
from pysand.erosion import erosion_rate

erosion_bp = Blueprint(
    'erosion_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/erosion/static'
    )

@erosion_bp.route('/erosion/<erosion_model>', methods=['GET', 'POST'])
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

        return render_template('erosion_modal.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, title=status, 
        E_rel=E_rel, erosion_yearly=erosion_yearly, Q_s=Q_s, status=status, warnings=warning, error=error, active_page='erosion')

    return render_template('erosion.html', pysand_version=pysand_version, form=form, erosion_model=erosion_model, model_comment=model_comment, active_page='erosion')

# 2 error handling routes
@erosion_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@erosion_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500