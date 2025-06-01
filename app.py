from flask import Flask
from routes import main_routes
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.register_blueprint(main_routes)
app.config['HTML_MINIFY'] = True
htmlmin = HTMLMIN(app)

if __name__ == '__main__':
    app.run(debug=True)