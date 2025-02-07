import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список задач")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.tasks = []

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_entry = ttk.Entry(self.frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ttk.Button(self.frame, text="Добавить", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.listbox = tk.Listbox(
            self.root, selectmode=tk.MULTIPLE, width=50, height=15
        )
        self.listbox.pack(pady=10)

        self.scrollbar = ttk.Scrollbar(self.root, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.delete_button = ttk.Button(
            self.root, text="Удалить выбранные", command=self.delete_selected
        )
        self.delete_button.pack(pady=5)
        self.root.bind("<Delete>", lambda event: self.delete_selected())

        self.clear_button = ttk.Button(
            self.root, text="Очистить всё", command=self.clear_all
        )
        self.clear_button.pack()

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Ошибка", "Введите задание!")

    def delete_selected(self):
        selected = list(self.listbox.curselection())[::-1]
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задание для удаления!")
            return

        for index in selected:
            self.listbox.delete(index)
            del self.tasks[index]

        self.root.after(300, self.save_tasks)

    def clear_all(self):
        if messagebox.askyesno(
            "Подтверждение", "Вы уверены, что хотите удалить все задачи?"
        ):
            self.tasks.clear()
            self.listbox.delete(0, tk.END)
            self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.listbox.insert(tk.END, task)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
