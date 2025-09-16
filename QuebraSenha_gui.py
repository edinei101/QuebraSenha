import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class QuebraSenhaApp:
    def __init__(self, master):
        self.master = master
        master.title("QuebraSenha")

        self.zip_var = tk.StringVar()
        self.wordlist_var = tk.StringVar()
        self.sevenzip_path = None
        self.sevenzip_label_var = tk.StringVar(value="Não detectado")

        # Seleção de ZIP
        tk.Label(master, text="Arquivo ZIP:").pack(anchor="w")
        tk.Entry(master, textvariable=self.zip_var, width=50).pack(anchor="w")
        tk.Button(master, text="Selecionar ZIP", command=self.select_zip).pack(anchor="w", pady=2)

        # Seleção de Wordlist
        tk.Label(master, text="Wordlist:").pack(anchor="w")
        tk.Entry(master, textvariable=self.wordlist_var, width=50).pack(anchor="w")
        tk.Button(master, text="Selecionar Wordlist", command=self.select_wordlist).pack(anchor="w", pady=2)

        # Seleção de 7-Zip
        tk.Label(master, text="7-Zip:").pack(anchor="w")
        tk.Label(master, textvariable=self.sevenzip_label_var).pack(anchor="w")
        tk.Button(master, text="Selecionar 7z.exe", command=self.select_sevenzip).pack(anchor="w", pady=2)

        # Botão iniciar
        tk.Button(master, text="Iniciar Quebra", command=self.start_crack).pack(pady=4)

        # Log
        self.log = tk.Text(master, height=10, width=70)
        self.log.pack(padx=8, pady=8)

        self.detect_sevenzip()

    def select_zip(self):
        path = filedialog.askopenfilename(filetypes=[("Arquivos ZIP", "*.zip")])
        if path:
            self.zip_var.set(path)

    def select_wordlist(self):
        path = filedialog.askopenfilename(filetypes=[("Arquivos TXT", "*.txt")])
        if path:
            self.wordlist_var.set(path)

    def select_sevenzip(self):
        path = filedialog.askopenfilename(filetypes=[("Executável 7-Zip", "7z.exe")])
        if path:
            self.sevenzip_path = path
            self.sevenzip_label_var.set(path)

    def detect_sevenzip(self):
        candidates = [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]
        for c in candidates:
            if os.path.exists(c):
                self.sevenzip_path = c
                self.sevenzip_label_var.set(c)
                self.log.insert(tk.END, f"7-Zip detectado automaticamente: {c}\n")
                return
        self.sevenzip_path = None
        self.sevenzip_label_var.set("Não detectado")
        self.log.insert(tk.END, "7-Zip não detectado. Use o botão para selecionar manualmente.\n")

    def start_crack(self):
        zip_path = self.zip_var.get()
        wordlist_path = self.wordlist_var.get()

        if not zip_path:
            messagebox.showerror("Erro", "Selecione um arquivo ZIP.")
            return

        if not wordlist_path or not os.path.exists(wordlist_path):
            messagebox.showerror("Erro", "Selecione uma wordlist válida.")
            return

        if not self.sevenzip_path:
            messagebox.showerror("Erro", "7-Zip não configurado.")
            return

        # Leitura da wordlist
        with open(wordlist_path, "r", encoding="utf-8") as f:
            senhas = [line.strip() for line in f]

        self.log.insert(tk.END, f"Iniciando quebra de senha em {zip_path}...\n")

        senha_encontrada = None

        for idx, senha in enumerate(senhas, 1):
            # Executa 7-Zip para testar senha
            result = subprocess.run([self.sevenzip_path, "t", "-p" + senha, zip_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "Everything is Ok" in result.stdout:
                senha_encontrada = senha
                break
            if idx % 50 == 0:
                self.log.insert(tk.END, f"Tentativa {idx}: {senha} falhou\n")
                self.log.see(tk.END)

        if senha_encontrada:
            self.log.insert(tk.END, f"\n=== Senha encontrada: {senha_encontrada} ===\n")
            messagebox.showinfo("Senha encontrada", f"A senha é: {senha_encontrada}")
        else:
            self.log.insert(tk.END, "\n=== Nenhuma senha funcionou ===\n")
            messagebox.showwarning("Falha", "Nenhuma senha funcionou.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuebraSenhaApp(root)
    root.mainloop()



