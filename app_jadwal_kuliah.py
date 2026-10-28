import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_jadwal():
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
            cursor.execute("SELECT id_jadwal, kode_mk, hari, jam_mulai, jam_selesai, ruangan FROM jadwal_kuliah")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    window_jadwal = tk.Toplevel()
    window_jadwal.title("Pengelolaan Jadwal Kuliah - SIAKAD")
    window_jadwal.geometry("850x450")

    frame_table = tk.Frame(window_jadwal)
    frame_table.pack(fill="both", expand=True, padx=15, pady=15)
    
    columns = ("ID Jadwal", "Kode MK", "Hari", "Jam Mulai", "Jam Selesai", "Ruangan")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(fill="both", expand=True)

    load_data()
