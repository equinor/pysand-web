'''Initialise Flask app'''
from flask import Flask
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap4

def create_app():
    """Create Flask application."""
    app = Flask(
        __name__, 
        instance_relative_config=False,
        template_folder='templates',
        static_folder='static'
        )

    csrf = CSRFProtect(app)  # Global csrf protection (https://flask-wtf.readthedocs.io/en/latest/api/#module-flask_wtf.csrf)
    app.config.from_object('config.DevConfig')
    Bootstrap4(app)

    with app.app_context():
        # Import parts of our application
        from pysand_web.main import main_routes
        from pysand_web.erosion import erosion_routes
        from pysand_web.transport import transport_routes

        # Register Blueprints
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(erosion_routes.erosion_bp)
        app.register_blueprint(transport_routes.transport_bp)

        return app