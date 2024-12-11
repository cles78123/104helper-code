import tkinter as tk
from page.searchTable.Index import SearchTable
from page.savedTable.Index import SavedTable

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("104求職助手")
        self.root.geometry("800x600")

        # 創建頂部按鈕欄
        self.createTopFrame()
        
        # 創建用於顯示頁面的框架
        self.createContentFrame()

        # 默認不顯示任何頁面
        self.current_page = None

    def createTopFrame(self):
        self.top_frame = tk.Frame(self.root, bd=2, relief="groove")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # 創建搜尋和已保存按鈕
        self.search_button = tk.Button(
            self.top_frame, 
            text="搜尋", 
            width=10, 
            height=2, 
            relief="groove", 
            command=self.showSearchPage
        )
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.saved_button = tk.Button(
            self.top_frame, 
            text="已保存職缺", 
            width=10, 
            height=2, 
            relief="groove", 
            command=self.showSavedPage
        )
        self.saved_button.pack(side=tk.LEFT, padx=5, pady=5)

    def createContentFrame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clearCurrentPage(self):
        if self.current_page is not None:
            # 清理當前頁面的所有小部件
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.current_page = None

    def showSearchPage(self):
        self.clearCurrentPage()
        self.current_page = SearchTable(self.content_frame)

    def showSavedPage(self):
        self.clearCurrentPage()
        self.current_page = SavedTable(self.content_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()