import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_login import LoginManager
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



def create_app(config_class=None):
    app = Flask(__name__, 
                static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'), 
                template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend'))
    
    # Configure app first
    if config_class is None:
        # try:
        #     from config import Config
        # except ImportError:
        #     from config import Config
        # from config import config
        from .config import config
        config_name = os.getenv('FLASK_ENV') or 'default'
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(config_class)
    
    # Initialize extensions
    # backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    # sys.path.insert(0, backend_dir)
    # from models import db
    # from auth import login_manager
    # from .models import db
    # from .auth import login_manager
    try:
        from models import db
        from auth import login_manager
    except ImportError:
        from .models import db
        from .auth import login_manager

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    try:
        from routes.products import products_bp
        from routes.employees import employees_bp
        from routes.deliveries import deliveries_bp
        from routes.auth_routes import auth_bp
    except ImportError:
        from .routes.products import products_bp
        from .routes.employees import employees_bp
        from .routes.deliveries import deliveries_bp
        from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(employees_bp, url_prefix='/api')
    app.register_blueprint(deliveries_bp, url_prefix='/api')
    
    CORS(app, 
         supports_credentials=True,
         origins=["http://localhost:5000", "http://127.0.0.1:5000", "http://localhost:3000"])
    

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Serve frontend files
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'main.html')

    @app.route('/<path:path>')
    def serve_static(path):
        # Handle all frontend routes
        if '.' in path:  # If it has a file extension
            return send_from_directory(app.static_folder, path)
        else:  # For SPA routes, serve main.html
            return send_from_directory(app.static_folder, 'main.html')
        
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Stock Manager API is running'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    from .models import db

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        from models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@stockmaster.com')
            admin.set_password('1234')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created!")
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)