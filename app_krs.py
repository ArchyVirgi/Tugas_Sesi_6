import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_krs():
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
            cursor.execute("SELECT id_krs, nim, kode_mk, semester_ambil, tahun_ajaran, nilai_huruf, nilai_angka FROM krs")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    window_krs = tk.Toplevel()
    window_krs.title("Pengelolaan KRS Mahasiswa - SIAKAD")
    window_krs.geometry("900x450")

    frame_table = tk.Frame(window_krs)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)
    
    columns = ("ID KRS", "NIM", "Kode MK", "Semester Ambil", "Tahun Ajaran", "Nilai Huruf", "Nilai Angka")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True)

    load_data()
