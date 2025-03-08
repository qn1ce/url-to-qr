import re
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
import qrcode


# Создание + централизация окна
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f'{width}x{height}+{x}+{y}')

windows = tk.Tk()
windows.title('from URL to QR')
windows.geometry('500x700')
center_window(windows)

# создание поле ввода + подсказка
ent1 = tk.Entry(windows)
ent1.place(x=80, y=50, width=350)

def on_entry_click(event):
    if ent1.get() == 'URL':
        ent1.delete(0,'end')
        ent1.config(fg='black')

def on_focusout(event):
    if ent1.get() == '':
        ent1.insert(0,'URL')
        ent1.config(fg='gray')

ent1.insert(0,'URL')
ent1.config(fg='gray')

ent1.bind('<FocusIn>', on_entry_click)
ent1.bind('<FocusOut>', on_focusout)


# проверка ссылки + кнопка 
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            resul_label.config(text='Ссылка работает')
        else:
            resul_label.config(text="Ссылка не работает")
    except requests.exceptions.RequestException as e:
        resul_label.config(text='Ссылка не работает')

def btn1Click():
    url = ent1.get()
    if not url:
        resul_label.config(text="Пожалуйста, введите ссылку")
        return

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # Протокол
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Домен
        r'localhost|'  # Локальный хост
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP-адрес
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'  # Порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if re.match(regex,url):
        resul_label.config(text='url correct')
        threading.Thread(target=check_url,args=(url,)).start()
    else:
        resul_label.config(text='uncorrect url')


btn1 = tk.Button(windows, text='Check url', command=btn1Click, width=20,height=2)
btn1.place(x=175,y=130)

resul_label = tk.Label(windows,text='', fg='red')
resul_label.place(x=220,y= 90)

def btn2Click():
    url = ent1.get()
    if not url:
        resul_label.config(text="Пожалуйста, введите ссылку для QR-кода")
        return
    
    qr = qrcode.QRCode(version=1, box_size=10,border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill = 'black', back_color = 'white')

    img.save('qrcode.png')

    img = Image.open('qrcode.png')
    img = img.resize((200,200))
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image = img_tk)
    qr_label.image = img_tk



btn2 = tk.Button(windows, text='Generate', command=btn2Click, width=20,height=2)
btn2.place(x=175,y=180)
qr_label = tk.Label(windows)
qr_label.place(x = 150,y = 300)

windows.mainloop()
