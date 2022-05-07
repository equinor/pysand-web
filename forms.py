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
    material = SelectField('Select material', default='duplex', choices=materials_tuples, validators=[DataRequired()])
    internal_diameter = DecimalField('Inner diameter (D) [m]', places=3, default=0.1, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    
    # Erosive agents
    erosive_agent = SelectField('Select erosive agent', default='quartz', choices=[('quartz', 'Quartz sand')], validators=[DataRequired()])
    q_s = DecimalField('Sand production rate [g/s]', default=0.1)

    # PVT input
    rho_l = DecimalField('Liquid Density [kg/m³]', default=1000, places=0, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    rho_g = DecimalField('Gas Density [kg/m³]', default=200, places=0, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    
    # Flow input
    v_l_s = DecimalField('Superficial Liquid Velocity [m/s]', places=1, default=10, validators=[DataRequired(), NumberRange(min=0, max=200)])
    v_g_s = DecimalField('Superficial Gas Velocity [m/s]', places=1, default=5, validators=[DataRequired(), NumberRange(min=0, max=200)])
    #v_m = DecimalField('Mixture Velocity [m/s]', default=10, validators=[DataRequired(), NumberRange(min=0, max=200)])

    calculate = SubmitField('Calculate')

class BaseFormVisc(BaseForm):
    mu_l = DecimalField('Liquid Viscosity [kg/ms]', default=1e-3, places=6, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])
    mu_g = DecimalField('Gas Viscosity [kg/ms]', default=1e-5, places=6, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])
    #mu_m = DecimalField('Mix Viscosity [cp]', default=0.01, validators=[DataRequired(), NumberRange(min=1e-6, max=1e-2)])

class Bend(BaseFormVisc):
    # Pipe bend specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    R = DecimalField('Radius of curvature (R) [# IDs]', default=3, places=1, validators=[DataRequired(), NumberRange(min=0.5, max=50)])
    GF = DecimalField('Geometry Factor', default=1, validators=[DataRequired()])

class Tee(BaseFormVisc):
    # Blind tee specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    GF = DecimalField('Geometry factor', places=1, default=1, validators=[DataRequired()])

class WeldedJoint(BaseForm):
    # Blind tee specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    h = DecimalField('Height of weld [m]', places=3, default=0.1, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    alpha = DecimalField('Particle impact angle (\u03B1) [deg]', places=0, default=60, validators=[DataRequired(), NumberRange(min=0, max=90)])
    Location = SelectField('Location of weld', default='downstream', choices=[('downstream', 'Downstream'), ('upstream', 'Upstream')], validators=[DataRequired()])

class Manifold(BaseFormVisc):
    # Manifold specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    Dman = DecimalField('Manifold Diameter (Dman) [m]', places=3, default=0.2, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    GF = DecimalField('Geometry factor', places=1, default=1, validators=[DataRequired()])

class Reducer(BaseForm):
    # Reducers specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    D2 = DecimalField('Reduced diameter (D2) [m]', places=3, default=0.05, validators=[DataRequired()])
    GF = DecimalField('Geometry factor', places=1, default=1, validators=[DataRequired()])
    alpha = DecimalField('Particle impact angle (\u03B1) [deg]', places=0, default=60, validators=[DataRequired(), NumberRange(min=0, max=90)])

class Probes(BaseForm):
    # Erosion probe specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    alpha = DecimalField('Particle impact angle (\u03B1) [deg]', places=0, default=60, validators=[DataRequired(), NumberRange(min=0, max=90)])

class Flexible(BaseFormVisc):
    # Erosion probe specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    mbr = DecimalField('Minimum bending radius in operation [# IDs]',default=5, places=1, validators=[DataRequired(), NumberRange(min=0.5, max=50)])

class ChokeGallery(BaseFormVisc):
    # Erosion probe specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    alpha = DecimalField('Particle impact angle (\u03B1) [deg]', places=0, default=60, validators=[DataRequired(), NumberRange(min=0, max=90)])
    Rc = DecimalField('Radius of choke gallery [m]', default=0.1, validators=[DataRequired(), NumberRange(min=0)])
    gap = DecimalField('Gap cage and choke body [m]', default=0.01, validators=[DataRequired(), NumberRange(min=0)])
    H = DecimalField('Height of choke gallery [m]', default=0.1, validators=[DataRequired(), NumberRange(min=0)])

class NozzlevalveWall(BaseForm):
    # Erosion probe specific input
    particle_diameter = DecimalField('Particle diameter [mm]', default=0.1, validators=[DataRequired()])
    At = DecimalField('Minimum flow area of the valve [m]', default=0.1, validators=[DataRequired(), NumberRange(min=0)])