from flask import Flask
from app.routes import bp as main_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecret"  # change this in production

# Register Blueprints
app.register_blueprint(main_bp)

# Inject current year dynamically into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

if __name__ == "__main__":
    app.run(debug=True)
