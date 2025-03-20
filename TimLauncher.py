import minecraft_launcher_lib
import subprocess
import os
import tkinter as tk
from tkinter import ttk, messagebox


MINECRAFT_VERSION = "1.20.1"


minecraft_directory = os.path.join(
    os.path.dirname(minecraft_launcher_lib.utils.get_minecraft_directory()), "TimLauncher"
)

# Функция обновления прогресса
def set_progress(value):
    progress_bar["value"] = value

def set_max(value):
    progress_bar["maximum"] = value

def set_status(text):
    log_label.config(text=text)


callback = {
    "setStatus": lambda text: set_status(text),
    "setProgress": lambda value: set_progress(value),
    "setMax": lambda value: set_max(value)
}

def install_minecraft():
    username = username_entry.get().strip()

    if not username:
        messagebox.showerror("Ошибка", "Введите имя пользователя!")
        return

    log_label.config(text=f"Устанавливаем Minecraft {MINECRAFT_VERSION}...")
    
    try:
        minecraft_launcher_lib.install.install_minecraft_version(
            versionid=MINECRAFT_VERSION, 
            minecraft_directory=minecraft_directory, 
            callback=callback
        )
        messagebox.showinfo("Успех", "Minecraft установлен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка установки: {e}")

# Функция запуска Minecraft
def launch_minecraft():
    username = username_entry.get().strip()

    if not username:
        messagebox.showerror("Ошибка", "Введите имя пользователя!")
        return

    options = {"username": username}

    try:
        log_label.config(text="Запуск Minecraft...")
        subprocess.call(
            minecraft_launcher_lib.command.get_minecraft_command(
                version=MINECRAFT_VERSION,
                minecraft_directory=minecraft_directory,
                options=options
            )
        )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка запуска: {e}")

# Создание окна
root = tk.Tk()
root.title("TimLauncher")
root.geometry("400x250")
root.resizable(False, False)


title_label = tk.Label(root, text="TimLauncher", font=("Arial", 16, "bold"))
title_label.pack(pady=10)


username_label = tk.Label(root, text="Имя пользователя:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack(pady=5)


install_button = tk.Button(root, text="Установить Minecraft", command=install_minecraft)
install_button.pack(pady=5)

launch_button = tk.Button(root, text="Запустить Minecraft", command=launch_minecraft)
launch_button.pack(pady=5)


progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=5)

# Лог-вывод
log_label = tk.Label(root, text="", font=("Arial", 10))
log_label.pack()

# Запуск GUI
root.mainloop()
