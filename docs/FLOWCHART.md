# 流程圖文件 (FLOWCHART) - 個人記帳簿系統

本文件根據 PRD 與系統架構設計，視覺化使用者的操作路徑與系統內部的資料流。

## 1. 使用者流程圖 (User Flow)

以下說明使用者進入系統後的各種操作路徑，涵蓋查看首頁、新增收支紀錄、編輯與刪除的基本流程。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home[首頁 - 收支總覽與明細列表]
    
    Home --> Action{想執行什麼操作？}
    
    Action -->|新增收支| Add[點擊新增按鈕]
    Add --> Form[填寫類型、項目、金額、日期等資訊]
    Form --> Submit{送出表單}
    Submit -->|成功| Home
    Submit -->|驗證失敗| Form
    
    Action -->|修改明細| Edit[點擊特定紀錄的「編輯」按鈕]
    Edit --> EditForm[修改成新的資料內容]
    EditForm --> EditSubmit{儲存修改}
    EditSubmit -->|成功| Home
    
    Action -->|刪除明細| Delete[點擊特定紀錄的「刪除」按鈕]
    Delete --> ConfirmDelete{確認是否刪除？}
    ConfirmDelete -->|是| Home
    ConfirmDelete -->|否| Home
```

## 2. 系統序列圖 (Sequence Diagram)

此處針對「**新增一筆收支紀錄**」這個最具代表性的功能，展開從前端使用者互動到後端資料庫互動的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as SQLAlchemy (Model)
    participant DB as SQLite

    User->>Browser: 在表單輸入支出/收入金額與項目，並點擊送出
    Browser->>Flask: POST /record/add (包含 amount, type, title 等資訊)
    Flask->>Flask: 檢查資料正確性 (如金額不得為空或負數)
    Flask->>Model: 將輸入資料轉換為 Record 物件
    Model->>DB: INSERT INTO records ...
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳存檔結果
    Flask-->>Browser: HTTP 302 重導向到首頁
    
    Note over Browser, DB: 重新導向後載入最新資料
    
    Browser->>Flask: GET / (請求首頁)
    Flask->>Model: 查詢所有 records 並動態計算最新總餘額
    Model->>DB: SELECT * FROM records
    DB-->>Model: 回傳資料集
    Model-->>Flask: 整理資料傳遞給 Jinja2 模板渲染
    Flask-->>Browser: 回傳整理後的首頁 HTML (顯示最新紀錄與餘額)
```

## 3. 功能清單對照表

我們將剛才梳理的使用者行為轉換成對應的路由與請求方式，為下一階段的 API 實作做準備：

| 功能名稱 | 說明 | HTTP 請求方法 | 預定 URL 路徑 |
| :--- | :--- | :--- | :--- |
| **首頁與明細** | 顯示總餘額計算結果，並條列所有收支紀錄 | GET | `/` |
| **新增紀錄頁面** | 展示用來新增一筆收入或支出的表單 | GET | `/record/add` |
| **提交新增紀錄** | 接收表單傳入的參數並真正寫入資料庫 | POST | `/record/add` |
| **編輯紀錄頁面** | 針對特定的一筆紀錄展示修改用的表單 | GET | `/record/edit/<int:id>` |
| **提交修改紀錄** | 接收編輯後的資料並覆寫該筆紀錄 | POST | `/record/edit/<int:id>` |
| **刪除特定紀錄** | 移除指定的收支紀錄 (僅接受 POST 防止意外 GET 請求) | POST | `/record/delete/<int:id>` |
