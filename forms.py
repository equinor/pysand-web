from lib2to3.pytree import Base
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from data import materials_tuples, erosion_models_tuples

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot

class ErosionModel(FlaskForm):
    erosion_model = SelectField('Select erosion model', choices=erosion_models_tuples, validators=[DataRequired()])

class BaseForm(FlaskForm):
    # Geometry and material
    erosion_model = SelectField('Select erosion model', default='bend', choices=erosion_models_tuples, validators=[DataRequired()])
    material = SelectField('Select material', choices=materials_tuples, validators=[DataRequired()])
    internal_diameter = DecimalField('Inner diameter (D) [m]', default=0.1, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    
    # Erosive agents
    erosive_agent = SelectField('Select erosive agent', default='quartz', choices=[('quartz', 'Quartz sand')], validators=[DataRequired()])
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    q_s = DecimalField('Sand production rate [g/s]', default=0.1)

    # PVT input
    rho_l = DecimalField('Liquid Density [kg/m³]', default=1000, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    mu_l = DecimalField('Liquid Viscosity [kg/ms]', default=0.01, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])
    rho_g = DecimalField('Gas Density [kg/m³]', default=200, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    mu_g = DecimalField('Gas Viscosity [kg/ms]', default=0.01, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])
    #mu_m = DecimalField('Mix Viscosity [cp]', default=0.01, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])

    # Flow input
    v_l_s = DecimalField('Superficial Liquid Velocity [m/s]', default=10, validators=[DataRequired(), NumberRange(min=0, max=200)])
    v_g_s = DecimalField('Superficial Gas Velocity [m/s]', default=5, validators=[DataRequired(), NumberRange(min=0, max=200)])
    #v_m = DecimalField('Mixture Velocity [m/s]', default=10, validators=[DataRequired(), NumberRange(min=0, max=200)])

    calculate = SubmitField('Calculate')

class Bend(BaseForm):
    # Pipe bend specific input
    R = DecimalField('Radius of curvature (R) [# IDs]', default=3, validators=[DataRequired(), NumberRange(min=0.5, max=50)])
    GF = DecimalField('Geometry Factor', default=1, validators=[DataRequired()])

class Reducer(BaseForm):
    # Reducers specific input
    D2 = DecimalField('Reduced diameter (D2) [m]', default=0.05, validators=[DataRequired()])
    GF = DecimalField('Geometry factor', validators=[DataRequired()])
    alpha = DecimalField('Particle impact angle (\u03B1) [deg]', default=60, validators=[DataRequired(), NumberRange(min=0, max=90)])

class BlindTee(BaseForm):
    # Blind tee specific input
    GF = DecimalField('Geometry factor', default=1, validators=[DataRequired()])

class Manifold(BaseForm):
    # Manifold specific input
    Dman = DecimalField('Manifold Diameter (Dman) [m]', default=0.2, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    GF = DecimalField('Geometry factor', default=1, validators=[DataRequired()])




