import dotenv
import secrets
import string
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
def encryptor(message, key):
    encrypted_message = ""
    for i, char in enumerate(message):
        if char.isalpha():
            if char.isupper():
                if 'A' <= char <= 'Z':
                    encrypted_message += chr((ord(char) + ord(key[i % len(key)]) - 65) % 26 + 65)
                else:
                    encrypted_message += chr((ord(char) + ord(key[i % len(key)]) - 1040) % 32 + 1040)
            else:
                if 'a' <= char <= 'z':
                    encrypted_message += chr((ord(char) + ord(key[i % len(key)]) - 97) % 26 + 97)
                else:
                    encrypted_message += chr((ord(char) + ord(key[i % len(key)]) - 1072) % 32 + 1072)
        else:
            encrypted_message += char
    return encrypted_message

public_key="'=9=pR}+78'KCuy+SBT#Q4,]!x46,6B*]f6,%`WYxE^@&8g!Fv"
def encrypt(message):
    #Генерация секретного ключа
    alphabet = string.ascii_letters + string.digits+string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for i in range(20)) 
    crypted_secret_key=encryptor(secret_key,public_key)
    dotenv.set_key(dotenv_path=".env",key_to_set="KEY",value_to_set=crypted_secret_key)
    encrypted_message = encryptor(message, secret_key)
    encrypted_message=encryptor((encrypted_message)+''.join(secrets.choice(alphabet) for i in range(97)),secret_key)
    encrypted_message=encryptor(encrypted_message,public_key)
    return encrypted_message
#print("Encrypted message:",encrypted_message)


class Cryptor(Gtk.Window):
    def __init__(self):
        super().__init__(title="Интерфейс на PyGTK")
        self.set_default_size(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.set_resizable(True)

        # VBox для вертикального расположения элементов
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Создание голубого поля
        entry_frame = Gtk.Frame()
        entry_frame.set_border_width(0)  # Убираем границы
        entry_frame.set_property("shadow-type", Gtk.ShadowType.NONE)  # Убираем тени

        # Установка голубого фона
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Поле ввода текста
        self.input_field = Gtk.Entry()
        self.input_field.set_placeholder_text("Введите текст здесь")
        entry_box.pack_start(self.input_field, True, True, 0)

        entry_frame.add(entry_box)
        vbox.pack_start(entry_frame, True, False, 0)

        # Кнопка "Синяя кнопка"
        self.submit_button = Gtk.Button(label="Зашифровать")
        self.submit_button.connect("clicked", self.on_submit)
        vbox.pack_start(self.submit_button, False, False, 0)
        



    def on_submit(self, widget):
        input_text = self.input_field.get_text()  # Получаем текст из поля
        encrypted_text = encrypt(input_text)  # Шифруем текст
        self.input_field.set_text(encrypted_text)  # Устанавливаем результат в поле ввода
# Запуск приложения
win = Cryptor()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
