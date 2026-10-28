import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_mahasiswa():
    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="siakad"
        )

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT nim, nama_lengkap, jenis_kelamin, tanggal_lahir, tempat_lahir, alamat, no_telepon, email, jurusan, angkatan, status FROM mahasiswa")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data mahasiswa: {e}")

    window_mhs = tk.Toplevel()
    window_mhs.title("Pengelolaan Data Mahasiswa - SIAKAD")
    window_mhs.geometry("1100x500")

    frame_table = tk.Frame(window_mhs)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)

    columns = ("NIM", "Nama Lengkap", "JK", "Tanggal Lahir", "Tempat Lahir", "Alamat", "No Telp", "Email", "Jurusan", "Angkatan", "Status")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    scroll_y = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)
    
    load_data()
