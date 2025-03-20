import minecraft_launcher_lib
import subprocess
import tkinter as tk
from tkinter import messagebox


minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()


def launch_minecraft():
    version = version_var.get()
    username = username_var.get()

    if not version or not username:
        messagebox.showerror("Ошибка", "Выберите версию и введите никнейм!")
        return

    messagebox.showinfo("Установка", f"Начинаем установку версии {version}...")

   
    try:
        callback = {
            "setStatus": lambda text: status_label.config(text=text),
            "setProgress": lambda value: progress_bar.config(value=value),
        }
        minecraft_launcher_lib.install.install_minecraft_version(
            versionid=version,
            minecraft_directory=minecraft_directory,
            callback=callback,
            force=True  
        )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при установке: {e}")
        return

    messagebox.showinfo("Запуск", f"Запускаем Minecraft {version} для {username}...")


    options = {
        "username": username,
    }

    try:
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(
            version=version,
            minecraft_directory=minecraft_directory,
            options=options
        ))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при запуске: {e}")


try:
    versions = minecraft_launcher_lib.utils.get_version_list()
    version_list = [v["id"] for v in versions if v["type"] in ["release", "snapshot"]]
except Exception as e:
    version_list = []
    messagebox.showerror("Ошибка", f"Не удалось получить список версий: {e}")


root = tk.Tk()
root.title("Minecraft Launcher")

# Поле выбора версии
tk.Label(root, text="Выберите версию:").pack()
version_var = tk.StringVar(root)
version_menu = tk.OptionMenu(root, version_var, *version_list)
version_menu.pack()


tk.Label(root, text="Введите никнейм:").pack()
username_var = tk.StringVar(root)
username_entry = tk.Entry(root, textvariable=username_var)
username_entry.pack()


launch_button = tk.Button(root, text="Запустить Minecraft", command=launch_minecraft)
launch_button.pack()

status_label = tk.Label(root, text="Ожидание запуска...", fg="blue")
status_label.pack()

# Прогресс-бар
progress_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", length=300)
progress_bar.pack()


root.mainloop()
