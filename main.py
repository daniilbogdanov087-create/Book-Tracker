import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []

        # Вводные поля
        self.create_input_fields()

        # Таблица
        self.create_treeview()

        # Фильтр
        self.create_filter_section()

        # Кнопки
        self.create_buttons()

        # Загрузка данных при запуске (по желанию)
        # self.load_from_json()

    def create_input_fields(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text='Название книги:').grid(row=0, column=0, sticky='w')
        self.title_entry = ttk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(frame, text='Автор:').grid(row=1, column=0, sticky='w')
        self.author_entry = ttk.Entry(frame)
        self.author_entry.grid(row=1, column=1)

        ttk.Label(frame, text='Жанр:').grid(row=2, column=0, sticky='w')
        self.genre_entry = ttk.Entry(frame)
        self.genre_entry.grid(row=2, column=1)

        ttk.Label(frame, text='Количество страниц:').grid(row=3, column=0, sticky='w')
        self.pages_entry = ttk.Entry(frame)
        self.pages_entry.grid(row=3, column=1)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.root, columns=('Title', 'Author', 'Genre', 'Pages'), show='headings')
        for col in ('Title', 'Author', 'Genre', 'Pages'):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10)

    def create_filter_section(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(filter_frame, text='Фильтр по жанру:').grid(row=0, column=0)
        self.genre_filter = ttk.Combobox(filter_frame, values=[])
        self.genre_filter.grid(row=0, column=1)

        ttk.Label(filter_frame, text='Кол-во страниц больше:').grid(row=0, column=2)
        self.pages_filter_var = tk.StringVar()
        self.pages_filter_entry = ttk.Entry(filter_frame, textvariable=self.pages_filter_var)
        self.pages_filter_entry.grid(row=0, column=3)

        ttk.Button(filter_frame, text='Применить фильтр', command=self.apply_filter).grid(row=0, column=4)
        ttk.Button(filter_frame, text='Сбросить фильтр', command=self.reset_filter).grid(row=0, column=5)

    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=10)

        ttk.Button(button_frame, text='Добавить книгу', command=self.add_book).grid(row=0, column=0)
        ttk.Button(button_frame, text='Сохранить в JSON', command=self.save_to_json).grid(row=0, column=1)
        ttk.Button(button_frame, text='Загрузить из JSON', command=self.load_from_json).grid(row=0, column=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages = self.pages_entry.get()

        # Проверка
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        self.books.append({
            'title': title,
            'author': author,
            'genre': genre,
            'pages': int(pages)
        })

        self.update_treeview()
        self.update_genre_filter()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_treeview(self, filtered_books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = filtered_books if filtered_books is not None else self.books
        for book in data:
            self.tree.insert('', tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

    def update_genre_filter(self):
        genres = list(set(book['genre'] for book in self.books))
        self.genre_filter['values'] = ['Все'] + genres
        self.genre_filter.set('Все')

    def apply_filter(self):
        genre = self.genre_filter.get()
        pages_str = self.pages_filter_var.get()

        filtered = self.books
        if genre != 'Все':
            filtered = [b for b in filtered if b['genre'] == genre]
        if pages_str.isdigit():
            filtered = [b for b in filtered if b['pages'] > int(pages_str)]

        self.update_treeview(filtered)

    def reset_filter(self):
        self.genre_filter.set('Все')
        self.pages_filter_var.set('')
        self.update_treeview()

    def save_to_json(self):
        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books.json")

    def load_from_json(self):
        try:
            with open('books.json', 'r', encoding='utf-8') as f:
                self.books = json.load(f)
            self.update_treeview()
            self.update_genre_filter()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл books.json не найден")


if __name__ == '__main__':
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()