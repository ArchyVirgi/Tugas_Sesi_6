import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_ukt():
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
            cursor.execute("SELECT id_pembayaran, nim, semester, tahun_ajaran, jumlah_bayar, tanggal_bayar, metode_pembayaran, status FROM pembayaran_ukt")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    window_ukt = tk.Toplevel()
    window_ukt.title("Pengelolaan Pembayaran UKT - SIAKAD")
    window_ukt.geometry("950x450")

    frame_table = tk.Frame(window_ukt)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)
    
    columns = ("ID", "NIM", "Semester", "Tahun Ajaran", "Jumlah Bayar", "Tanggal Bayar", "Metode", "Status")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")
    tree.pack(fill="both", expand=True)

    load_data()
