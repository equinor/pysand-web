'''Initialise Flask app'''
from flask import Flask
from flask_bootstrap import Bootstrap4

def create_app():
    """Create Flask application."""
    app = Flask(
        __name__, 
        instance_relative_config=False,
        template_folder='templates',
        static_folder='static'
        )

    app.config.from_object('config.ProdConfig')
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