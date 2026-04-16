# 路由與頁面設計文件 (ROUTES) - 個人記帳簿系統

本文件基於 PRD、系統架構與資料庫設計，規劃系統的 URL 路由結構、HTTP 方法及對應的處理邏輯與 Jinja2 模板。我們採用 RESTful 風格搭配 HTTP 表單標準來設計。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (記帳列表) | GET | `/` | `index.html` | 顯示所有收支紀錄以及計算後的總餘額 |
| 新增紀錄頁面 | GET | `/records/new` | `new.html` | 顯示新增收支紀錄的表單 |
| 建立紀錄 | POST | `/records` | — | 接收新增表單，存入 DB，完成後重導向首頁 |
| 編輯紀錄頁面 | GET | `/records/<id>/edit` | `edit.html` | 顯示修改特定收支紀錄的表單 |
| 更新紀錄 | POST | `/records/<id>/update` | — | 接收編輯表單，更新該筆紀錄，完成後重導向首頁 |
| 刪除紀錄 | POST | `/records/<id>/delete` | — | 刪除單筆紀錄，完成後重導向至首頁 |

## 2. 每個路由的詳細說明

### 2.1. GET `/` (首頁/列表)
- **輸入**：無
- **處理邏輯**：呼叫 `Record.get_all()` 取得所有近期歷史紀錄。計算 `total_balance` (所有 `type='income'` 總額減去所有 `type='expense'` 總額)。
- **輸出**：渲染 `index.html`，傳遞 `records` 與 `total_balance`。

### 2.2. GET `/records/new`
- **輸入**：無
- **處理邏輯**：準備渲染新增頁面。
- **輸出**：渲染 `new.html`。

### 2.3. POST `/records`
- **輸入 (表單)**：`type` ('income'或'expense'), `title`, `amount` (大於0的數字), `date`
- **處理邏輯**：驗證欄位合法性，接著透過 `Record.create(...)` 方法在資料庫建立新紀錄。
- **錯誤處理**：如果必填未填或格式有誤，重新渲染 `new.html` 附帶錯誤訊息。
- **輸出**：成功後執行 `redirect(url_for('main.index'))` 回到首頁。

### 2.4. GET `/records/<id>/edit`
- **輸入 (URL 參數)**：`id` (整數)
- **處理邏輯**：透過 `Record.get_by_id(id)` 拿取紀錄供預填。
- **錯誤處理**：如果 `id` 找不到，回傳 `abort(404)` 錯誤頁面。
- **輸出**：渲染 `edit.html`，並將紀錄資料注入模板中。

### 2.5. POST `/records/<id>/update`
- **輸入 (URL 參數 + 表單)**：`id` 加上表單欄位 `type`, `title`, `amount`, `date`
- **處理邏輯**：呼叫 `Record.get_by_id(id)`，接著更新屬性並使用 `record.update()` 儲存變更。
- **錯誤處理**：資料驗證失敗則重新導回編輯表單顯示錯誤。
- **輸出**：成功後執行 `redirect(url_for('main.index'))` 回到首頁。

### 2.6. POST `/records/<id>/delete`
- **輸入 (URL 參數)**：`id` (整數)
- **處理邏輯**：尋找 `Record.get_by_id(id)` 後執行 `record.delete()` 移除之。
- **錯誤處理**：若該 id 不存在直接 pass 或 404，然後回首頁。
- **輸出**：完成後執行 `redirect(url_for('main.index'))`。

## 3. Jinja2 模板清單

所有的模板檔案都會存放在 `app/templates/` 目錄中：

- `base.html`：負責整個網站的共通版面 (Header、Footer、HTML5 的 head 與匯入 CSS/JS)，包含 `{% block content %}`。
- `index.html`：繼承自 `base.html`。展示網頁頂部大字體的總餘額，下方條列所有的收支明細，每條明細皆附帶「編輯」與「刪除」的選項。
- `new.html`：繼承自 `base.html`。提供輸入一筆新紀錄的乾淨表單。
- `edit.html`：繼承自 `base.html`。顯示與新增相似的表單，但具備現有資料的自動帶入。

## 4. 路由骨架程式碼

已建立於 `app/routes/main_routes.py`。
