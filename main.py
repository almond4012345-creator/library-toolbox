import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading

from get_covers import run_get_covers
from name import run_author_code
from compare import run_compare
from catchbook import run_catchbook

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

def handle_normal_task(task_func, task_name):
    file_path = filedialog.askopenfilename(title=f"選擇檔案 - {task_name}", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    def run_in_background():
        success, result = task_func(file_path)
        
        def update_gui():
            if success:
                messagebox.showinfo("成功", f"【{task_name}】執行成功！\n檔案已存至：\n{result}")
            else:
                messagebox.showerror("錯誤", f"【{task_name}】執行失敗：\n{result}")
        
        root.after(0, update_gui)

    threading.Thread(target=run_in_background, daemon=True).start()

def open_compare_window():
    comp_win = ctk.CTkToplevel(root)
    comp_win.title("查重設定")
    comp_win.geometry("400x420")
    comp_win.attributes('-topmost', True)
    comp_win.configure(fg_color="#E8F5E9")
    
    file_paths = {"collection": None, "isbn": None, "title": None}
    
    def choose_file(key, label_obj):
        path = filedialog.askopenfilename(title="選擇 Excel", filetypes=[("Excel files", "*.xlsx")])
        if path:
            file_paths[key] = path
            label_obj.configure(text="✅ 已選擇", text_color="#34C759")

    ctk.CTkLabel(comp_win, text="1. 上傳已有館藏 (必填)", font=("Helvetica", 14, "bold")).pack(pady=(20, 5))
    var_col = ctk.CTkLabel(comp_win, text="❌ 未選擇", text_color="#FF3B30", font=("Helvetica", 12))
    ctk.CTkButton(comp_win, text="選擇館藏檔案", fg_color="#FFFFFF", text_color="black", hover_color="#E5E5EA", command=lambda: choose_file("collection", var_col)).pack()
    var_col.pack(pady=(0, 10))

    ctk.CTkLabel(comp_win, text="2. 上傳待查 ISBN (選填)", font=("Helvetica", 14, "bold")).pack(pady=(5, 5))
    var_isbn = ctk.CTkLabel(comp_win, text="❌ 未選擇", text_color="#FF3B30", font=("Helvetica", 12))
    ctk.CTkButton(comp_win, text="選擇 ISBN 檔案", fg_color="#FFFFFF", text_color="black", hover_color="#E5E5EA", command=lambda: choose_file("isbn", var_isbn)).pack()
    var_isbn.pack(pady=(0, 10))

    ctk.CTkLabel(comp_win, text="3. 上傳待查書名 (選填)", font=("Helvetica", 14, "bold")).pack(pady=(5, 5))
    var_title = ctk.CTkLabel(comp_win, text="❌ 未選擇", text_color="#FF3B30", font=("Helvetica", 12))
    ctk.CTkButton(comp_win, text="選擇書名檔案", fg_color="#FFFFFF", text_color="black", hover_color="#E5E5EA", command=lambda: choose_file("title", var_title)).pack()
    var_title.pack(pady=(0, 10))

    def start_compare():
        if not file_paths["collection"]:
            messagebox.showwarning("警告", "必須上傳已有館藏！")
            return
        
        def run_in_background():
            success, result = run_compare(file_paths["collection"], file_paths["isbn"], file_paths["title"])
            
            def update_gui():
                if success:
                    messagebox.showinfo("查重完成", result)
                    comp_win.destroy()
                else:
                    messagebox.showerror("錯誤", f"查重失敗：\n{result}")
            
            root.after(0, update_gui)

        threading.Thread(target=run_in_background, daemon=True).start()

    ctk.CTkButton(comp_win, text="開始", fg_color="#FF9500", text_color="white", hover_color="#CC7700", font=("Helvetica", 15, "bold"), width=200, height=40, corner_radius=8, command=start_compare).pack(pady=20)

root = ctk.CTk()
root.title("圖書館工具箱")
root.geometry("450x450")
root.configure(fg_color="#E8F5E9")

try:
    root.iconbitmap("Unknown.ico")
except:
    pass

title_label = ctk.CTkLabel(root, text="圖書館自動化工具", font=("Helvetica", 24, "bold"), text_color="#1C1C1E")
title_label.pack(pady=(40, 30))

btn_style = {
    "width": 280,
    "height": 45,
    "corner_radius": 10,
    "font": ("Helvetica", 15, "bold"),
    "fg_color": "#FFFFFF",
    "text_color": "#1C1C1E",
    "hover_color": "#E5E5EA"
}

ctk.CTkButton(root, text="查重", command=open_compare_window, **btn_style).pack(pady=12)
ctk.CTkButton(root, text="自動換著者號", command=lambda: handle_normal_task(run_author_code, "自動換著者號"), **btn_style).pack(pady=12)
ctk.CTkButton(root, text="自動找封面(快)", command=lambda: handle_normal_task(run_get_covers, "自動找封面"), **btn_style).pack(pady=12)
ctk.CTkButton(root, text="協助查價錢", command=lambda: handle_normal_task(run_catchbook, "協助查價錢"), **btn_style).pack(pady=12)

root.mainloop()