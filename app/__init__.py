import os
from flask import Flask
from .models.record import db
from .routes.main_routes import main_bp

def create_app():
    """
    Flask 應用程式工廠函式 (Application Factory)
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'default_dev_key_if_not_set'),
        SQLALCHEMY_DATABASE_URI='sqlite:///database.db', # 預設在 instance/database.db
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化套件
    db.init_app(app)

    # 註冊 Blueprints (路由)
    app.register_blueprint(main_bp)

    # 初始化資料庫表格 (根據 Model 定義)
    with app.app_context():
        db.create_all()

    return app
