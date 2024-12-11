from modules.FileUtil import FileUtil
from tkinter import messagebox

class SavedTableEvent:
    @staticmethod
    def deleteSelected(table, group_var, count_label):
        # 獲取選中的項目
        selected_items = []
        for item in table.get_children():
            values = table.item(item)['values']
            if values[0] == "☑":
                selected_items.append(item)
        
        if not selected_items:
            messagebox.showwarning("警告", "請先選擇要刪除的項目")
            return
        
        # 確認是否刪除
        if not messagebox.askyesno("確認", "確定要刪除選中的項目嗎？"):
            return
        
        # 獲取當前選擇的檔案
        selected_group = group_var.get()
        if not selected_group:
            return

        # 使用 FileUtil 來處理檔案操作
        saved_data = FileUtil.loadGroupData(selected_group)
        if not saved_data:
            return
            
        # 獲取要保留的數據
        new_data = []
        deleted_count = 0
        
        # 遍歷所有數據
        for item in saved_data:
            # 檢查是否在表格中被選中要刪除
            is_selected = False
            for table_item in selected_items:
                table_values = table.item(table_item)['values']
                if (item['company'] == table_values[1] and 
                    item['job'] == table_values[2] and 
                    str(item['appear_at']) == str(table_values[3])):
                    is_selected = True
                    deleted_count += 1
                    break
            
            # 如果沒有被選中刪除，則保留
            if not is_selected:
                new_data.append(item)
        
        # 保存更新後的數據
        if FileUtil.saveGroupData(selected_group, new_data):
            # 更新表格和計數
            for item in selected_items:
                table.delete(item)
            count_label.config(text=f"總筆數: {len(new_data)}")
            messagebox.showinfo("成功", f"已刪除 {deleted_count} 個項目")
        else:
            messagebox.showerror("錯誤", "保存失敗")

    @staticmethod
    def deleteGroup(group_var, group_combobox, table, count_label):
        selected_group = group_var.get()
        if not selected_group:
            messagebox.showwarning("警告", "請先選擇要刪除的組")
            return
        
        if not messagebox.askyesno("確認", f"確定要刪除「{selected_group}」組嗎？\n此操作無法復原！"):
            return
        
        if FileUtil.deleteGroup(selected_group):
            # 更新下拉選單選項
            group_combobox['values'] = FileUtil.getSavedGroups()
            
            # 清空當前選擇和表格
            group_var.set('')
            for item in table.get_children():
                table.delete(item)
            count_label.config(text="總筆數: 0")
            
            messagebox.showinfo("成功", f"已刪除「{selected_group}」組")
        else:
            messagebox.showerror("錯誤", "刪除失敗") 