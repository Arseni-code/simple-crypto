import dotenv
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def decryptor(encrypted_message, key):
    decrypted_message = ""
    for i, char in enumerate(encrypted_message):
        if char.isalpha():
            if char.isupper():
                decrypted_message += chr((ord(char) - ord(key[i % len(key)]) - 65) % 26 + 65)
            else:
                decrypted_message += chr((ord(char) - ord(key[i % len(key)]) - 97) % 26 + 97)
        else:
            decrypted_message += char
    return decrypted_message

def decrypt(crypted_message):
    public_key = "'=9=pR}+78'KCuy+SBT#Q4,]!x46,6B*]f6,%`WYxE^@&8g!Fv"
    env_values = dotenv.dotenv_values(".env")
    crypted_secret_key = env_values.get('KEY')

    if crypted_secret_key is None:
        print("Ошибка: ключ не найден в .env файле.")
        return None

    secret_key = decryptor(crypted_secret_key, public_key)
    crypted_message = decryptor(crypted_message, public_key)
    crypted_message = decryptor(crypted_message, secret_key)
    crypted_message = crypted_message[0:-97:1]
    decrypted_message = decryptor(crypted_message, secret_key)
    
    return decrypted_message  # Не забудьте вернуть расшифрованное сообщение

class Cryptor(Gtk.Window):
    def __init__(self):  # Исправлено init на __init__
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
        self.submit_button = Gtk.Button(label="Дешифровать")
        self.submit_button.connect("clicked", self.on_submit)
        vbox.pack_start(self.submit_button, False, False, 0)

    def on_submit(self, widget):
        input_text = self.input_field.get_text()  # Получаем текст из поля
        decrypted_text = decrypt(input_text)  # Дешифруем текст
        if decrypted_text is not None:

            self.input_field.set_text(decrypted_text)  # Устанавливаем результат в поле ввода
            

# Запуск приложения
win = Cryptor()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
