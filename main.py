import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Предопределённые цитаты
quotes = [
    {"text": "Жизнь - это 10% того, что с тобой происходит, и 90% того, как ты реагируешь на это.", "author": "Чарльз Свиндолл", "topic": "жизнь"},
    {"text": "Лучше сделать и пожалеть, чем пожалеть, что не сделал.", "author": "Роберт Кийосаки", "topic": "мотивация"},
    {"text": "Успех — это способность идти от неудачи к неудаче без потери энтузиазма.", "author": "Винстон Черчилль", "topic": "успех"},
    {"text": "Только тот, кто рискнул пойти далеко, узнает, насколько он далеко может зайти.", "author": "Томас Джефферсон", "topic": "риски"},
    # добавьте больше цитат по желанию
]

history = []

HISTORY_FILE = 'history.json'

# Загрузка истории при запуске
def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []

# Сохранение истории при закрытии
def save_history():
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Основное окно
root = tk.Tk()
root.title("Random Quote Generator")

# Обработчик закрытия
def on_closing():
    save_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
author_filter_var = tk.StringVar()
author_filter_entry = tk.Entry(filter_frame, textvariable=author_filter_var)
author_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
topic_filter_var = tk.StringVar()
topic_filter_entry = tk.Entry(filter_frame, textvariable=topic_filter_var)
topic_filter_entry.grid(row=0, column=3, padx=5)

def apply_filters():
    author_filter = author_filter_var.get().lower()
    topic_filter = topic_filter_var.get().lower()
    filtered = [q for q in quotes if
                (author_filter in q['author'].lower()) and
                (topic_filter in q['topic'].lower())]
    return filtered

# Функция для генерации и отображения цитаты
def generate_quote():
    filtered_quotes = apply_filters()
    if not filtered_quotes:
        messagebox.showinfo("Нет цитат", "Нет цитат, соответствующих фильтру.")
        return
    quote = random.choice(filtered_quotes)
    display_quote(quote)
    # Добавляем в историю
    history.append(quote)
    update_history_list()

# Область для отображения цитаты
quote_frame = tk.Frame(root)
quote_frame.pack(pady=10)

quote_text = tk.Text(quote_frame, wrap='word', width=60, height=5, font=("Arial", 12))
quote_text.pack()

def display_quote(quote):
    quote_text.delete(1.0, tk.END)
    text = f"\"{quote['text']}\"\n\n— {quote['author']} ({quote['topic']})"
    quote_text.insert(tk.END, text)

# История
history_frame = tk.Frame(root)
history_frame.pack(pady=10)

tk.Label(history_frame, text="История:").pack()

history_listbox = tk.Listbox(history_frame, width=80, height=10)
history_listbox.pack()

def update_history_list():
    history_listbox.delete(0, tk.END)
    for h in reversed(history):
        display_text = f"\"{h['text']}\" — {h['author']} ({h['topic']})"
        history_listbox.insert(tk.END, display_text)

# Кнопка генерации
generate_button = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_button.pack(pady=5)

# Функция для добавления новой цитаты (по желанию)
def add_new_quote():
    text = new_text_entry.get().strip()
    author = new_author_entry.get().strip()
    topic = new_topic_entry.get().strip()
    if not text or not author or not topic:
        messagebox.showwarning("Ошибка", "Все поля обязательно заполнить.")
        return
    new_q = {'text': text, 'author': author, 'topic': topic}
    quotes.append(new_q)
    messagebox.showinfo("Успех", "Цитата добавлена.")
    # Очистка полей
    new_text_entry.delete(0, tk.END)
    new_author_entry.delete(0, tk.END)
    new_topic_entry.delete(0, tk.END)

# Поля для добавления новой цитаты (опционально)
add_frame = tk.LabelFrame(root, text="Добавить новую цитату")
add_frame.pack(pady=10, fill='x', padx=10)

tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky='e')
new_text_entry = tk.Entry(add_frame, width=50)
new_text_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky='e')
new_author_entry = tk.Entry(add_frame, width=50)
new_author_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky='e')
new_topic_entry = tk.Entry(add_frame, width=50)
new_topic_entry.grid(row=2, column=1, padx=5, pady=2)

add_button = tk.Button(add_frame, text="Добавить цитату", command=add_new_quote)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

# Кнопки для фильтрации
filter_button = tk.Button(root, text="Применить фильтры", command=update_history_list)
filter_button.pack(pady=5)

# Загружать историю при запуске
load_history()
update_history_list()

root.mainloop()