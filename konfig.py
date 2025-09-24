import tkinter as tk
from tkinter import scrolledtext
import shlex

root = tk.Tk()
root.title("VFS")
root.geometry("800x600")#главное окно


console_output = scrolledtext.ScrolledText(root, state='disabled', bg='white', fg='black')
console_output.pack(expand=True, fill='both', padx=5, pady=5)#  окно вывода(#pack размещает виджет в окне с расширением на все доступное пространство)


input_entry = tk.Entry(root, bg='white', fg='black', insertbackground='black')
input_entry.pack(fill='x', padx=5, pady=5)#  окно ввода

def print_to_console(text):
    console_output.configure(state='normal')
    console_output.insert(tk.END, text + "\n")
    console_output.see(tk.END)#рокрутили в конец
    console_output.configure(state='disabled')

def handle_command(event=None):
    command_line = input_entry.get().strip()
    print_to_console(command_line)
    input_entry.delete(0, tk.END)#очистили строку ввода

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
            print_to_console(f"Ошибка: Неизвестная ошибка '{command}'")

    except ValueError as e:
        print_to_console(f"Ошибка: Неверные аргументы - {e}")


input_entry.bind("<Return>", handle_command)

root.mainloop()
