import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_dosen():
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
            cursor.execute("SELECT nip, nama_dosen, jenis_kelamin, email, no_telepon, pendidikan_terakhir, bidang_keahlian FROM dosen")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    # Membuat Jendela Baru pop-up
    window_dosen = tk.Toplevel()
    window_dosen.title("Pengelolaan Data Dosen - SIAKAD")
    window_dosen.geometry("900x500")

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_dosen)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)
    
    columns = ("NIP", "Nama Dosen", "JK", "Email", "No Telp", "Pendidikan", "Keahlian")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")
    tree.pack(fill="both", expand=True)
    
    load_data()
