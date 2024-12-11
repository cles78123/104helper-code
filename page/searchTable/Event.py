import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from modules.FileUtil import FileUtil

class SearchTableEvent:
    @staticmethod
    def showSaveDialog(master, table):
        # 獲取已選中的項目
        selected_items = []
        for item in table.get_children():
            values = table.item(item)['values']
            if values[0] == "☑":
                selected_items.append({
                    'company': values[1],
                    'job': values[2],
                    'appear_at': values[3],
                    'company_url': values[4],
                    'job_url': values[5]
                })
        
        if not selected_items:
            messagebox.showwarning("警告", "請先選擇要保存的項目")
            return

        # 創建保存對話框
        save_dialog = tk.Toplevel(master)
        save_dialog.title("保存職缺")
        save_dialog.geometry("300x300")
        save_dialog.grab_set()

        # 讀取現有的保存組
        save_path = os.path.join(os.getcwd(), "userData", "guest", "group")
        os.makedirs(save_path, exist_ok=True)
        existing_groups = [f.replace('.json', '') for f in os.listdir(save_path) if f.endswith('.json')]

        # 創建選擇模式的變量
        save_mode = tk.StringVar(value="existing" if existing_groups else "new")

        # 創建現有項目框架
        existing_frame = tk.LabelFrame(save_dialog, text="選擇保存方式", padx=10, pady=5)
        existing_frame.pack(fill="x", padx=10, pady=5)

        # 添加 Radiobutton
        if existing_groups:
            existing_radio = tk.Radiobutton(
                existing_frame, 
                text="保存到現有項目", 
                variable=save_mode, 
                value="existing"
            )
            existing_radio.pack(anchor=tk.W)

        new_radio = tk.Radiobutton(
            existing_frame, 
            text="創建新項目", 
            variable=save_mode, 
            value="new"
        )
        new_radio.pack(anchor=tk.W)

        # 創建下拉選單框架
        group_frame = tk.LabelFrame(save_dialog, text="選擇保存位置", padx=10, pady=5)
        group_frame.pack(fill="x", padx=10, pady=5)

        # 添加下拉選單
        group_var = tk.StringVar()
        group_combobox = ttk.Combobox(group_frame, textvariable=group_var, values=existing_groups)
        group_combobox.pack(fill="x", pady=5)
        if not existing_groups:
            group_combobox.configure(state='disabled')

        # 創建新項目框架
        new_group_frame = tk.LabelFrame(save_dialog, text="新項目名稱", padx=10, pady=5)
        new_group_frame.pack(fill="x", padx=10, pady=5)

        new_group_entry = tk.Entry(new_group_frame)
        new_group_entry.pack(fill="x", pady=5)

        # 根據選擇模式啟用/禁用對應的輸入框
        def updateInputState(*args):
            if save_mode.get() == "existing":
                group_combobox.configure(state='normal')
                new_group_entry.configure(state='disabled')
            else:
                group_combobox.configure(state='disabled')
                new_group_entry.configure(state='normal')

        save_mode.trace('w', updateInputState)
        updateInputState()  # 初始化狀態

        def saveItems():
            if save_mode.get() == "existing":
                group_name = group_var.get()
                if not group_name:
                    messagebox.showwarning("警告", "請選擇保存位置")
                    return
            else:
                group_name = new_group_entry.get()
                if not group_name:
                    messagebox.showwarning("警告", "請輸入新項目名稱")
                    return

            # 獲取已選中的項目
            selected_items = []
            for item in table.get_children():
                values = table.item(item)['values']
                if values[0] == "☑":
                    selected_items.append({
                        'company': values[1],
                        'job': values[2],
                        'appear_at': values[3],
                        'company_url': values[4],
                        'job_url': values[5]
                    })

            # 讀取現有數據或創建新的
            existing_data = FileUtil.loadGroupData(group_name) or []

            # 檢查並只添加不重複的項目
            added_count = 0
            for item in selected_items:
                # 檢查是否已存在相同的公司和職缺組合
                is_duplicate = any(
                    existing['company'] == item['company'] and 
                    existing['job'] == item['job']
                    for existing in existing_data
                )
                
                # 如果不是重複項目，則添加
                if not is_duplicate:
                    existing_data.append(item)
                    added_count += 1

            # 保存數據
            if FileUtil.saveGroupData(group_name, existing_data):
                # 顯示保存結果
                if added_count > 0:
                    messagebox.showinfo("成功", f"成功保存 {added_count} 個新職缺！")
                else:
                    messagebox.showinfo("提示", "所選職缺都已經存在，沒有新增項目。")
                
                save_dialog.destroy()
            else:
                messagebox.showerror("錯誤", "保存失敗")

        # 添加保存按鈕
        save_button = tk.Button(save_dialog, text="保存", command=saveItems)
        save_button.pack(pady=10)
