import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class TableUtil:
    @staticmethod
    def createTable(frame, scrollbar_y, scrollbar_x):
        """創建標準表格"""
        columns = ("checkbox", "company", "job", "appear_at", "company_url", "job_url")
        table = ttk.Treeview(
            frame, 
            columns=columns, 
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # 設置列標題
        table.heading("checkbox", text="☐", command=lambda: TableUtil.toggleAll(table))
        table.heading("company", text="公司", command=lambda: TableUtil.sortByColumn(table, "company", False))
        table.heading("job", text="職缺", command=lambda: TableUtil.sortByColumn(table, "job", False))
        table.heading("appear_at", text="刊登日期", command=lambda: TableUtil.sortByColumn(table, "appear_at", False))
        
        # 設置列寬
        table.column("checkbox", width=30, anchor="center")
        table.column("company", width=200)
        table.column("job", width=300)
        table.column("appear_at", width=100)
        table.column("company_url", width=0, stretch=False)
        table.column("job_url", width=0, stretch=False)
        
        # 配置滾動條
        scrollbar_y.config(command=table.yview)
        scrollbar_x.config(command=table.xview)
        
        # 綁定點擊事件
        table.bind('<ButtonRelease-1>', lambda e: TableUtil.onClick(table, e))
        
        return table

    @staticmethod
    def insertData(table, data):
        """插入數據到表格"""
        # 清空現有表格
        for item in table.get_children():
            table.delete(item)
        
        # 插入新數據
        for item in data:
            table.insert("", "end", values=(
                "☐",
                item['company'],
                item['job'],
                item['appear_at'],
                item['company_url'],
                item['job_url']
            ))
        
        return len(data)

    @staticmethod
    def onClick(table, event):
        """處理表格點擊事件"""
        # 檢查點擊的區域
        region = table.identify("region", event.x, event.y)
        
        # 如果點擊的是標題區域，則不處理
        if region == "heading":
            return
            
        # 獲取點擊的行
        item_id = table.identify_row(event.y)
        if not item_id:
            return
        
        column = table.identify_column(event.x)
        values = table.item(item_id)['values']
        
        if column == '#1':  # checkbox
            current_state = values[0]
            new_state = "☑" if current_state == "☐" else "☐"
            values = list(values)
            values[0] = new_state
            table.item(item_id, values=values)
        elif column == '#2':  # 公司
            company_url = values[4]
            if company_url:
                webbrowser.open(company_url)
        elif column == '#3':  # 職缺
            job_url = values[5]
            if job_url:
                webbrowser.open(job_url)

    @staticmethod
    def toggleAll(table):
        """切換所有 checkbox 狀態"""
        items = table.get_children()
        
        all_checked = True
        for item in items:
            values = table.item(item)['values']
            if values[0] == "☐":
                all_checked = False
                break
        
        new_state = "☐" if all_checked else "☑"
        table.heading("checkbox", text=new_state)
        
        for item in items:
            values = list(table.item(item)['values'])
            values[0] = new_state
            table.item(item, values=values)

    @staticmethod
    def sortByColumn(table, column, reverse):
        """依照指定欄位排序"""
        items = [(table.set(k, column), k) for k in table.get_children("")]
        
        if column == "appear_at":
            items = [(datetime.strptime(date, '%Y%m%d'), k) for date, k in items]
        
        items.sort(reverse=reverse)
        
        for index, (_, k) in enumerate(items):
            table.move(k, "", index)
        
        column_text = {
            "company": "公司",
            "job": "職缺",
            "appear_at": "刊登日期"
        }.get(column)
        
        table.heading(
            column, 
            command=lambda: TableUtil.sortByColumn(table, column, not reverse),
            text=f"{column_text} ▼" if reverse else f"{column_text} ▲"
        ) 

    @staticmethod
    def createTableWithScrollbar(frame):
        """創建帶有滾動條的表格"""
        # 創建滾動條
        scrollbar_y = ttk.Scrollbar(frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal")
        
        # 創建表格
        table = TableUtil.createTable(frame, scrollbar_y, scrollbar_x)
        
        # 使用 grid 布局
        table.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")
        
        return table 

    @staticmethod
    def createTableFrame(parent, button_text, button_command):
        """創建帶有標題和按鈕的表格框架"""
        # 創建主框架
        frame = tk.Frame(parent, bd=2, relief="groove", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # 添加標題框架
        title_frame = tk.Frame(frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)

        # 創建右側框架
        right_frame = tk.Frame(title_frame)
        right_frame.pack(side=tk.RIGHT)

        # 添加計數標籤
        count_label = tk.Label(right_frame, text="總筆數: 0")
        count_label.pack(side=tk.LEFT, padx=5, pady=5)

        # 添加按鈕
        button = tk.Button(right_frame, text=button_text, command=button_command)
        button.pack(side=tk.LEFT, padx=5, pady=5)

        # 創建表格
        table = TableUtil.createTableWithScrollbar(frame)
        
        # 配置 grid 權重
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return frame, table, count_label 