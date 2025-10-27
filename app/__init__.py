from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    jwt = JWTManager(app)
    api = Api(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.artist_routes import artist_bp
    from app.routes.collector_routes import collector_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(artist_bp, url_prefix='/api/artist')
    app.register_blueprint(collector_bp, url_prefix='/api/collector')

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {'message': 'Missing authorization header'}, 401

    return app