import tkinter as tk
from tkinter import ttk
from .Event import SavedTableEvent
from modules.TableUtil import TableUtil
from modules.FileUtil import FileUtil

class SavedTable:
    def __init__(self, master):
        self.master = master
        
        # 創建主框架
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # 創建選擇框架和表格框架
        self.createSelectionFrame()
        self.createTableFrame()
        
    def createSelectionFrame(self):
        selection_frame = tk.Frame(self.main_frame, bd=2, relief="groove", padx=10, pady=10)
        selection_frame.pack(fill=tk.X, padx=10, pady=10)

        # 使用 FileUtil 獲取所有保存的組
        self.saved_files = FileUtil.getSavedGroups()

        # 創建下拉選單
        tk.Label(selection_frame, text="選擇保存組:").pack(side=tk.LEFT, padx=5)
        self.group_var = tk.StringVar()
        self.group_combobox = ttk.Combobox(
            selection_frame, 
            textvariable=self.group_var, 
            values=self.saved_files,
            width=30
        )
        self.group_combobox.pack(side=tk.LEFT, padx=5)

        # 添加刪除組按鈕
        delete_group_button = tk.Button(
            selection_frame, 
            text="刪除組", 
            command=lambda: SavedTableEvent.deleteGroup(
                self.group_var, 
                self.group_combobox, 
                self.table, 
                self.count_label
            )
        )
        delete_group_button.pack(side=tk.LEFT, padx=5)

        # 綁定選擇事件
        self.group_combobox.bind('<<ComboboxSelected>>', self.loadSavedData)

    def loadSavedData(self, event=None):
        selected_group = self.group_var.get()
        if not selected_group:
            return

        # 使用 FileUtil 載入組數據
        saved_data = FileUtil.loadGroupData(selected_group)
        
        # 使用 TableUtil 插入數據
        data_count = TableUtil.insertData(self.table, saved_data)
        
        # 更新計數
        self.count_label.config(text=f"總筆數: {data_count}")

    def createTableFrame(self):
        # 使用 TableUtil 創建表格框架
        self.second_frame, self.table, self.count_label = TableUtil.createTableFrame(
            self.main_frame,
            "刪除",
            lambda: SavedTableEvent.deleteSelected(
                self.table, 
                self.group_var, 
                self.count_label
            )
        )
        
        # 綁定點擊事件
        self.table.bind('<ButtonRelease-1>', lambda e: TableUtil.onClick(self.table, e)) 