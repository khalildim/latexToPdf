import os
import platform
import shutil
import subprocess
import urllib.request
from tkinter import messagebox, Tk

# Ensure a root window exists for messageboxes
root = Tk()
root.withdraw()

def install_miktex_windows():
    url = "https://mirror.dogado.de/tex-archive/systems/win32/miktex/setup/windows-x64/basic-miktex-24.1-x64.exe"
    installer_path = os.path.join(os.getenv("TEMP"), "basic-miktex-installer.exe")

    try:
        urllib.request.urlretrieve(url, installer_path)
        subprocess.run([installer_path], check=True)
        messagebox.showinfo("Installation", "✅ MiKTeX installed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ MiKTeX installation failed:\n{e}")

def install_mactex():
    url = "https://mirror.dogado.de/tex-archive/systems/mac/mactex/MacTeX.pkg"
    pkg_path = "/tmp/MacTeX.pkg"
    try:
        urllib.request.urlretrieve(url, pkg_path)
        subprocess.run(["sudo", "installer", "-pkg", pkg_path, "-target", "/"], check=True)
        messagebox.showinfo("Installation", "✅ MacTeX installed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ MacTeX installation failed:\n{e}")

def install_texlive_linux():
    try:
        messagebox.showinfo("Permission Required", "ℹ️ You'll be asked for your password to install LaTeX.")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "texlive-full"], check=True)
        messagebox.showinfo("Installation", "✅ TeX Live installed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ TeX Live installation failed:\n{e}")

def is_pdflatex_installed(os_name):
    if shutil.which("pdflatex") is None:
        msg = "LaTeX is not installed. Do you want to install it now?"
        if not messagebox.askyesno("Missing LaTeX", msg):
            return

        if os_name == "Windows":
            install_miktex_windows()
        elif os_name == "Darwin":
            install_mactex()
        elif os_name == "Linux":
            install_texlive_linux()
    else:
        messagebox.showinfo("Installed", "✅ LaTeX is already installed.")

class Setup:
    def __init__(self):
        os_name = platform.system()
        print("Detected OS:", os_name)
        is_pdflatex_installed(os_name)

if __name__ == "__main__":
    Setup()
