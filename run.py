from flask import Flask
from app.routes import bp as main_bp

# Point Flask to app/templates since templates live inside the package
app = Flask(__name__, template_folder="app/templates")
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
