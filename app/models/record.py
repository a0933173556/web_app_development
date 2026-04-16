from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

# 初始化 db 實例，這個通常會在 __init__.py 統籌或傳入 app 進行 init_app
db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # type 用於區分 'income' 或 'expense'
    type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def create(cls, type, title, amount, date):
        """新增一筆紀錄"""
        new_record = cls(
            type=type,
            title=title,
            amount=amount,
            date=date
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record

    @classmethod
    def get_all(cls):
        """讀取所有紀錄，依照日期與建立時間排序"""
        return cls.query.order_by(cls.date.desc(), cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, record_id):
        """依 ID 取得單一紀錄"""
        return cls.query.get(record_id)

    def update(self, **kwargs):
        """更新目前的紀錄"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """刪除這筆紀錄"""
        db.session.delete(self)
        db.session.commit()
