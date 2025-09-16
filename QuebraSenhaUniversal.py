# QuebraSenhaUniversal.py
# Funciona para ZipCrypto (zipfile) e AES (7-Zip)
# Requer: 7-Zip instalado e acessível via "7z"

import zipfile
import subprocess
import os
import sys
import shutil

def is_zip_aes(zip_path):
    """Detecta se o ZIP provavelmente usa AES"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                try:
                    zf.read(info.filename)
                except RuntimeError as e:
                    if "AES" in str(e) or "encrypted" in str(e):
                        return True
        return False
    except zipfile.BadZipFile:
        return True
    except:
        return True

def try_zipfile(zip_path, wordlist):
    """Tenta quebrar ZIP ZipCrypto usando zipfile"""
    print("Tentando ZipCrypto com zipfile...")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            target = zf.namelist()[0]
            with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    pw = line.strip()
                    if not pw:
                        continue
                    try:
                        zf.read(target, pwd=pw.encode("utf-8"))
                        print(f"✅ SENHA ENCONTRADA (ZipCrypto): '{pw}'")
                        return pw
                    except:
                        if i % 50 == 0:
                            print(f"{i} tentativas... ultima: {pw}")
        print("Nenhuma senha funcionou no ZipCrypto")
        return None
    except Exception as e:
        print("Erro no zipfile:", e)
        return None

def try_7zip(zip_path, wordlist):
    """Tenta quebrar ZIP AES usando 7z"""
    print("Tentando AES com 7z...")
    if not shutil.which("7z"):
        print("ERRO: 7z nao encontrado no PATH. Instale 7-Zip.")
        return None
    out_dir = "tmp_extract"
    os.makedirs(out_dir, exist_ok=True)
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            pw = line.strip()
            if not pw:
                continue
            cmd = ["7z", "x", zip_path, f"-p{pw}", "-y", f"-o{out_dir}"]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                print(f"✅ SENHA ENCONTRADA (AES/7z): '{pw}'")
                return pw
            if i % 20 == 0:
                print(f"{i} tentativas com 7z...")
    print("Nenhuma senha funcionou com 7z")
    return None

def main():
    if len(sys.argv) != 3:
        print("Uso: python QuebraSenhaUniversal.py arquivo.zip wordlist.txt")
        sys.exit(1)
    zip_path = sys.argv[1]
    wordlist = sys.argv[2]
    if not os.path.exists(zip_path) or not os.path.exists(wordlist):
        print("Arquivo zip ou wordlist nao encontrado.")
        sys.exit(1)

    # Detecta tipo de criptografia
    aes = is_zip_aes(zip_path)
    if aes:
        print("Parece que o ZIP usa AES. Vamos usar 7-Zip.")
        senha = try_7zip(zip_path, wordlist)
    else:
        print("Parece que o ZIP usa ZipCrypto. Vamos usar zipfile.")
        senha = try_zipfile(zip_path, wordlist)

    if senha:
        print(f"\n***** SENHA FINAL ENCONTRADA: {senha} *****")
    else:
        print("\nNenhuma senha funcionou.")

if __name__ == "__main__":
    main()


# QuebraSenhaUniversal.py
import zipfile
import subprocess
import os
import shutil
import sys

def is_zip_aes(zip_path):
    """Detecta se o ZIP usa AES ou ZipCrypto"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                try:
                    zf.read(info.filename)
                except RuntimeError as e:
                    if "AES" in str(e) or "encrypted" in str(e):
                        return True
        return False
    except:
        return True

def try_zipfile(zip_path, wordlist):
    """Tenta quebrar ZipCrypto usando zipfile"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            target = zf.namelist()[0]
            with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    pw = line.strip()
                    if not pw:
                        continue
                    try:
                        zf.read(target, pwd=pw.encode("utf-8"))
                        return pw
                    except:
                        if i % 50 == 0:
                            print(f"{i} tentativas... ultima: {pw}")
        return None
    except:
        return None

def try_7zip(zip_path, wordlist):
    """Tenta quebrar AES usando 7-Zip"""
    sevenzip = shutil.which("7z")
    if not sevenzip:
        print("ERRO: 7z não encontrado no PATH. Instale ou adicione manualmente.")
        return None

    out_dir = "tmp_extract"
    os.makedirs(out_dir, exist_ok=True)

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            pw = line.strip()
            if not pw:
                continue
            cmd = [sevenzip, "x", zip_path, f"-p{pw}", "-y", f"-o{out_dir}"]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode == 0:
                return pw
            if i % 20 == 0:
                print(f"{i} tentativas com 7z...")
    return None

def main():
    if len(sys.argv) != 3:
        print("Uso: python QuebraSenhaUniversal.py arquivo.zip wordlist.txt")
        sys.exit(1)

    zip_path = sys.argv[1]
    wordlist = sys.argv[2]

    if not os.path.exists(zip_path):
        print("Arquivo ZIP não encontrado!")
        sys.exit(1)
    if not os.path.exists(wordlist):
        print("Wordlist não encontrada!")
        sys.exit(1)

    print("Detectando tipo de criptografia...")
    aes = is_zip_aes(zip_path)

    if aes:
        print("AES detectado. Usando 7-Zip...")
        senha = try_7zip(zip_path, wordlist)
    else:
        print("ZipCrypto detectado. Usando zipfile...")
        senha = try_zipfile(zip_path, wordlist)

    if senha:
        print(f"SENHA ENCONTRADA: {senha}")
    else:
        print("Nenhuma senha funcionou.")

if __name__ == "__main__":
    main()
