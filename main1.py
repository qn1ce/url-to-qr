import re
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
import qrcode

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Проверка ссылки и генерация QR-кода')
        self.root.geometry('500x700')
        self.center_window()

        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.ent1 = tk.Entry(self.root)
        self.ent1.place(x=80, y=50, width=350)
        self.ent1.insert(0, 'Введите URL')
        self.ent1.config(fg='gray')

        self.btn1 = tk.Button(self.root, text='Проверить', command=self.btn1Click, width=20, height=2)
        self.btn1.place(x=175, y=130)

        self.resul_label = tk.Label(self.root, text='', fg='red')
        self.resul_label.place(x=220, y=90)

        self.btn2 = tk.Button(self.root, text='Сгенерировать QR-код', command=self.btn2Click, width=20, height=2)
        self.btn2.place(x=175, y=180)

        self.qr_label = tk.Label(self.root)
        self.qr_label.place(x=150, y=250)

    def check_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        try:
            response = requests.head(url, headers=headers, allow_redirects=True)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def btn1Click(self):
        url = self.ent1.get()  # Получаем текст из поля ввода
        if not url:
            self.resul_label.config(text="Пожалуйста, введите ссылку")
            return

        # Регулярное выражение для проверки формата URL
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # Протокол
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Домен
            r'localhost|'  # Локальный хост
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP-адрес
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
            r'(?::\d+)?'  # Порт
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if re.match(regex, url):
            self.resul_label.config(text='URL корректен')
            threading.Thread(target=self.check_url, args=(url,)).start()
        else:
            self.resul_label.config(text='Некорректный URL')

    def btn2Click(self):
        url = self.ent1.get()
        if not url:
            self.resul_label.config(text="Пожалуйста, введите ссылку для QR-кода")
            return
        
        # Проверка ссылки
        if not self.check_url(url):
            self.resul_label.config(text='Ты еблан')  # Если ссылка не работает
            return

        # Генерация QR-кода
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Сохранение QR-кода во временный файл
        img.save('qrcode1.png')

        # Открытие и отображение QR-кода
        img = Image.open('qrcode.png')
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        self.qr_label.config(image=img_tk)
        self.qr_label.image = img_tk  # Сохраняем ссылку на изображение

if __name__ == '__main__':
    windows = tk.Tk()
    app = QRCodeApp(windows)
    windows.mainloop()