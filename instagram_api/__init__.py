from app import app, csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.images.views import images_api_blueprint
from instagram_api.blueprints.sessions.views import sessions_api_blueprint


app.register_blueprint(csrf.exempt(users_api_blueprint), url_prefix='/api/v1/users')
app.register_blueprint(csrf.exempt(images_api_blueprint), url_prefix='/api/v1/images')
app.register_blueprint(csrf.exempt(sessions_api_blueprint), url_prefix='/api/v1/')

