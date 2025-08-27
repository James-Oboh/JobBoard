# app.py
from flask import Flask
from flask_login import LoginManager
from models import db, User 
from routes.auth import auth_bp
from routes.jobs import jobs_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(jobs_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)