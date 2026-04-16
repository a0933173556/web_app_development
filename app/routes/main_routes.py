from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from datetime import datetime
from ..models.record import Record

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示總餘額與所有收支紀錄
    """
    records = Record.get_all()
    # 依 type 將為 'income' 者相加，'expense' 者扣除
    total_balance = sum(r.amount if r.type == 'income' else -r.amount for r in records)
    return render_template('index.html', records=records, total_balance=total_balance)

@main_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    新增頁面：顯示新增紀錄的 HTML 表單
    """
    return render_template('new.html')

@main_bp.route('/records', methods=['POST'])
def create_record():
    """
    建立紀錄：接收表單資料，寫入資料記錄後重導向至首頁
    """
    type_ = request.form.get('type')
    title = request.form.get('title')
    amount = request.form.get('amount')
    date_str = request.form.get('date')

    # 基本的輸入驗證
    if not all([type_, title, amount, date_str]):
        flash("所有的欄位都是必填的！", "error")
        return redirect(url_for('main.new_record'))

    try:
        amount_int = int(amount)
        if amount_int < 0:
            raise ValueError
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("金額格式有誤或日期不正確！", "error")
        return redirect(url_for('main.new_record'))

    Record.create(type=type_, title=title, amount=amount_int, date=date_obj)
    flash("成功新增一筆紀錄！", "success")
    return redirect(url_for('main.index'))

@main_bp.route('/records/<int:id>/edit', methods=['GET'])
def edit_record(id):
    """
    編輯頁面：依據 ID 找出特定紀錄，將舊資料預填在表單上提供使用者修改
    """
    record = Record.get_by_id(id)
    if not record:
        abort(404)
    return render_template('edit.html', record=record)

@main_bp.route('/records/<int:id>/update', methods=['POST'])
def update_record(id):
    """
    更新紀錄：接收編輯表單提交的資料，更新指定紀錄，完成後導向至首頁
    """
    record = Record.get_by_id(id)
    if not record:
        abort(404)

    type_ = request.form.get('type')
    title = request.form.get('title')
    amount = request.form.get('amount')
    date_str = request.form.get('date')

    if not all([type_, title, amount, date_str]):
        flash("所有的欄位都是必填的！", "error")
        return redirect(url_for('main.edit_record', id=id))

    try:
        amount_int = int(amount)
        if amount_int < 0:
            raise ValueError
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("金額格式有誤或日期不正確！", "error")
        return redirect(url_for('main.edit_record', id=id))

    record.update(type=type_, title=title, amount=amount_int, date=date_obj)
    flash("紀錄更新成功！", "success")
    return redirect(url_for('main.index'))

@main_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    刪除紀錄：依據 ID 定位該筆紀錄並將其移除，完成後重導向至首頁
    """
    record = Record.get_by_id(id)
    if record:
        record.delete()
        flash("成功刪除該筆紀錄！", "success")
    return redirect(url_for('main.index'))
