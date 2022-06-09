from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app
from pysand_web.erosion.erosion_functions import calcRelErosion, getErosionForm
from pysand_web.erosion.erosion_data import erosionModelsDict
from pysand import __version__ as pysand_version
from pysand.erosion import erosion_rate

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static'
    )

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('erosion_bp.erosionform', erosion_model='bend'))

