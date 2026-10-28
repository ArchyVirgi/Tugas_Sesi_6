import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Mengimpor seluruh modul file CRUD SIAKAD
import app_dosen
import app_mahasiswa
import app_jadwal_kuliah
import app_krs
import app_mata_kuliah
import app_ukt

# Deklarasi kelas utama untuk mengelola antarmuka (GUI) jendela login
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - SIAKAD")
        self.root.geometry("380x250")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Konfigurasi koneksi database MySQL
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'siakad'
        }

        # Membuat container/frame utama untuk menampung seluruh elemen visual
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Membuat elemen teks/label judul utama form login
        lbl_title = tk.Label(
            main_frame, 
            text="SIAKAD LOGIN", 
            font=("Arial", 14, "bold"), 
            bg="#f0f0f0", 
            fg="black"
        )
        lbl_title.pack(pady=(0, 20))

        # Membuat sub-frame khusus untuk menyusun label dan input teks menggunakan tata letak Grid
        form_frame = tk.Frame(main_frame, bg="#f0f0f0")
        form_frame.pack()

        # Baris 0: Label petunjuk input Username (NIP)
        lbl_user = tk.Label(form_frame, text="Username:", font=("Arial", 10), bg="#f0f0f0", anchor="e", width=10)
        lbl_user.grid(row=0, column=0, padx=5, pady=6, sticky="e")
        
        self.entry_nip = tk.Entry(form_frame, font=("Arial", 10), width=22, relief=tk.SOLID, bd=1)
        self.entry_nip.grid(row=0, column=1, padx=5, pady=6)
        self.entry_nip.focus()

        # Baris 1: Label petunjuk input Password (Email)
        lbl_pass = tk.Label(form_frame, text="Password:", font=("Arial", 10), bg="#f0f0f0", anchor="e", width=10)
        lbl_pass.grid(row=1, column=0, padx=5, pady=6, sticky="e")
        
        self.entry_email = tk.Entry(form_frame, font=("Arial", 10), width=22, show="*", relief=tk.SOLID, bd=1)
        self.entry_email.grid(row=1, column=1, padx=5, pady=6)

        # Membuat tombol (button) untuk eksekusi tindakan login
        btn_login = tk.Button(
            main_frame, 
            text="Login", 
            font=("Arial", 10, "bold"), 
            bg="#4CAF50", 
            fg="white", 
            activebackground="#45a049", 
            activeforeground="white", 
            width=15, 
            bd=1, 
            cursor="hand2", 
            command=self.proses_login
        )
        btn_login.pack(pady=(20, 0))

        # Mengikat (binding) tombol 'Enter' pada keyboard untuk menjalankan fungsi proses_login()
        self.root.bind('<Return>', lambda event: self.proses_login())

    # Metode untuk menangani alur verifikasi data login pengampu
    def proses_login(self):
        nip = self.entry_nip.get().strip()
        email = self.entry_email.get().strip()

        if not nip or not email:
            messagebox.showwarning("Peringatan", "Username (NIP) dan Password (Email) wajib diisi!")
            return

        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT nip, nama_dosen, email FROM dosen WHERE nip = %s AND email = %s"
            cursor.execute(query, (nip, email))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Berhasil", f"Login berhasil!\nSelamat datang, {user['nama_dosen']}.")
                # Memanggil fungsi buka_dashboard setelah login sukses
                self.buka_dashboard(user)
            else:
                messagebox.showerror("Gagal", "Login gagal! Username atau Password salah.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Koneksi database bermasalah:\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # Metode untuk membuka Menu Utama / Dashboard setelah login berhasil
    def buka_dashboard(self, user):
        # Menutup jendela login
        self.root.destroy()

        # Membuat Jendela Baru untuk Menu Utama SIAKAD
        dashboard = tk.Tk()
        dashboard.title("Sistem Informasi Akademik (SIAKAD) - Menu Utama")
        dashboard.geometry("500x550")
        dashboard.configure(bg="#f9f9f9")

        # Sapaan nama dosen yang sedang login
        tk.Label(dashboard, text=f"Halo, {user['nama_dosen']}", font=("Arial", 14, "bold"), bg="#f9f9f9").pack(pady=(20, 5))
        tk.Label(dashboard, text="Silakan pilih menu pengelolaan data di bawah:", font=("Arial", 10), bg="#f9f9f9", fg="gray").pack(pady=(0, 20))

        # Fungsi navigasi untuk membuka masing-masing Form CRUD (Sudah Disinkronkan)
        def buka_form_dosen():
            app_dosen.run_dosen()

        def buka_form_mahasiswa():
            app_mahasiswa.run_mahasiswa()

        def buka_form_jadwal():
            app_jadwal_kuliah.run_jadwal()

        def buka_form_krs():
            app_krs.run_krs()

        def buka_form_matkul():
            app_mata_kuliah.run_matkul()

        def buka_form_ukt():
            app_ukt.run_ukt()

        # Tombol-Tombol Navigasi Menu Utama (6 Tombol Lengkap)
        tk.Button(dashboard, text="Kelola Data Dosen", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=30, height=2, command=buka_form_dosen, cursor="hand2").pack(pady=5)
        tk.Button(dashboard, text="Kelola Data Mahasiswa", font=("Arial", 10, "bold"), bg="#FF9800", fg="white", width=30, height=2, command=buka_form_mahasiswa, cursor="hand2").pack(pady=5)
        tk.Button(dashboard, text="Kelola Jadwal Kuliah", font=("Arial", 10, "bold"), bg="#9C27B0", fg="white", width=30, height=2, command=buka_form_jadwal, cursor="hand2").pack(pady=5)
        tk.Button(dashboard, text="Kelola KRS Mahasiswa", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=30, height=2, command=buka_form_krs, cursor="hand2").pack(pady=5)
        tk.Button(dashboard, text="Kelola Mata Kuliah", font=("Arial", 10, "bold"), bg="#009688", fg="white", width=30, height=2, command=buka_form_matkul, cursor="hand2").pack(pady=5)
        tk.Button(dashboard, text="Kelola Pembayaran UKT", font=("Arial", 10, "bold"), bg="#607D8B", fg="white", width=30, height=2, command=buka_form_ukt, cursor="hand2").pack(pady=5)

        # Tombol Keluar / Tutup Aplikasi
        tk.Button(dashboard, text="Keluar", font=("Arial", 9), bg="#f44336", fg="white", width=15, command=dashboard.destroy, cursor="hand2").pack(pady=(25, 0))

        dashboard.mainloop()

# Titik awal eksekusi program Python (Main Entry Point)
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
