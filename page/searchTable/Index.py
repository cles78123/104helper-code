import tkinter as tk
from tkinter import ttk
from crawlers.BaseCrawler import BaseCrawler
from crawlers.condition.BaseCondition import BaseCondition
from modules.FileUtil import FileUtil
from modules.TableUtil import TableUtil
from .Event import SearchTableEvent
import tkinter.messagebox as messagebox

class SearchTable:
    def __init__(self, master):
        self.master = master
        
        self.global_settings = {}
        
        # 加載公司和職缺設置
        self.company_rules = FileUtil.loadSettings('search_company_rules')
        self.job_rules = FileUtil.loadSettings('search_job_rules')
        
        # 合併所有設置
        self.global_settings = {
            **{f"company.{k}": v for k, v in self.company_rules.items()},
            **{f"job.{k}": v for k, v in self.job_rules.items()}
        }

        # 創建主框架並組合前兩個框架
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # 調用方法來生成搜索框架和表格框架
        self.createSearchFrame()
        self.createTableFrame()
        
    def createSearchFrame(self):
        search_frame = tk.Frame(self.main_frame, bd=2, relief="groove", padx=10, pady=10)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        # 左側的搜索組件
        left_frame = tk.Frame(search_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(left_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(left_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 右側的按鈕
        right_frame = tk.Frame(search_frame)
        right_frame.pack(side=tk.RIGHT)

        # 添加設定按鈕
        search_button = tk.Button(right_frame, text="設定", command=self.openSettingsWindow)
        search_button.pack(side=tk.LEFT, padx=5)

        # 添加搜索按鈕
        set_button = tk.Button(right_frame, text="搜尋", command=self.search)
        set_button.pack(side=tk.LEFT, padx=5)

        self.search_frame = search_frame

    def createTableFrame(self):
        # 使用 TableUtil 創建表格框架
        self.second_frame, self.table, self.count_label = TableUtil.createTableFrame(
            self.main_frame,
            "保存職缺",
            lambda: SearchTableEvent.showSaveDialog(self.master, self.table)
        )

    def openSettingsWindow(self):
        settings_window = tk.Toplevel()
        settings_window.title("設置")
        settings_window.geometry("300x300")
        settings_window.grab_set()
        
        # 創建一個Frame用於居中放置勾選框
        center_frame = tk.Frame(settings_window)
        center_frame.pack(expand=True)
        
        # 添加公司規則標題
        tk.Label(center_frame, text="公司規則").pack(anchor=tk.W, padx=10, pady=5)
        
        # 添加公司規則選項
        for key, item in self.company_rules.items():
            item["variable"] = tk.BooleanVar(value=item["status"])
            checkbutton = tk.Checkbutton(center_frame, text=item["name"], variable=item["variable"])
            checkbutton.pack(anchor=tk.W, padx=20, pady=2)
            checkbutton._name = f"company.{key}"
        
        # 添加職缺規則標題
        tk.Label(center_frame, text="職缺規則").pack(anchor=tk.W, padx=10, pady=5)
        
        # 添加職缺規則選項
        for key, item in self.job_rules.items():
            item["variable"] = tk.BooleanVar(value=item["status"])
            checkbutton = tk.Checkbutton(center_frame, text=item["name"], variable=item["variable"])
            checkbutton.pack(anchor=tk.W, padx=20, pady=2)
            checkbutton._name = f"job.{key}"

        # 修改保存設置按鈕的文字
        save_button = tk.Button(settings_window, text="保存設置", command=lambda: self.saveSettings(settings_window))
        save_button.pack(pady=10)
        
    def saveSettings(self, settings_window):
        for key in self.global_settings:
            self.global_settings[key]["status"] = self.global_settings[key]["variable"].get()

        FileUtil.saveSettingsToFile(self.global_settings)
        settings_window.destroy()
        
    def search(self):
        # 檢查 URL 格式
        url = self.search_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "請輸入搜索網址")
            return
            
        if not url.startswith('https://www.104.com.tw/jobs/search/'):
            messagebox.showwarning("警告", "請輸入正確的 104 搜索網址\n格式：https://www.104.com.tw/jobs/search/...")
            return

        # 創建進度條視窗
        progress_window = tk.Toplevel(self.master)
        progress_window.title("爬蟲進度")
        progress_window.geometry("300x150")
        
        # 設置進度條視窗置中
        progress_window.transient(self.master)
        progress_window.grab_set()
        
        # 添加提示文字
        status_label = tk.Label(progress_window, text="正在獲取資料...", pady=10)
        status_label.pack()
        
        # 創建進度條
        progress_bar = ttk.Progressbar(
            progress_window, 
            orient="horizontal", 
            length=200, 
            mode="determinate",
            maximum=100
        )
        progress_bar.pack(pady=20)
        
        def performSearch():
            try:
                def updateStatus(msg, progress=None):
                    status_label.config(text=msg)
                    if progress is not None:
                        progress_bar['value'] = progress
                    progress_window.update()
                    
                search_conditions = BaseCondition.generateConditionFromSettings(self.global_settings)
                search_results = BaseCrawler.getSearchItemTable(
                    self.search_entry.get(),  # 直接使用輸入框的內容作為完整 URL
                    search_conditions, 
                    status_callback=updateStatus
                )
                
                # 使用 TableUtil 插入數據
                data_count = TableUtil.insertData(self.table, search_results)
                
                # 更新總筆數
                self.count_label.config(text=f"總筆數: {data_count}")
                
                progress_window.destroy()
                
            except Exception as e:
                status_label.config(text=f"發生錯誤: {str(e)}")
                progress_bar.stop()
                tk.Button(
                    progress_window, 
                    text="確定", 
                    command=progress_window.destroy
                ).pack(pady=10)
        
        self.master.after(100, performSearch)