from flask import Blueprint, render_template, request, redirect, url_for, abort

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示總餘額與所有收支紀錄
    """
    pass

@main_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    新增頁面：顯示新增紀錄的 HTML 表單
    """
    pass

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    建立紀錄：接收表單資料，寫入資料記錄後重導向至首頁
    """
    pass

@main_bp.route('/records/<int:id>/edit', methods=['GET'])
def edit_record(id):
    """
    編輯頁面：依據 ID 找出特定紀錄，將舊資料預填在表單上提供使用者修改
    """
    pass

@main_bp.route('/records/<int:id>/update', methods=['POST'])
def update_record(id):
    """
    更新紀錄：接收編輯表單提交的資料，更新指定紀錄，完成後導向至首頁
    """
    pass

@main_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    刪除紀錄：依據 ID 定位該筆紀錄並將其移除，完成後重導向至首頁
    """
    pass
