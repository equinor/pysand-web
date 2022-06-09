from lib2to3.pytree import Base
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from pysand_web.transport.transport_data import transport_models_tuples


###################
# Transport Forms #
###################
class TransportBaseForm(FlaskForm):
    transport_model = SelectField('Select transport model', default='hydro', choices=transport_models_tuples, validators=[DataRequired()])
    rho_p = DecimalField('Particle Density [kg/m³]', id='particle', default=2650, places=0, validators=[DataRequired(), NumberRange(min=0, max=10000)])
    d_p = DecimalField('Particle diameter [mm]', id='particle', default=0.1, validators=[DataRequired()])
    calculate = SubmitField('Calculate')

class TransportHydroForm(TransportBaseForm):
    D = DecimalField('Inner diameter (D) [m]', id='geom', places=3, default=0.1, validators=[DataRequired(), NumberRange(min=0.01, max=1)])
    e = DecimalField('Pipe Roughness (e) [m]', id='geom', places=5, default=5e-5, validators=[DataRequired()])
    rho_l = DecimalField('Liquid Density [kg/m³]', id='pvt', default=1000, places=0, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    mu_l = DecimalField('Liquid Viscosity [cP]', id='pvt', default=1, places=3, validators=[DataRequired(), NumberRange(min=0.001, max=10)])

class TransportStokesForm(TransportBaseForm):
    rho_m = DecimalField('Liquid Density [kg/m³]', id='pvt', default=1000, places=0, validators=[DataRequired(), NumberRange(min=1, max=1500)])
    mu_m = DecimalField('Liquid Viscosity [cP]', id='pvt', default=1, places=3, validators=[DataRequired(), NumberRange(min=0.001, max=10)])
    angle = DecimalField('Inclination from vertical angle (\u03B1) [deg]', id='specific', places=0, default=60, validators=[DataRequired(), NumberRange(min=0, max=80)])