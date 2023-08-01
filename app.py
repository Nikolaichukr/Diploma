from flask import Flask
from views import *

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(task1, url_prefix='/task1')

if __name__ == "__main__":
    app.run(debug=True)
