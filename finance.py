import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data.json"

# --- Модуль Storage ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Если файл поврежден — создаем новый
        messagebox.showwarning("Ошибка", "Файл данных поврежден, создан новый файл.")
        save_data([]) # Перезаписываем битый файл пустым
        return []

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except PermissionError:
        messagebox.showerror("Ошибка", "Нет прав на запись в файл данных!")

# --- Модуль Logic ---
def calculate_total(data):
    # Магическое число исправлено на константу
    return sum(item["amount"] for item in data)

# --- Модуль UI ---
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Офлайн-трекер финансов")
        self.root.geometry("600x400")
        
        self.data = load_data()

        # Поля ввода
        frame_input = tk.Frame(self.root, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="Категория:").pack(side="left", padx=5)
        self.entry_category = tk.Entry(frame_input, width=15)
        self.entry_category.pack(side="left", padx=5)

        tk.Label(frame_input, text="Сумма:").pack(side="left", padx=5)
        self.entry_amount = tk.Entry(frame_input, width=10)
        self.entry_amount.pack(side="left", padx=5)

        tk.Button(frame_input, text="Добавить", command=self.add_expense, bg="lightgreen").pack(side="left", padx=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Category", "Amount"), show="headings")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Amount", text="Сумма")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Итог
        self.label_total = tk.Label(self.root, text="Итого: 0", font=("Arial", 14, "bold"))
        self.label_total.pack(pady=10)

        self.update_table()

    def add_expense(self):
        category = self.entry_category.get()
        amount_str = self.entry_amount.get()

        # Валидация
        if not category:
            messagebox.showerror("Ошибка", "Введите категорию!")
            return
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError("Сумма не может быть отрицательной!")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверная сумма: {e}")
            return

        self.data.append({"category": category, "amount": amount})
        save_data(self.data)
        self.update_table()
        
        # Очистка полей
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.data:
            self.tree.insert("", tk.END, values=(item["category"], item["amount"]))
        self.label_total.config(text=f"Итого: {calculate_total(self.data)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()