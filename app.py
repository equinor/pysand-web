'''Application entry point'''
from pysand_web import create_app
from waitress import serve

app = create_app()

# keep this as is
if __name__ == '__main__':
    app.run()
    #serve(app, host="0.0.0.0", port=5000)