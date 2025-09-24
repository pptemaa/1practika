import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys
import os
vfs_path = None
startup_script = None

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--vfs-path" and i + 1 < len(sys.argv):
        vfs_path = sys.argv[i + 1]
    elif sys.argv[i] == "--startup-script" and i + 1 < len(sys.argv):
        startup_script = sys.argv[i + 1]

root = tk.Tk()
root.title("VFS")
root.geometry("800x600")

console_output = scrolledtext.ScrolledText(root, state='disabled', bg='white', fg='black')
console_output.pack(expand=True, fill='both', padx=5, pady=5)

input_entry = tk.Entry(root, bg='white', fg='black', insertbackground='black')
input_entry.pack(fill='x', padx=5, pady=5)

def print_to_console(text):
    console_output.configure(state='normal')
    console_output.insert(tk.END, text + "\n")
    console_output.see(tk.END)
    console_output.configure(state='disabled')

print_to_console(" Параметры запуска:")
print_to_console(f"VFS путь: {vfs_path}")
print_to_console(f"Стартовый скрипт: {startup_script}")

def execute_startup_script(script_path):
    if not os.path.exists(script_path):
        print_to_console(f"Ошибка: Скрипт не найден: {script_path}")
        return
   
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                print_to_console(line)
                handle_script_command(line)
    except Exception as e:
        print_to_console(f"Ошибка выполнения скрипта: {e}")

def handle_script_command(command_line):
    try:
        args = shlex.split(command_line)
        command = args[0]
        command_args = args[1:]
        
        if command == "exit":
            root.destroy()
        elif command == "ls":
            print_to_console(f"Команда 'ls' с аргументами: {command_args}")
        elif command == "cd":
            print_to_console(f"Команда 'cd' с аргументами: {command_args}")
        else:
            print_to_console(f"Ошибка: Неизвестная команда '{command}'")
            
    except Exception as e:
        print_to_console(f"Ошибка: {e}")

def handle_command(event=None):
    command_line = input_entry.get().strip()
    print_to_console(command_line)
    input_entry.delete(0, tk.END)

    if not command_line:
        return

    try:
        args = shlex.split(command_line)
        command = args[0]
        command_args = args[1:]
        
        if command == "exit":
            root.destroy()
        elif command == "ls":
            print_to_console(f"Команда 'ls' с аргументами: {command_args}")
        elif command == "cd":
            print_to_console(f"Команда 'cd' с аргументами: {command_args}")
        else:
            print_to_console(f"Ошибка: Неизвестная команда '{command}'")

    except ValueError as e:
        print_to_console(f"Ошибка: Неверные аргументы - {e}")

input_entry.bind("<Return>", handle_command)

if startup_script:
    execute_startup_script(startup_script)

root.mainloop()
