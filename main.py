from flask import Flask
from init import db, ma, bc, jwt
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import StatementError
from controllers.vinyls_controller import vinyls_bp
from controllers.auth_controller import auth_bp
from controllers.comments_controller import comments_bp
from controllers.likes_controller import likes_bp
from controllers.artists_controller import artists_bp
from controllers.cli_controller import db_commands
import os

# Function to define our app
def create_app():
    app = Flask(__name__)
    # Error handlers
    @app.errorhandler(KeyError)
    def key_err(err):
        return {"error": f"Missing field: {str(err)}"}, 400
                
    @app.errorhandler(ValidationError)
    def validation_err(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(TypeError)
    def type_err(err):
        return {"error": str(err)}, 400

    @app.errorhandler(ValueError)
    def value_err(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(StatementError)
    def statement_err(err):
        return {"error": "Statement Error, value used is not of the correct type or the related entity doesn't exist"}, 400
   
    @app.errorhandler(AttributeError)
    def attribute_err(err):
        return {"error": str(err)}, 401

    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
            
    @app.errorhandler(401)
    def not_artistised(err):
        return {"error": str(err)}, 401
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404

    @app.errorhandler(405)
    def method_not_allowed(err):
        return {"error": str(err)}, 405
        
    @app.errorhandler(409)
    def conflict_err(err):
        return {"error": str(err)}, 409
    
    # Stopping flask from trying to sort the returned JSON resources 
    app.config['JSON_SORT_KEYS'] = False
    # Getting our database link from our environment variables 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # Getting JWT secret key from environment variables 
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    
    # Instantiating models
    db.init_app(app)
    ma.init_app(app)
    bc.init_app(app)
    jwt.init_app(app)
    
    # Connecting blueprints to app
    app.register_blueprint(db_commands)
    app.register_blueprint(vinyls_bp)
    app.register_blueprint(artists_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(auth_bp)
    
    # Must return the app so flask can recognise it 
    return app
 