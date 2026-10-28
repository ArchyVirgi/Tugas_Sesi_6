import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_matkul():
    def connect_db():
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="siakad"
        )

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT kode_mk, nama_mk, sks, semester, nip_dosen FROM mata_kuliah")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    window_matkul = tk.Toplevel()
    window_matkul.title("Pengelolaan Data Mata Kuliah - SIAKAD")
    window_matkul.geometry("800x450")

    frame_table = tk.Frame(window_matkul)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)
    
    columns = ("Kode MK", "Nama Mata Kuliah", "SKS", "Semester", "NIP Dosen")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(fill="both", expand=True)

    load_data()
