from datetime import datetime
import locale
import os, shutil

from customtkinter import *
from PIL import Image 
import pytz

from settings import *
from modules.gui.select_theme import SelectTheme
from modules.gui.qrcode_image import QRCodeImage
from modules.gui.tool_tip import ToolTip
from modules.utils.json_io import *

locale.setlocale(locale.LC_TIME, 'uk_UA')
SETTINGS = json_io.read_json(
    json_path = os.path.abspath('settings.json')
)


class MainApp(CTk):
    def __init__(self):
        # Розміри вікна
        self.WIDTH = 500
        self.HEIGHT = self.WIDTH + 155
        
        # Відступи
        self.TAB_VIEW_PADX = 12
        self.TAB_VIEW_PADY = 23


        # Розміри кнопки GENERATE_BUTTON
        self.GENERATE_BUTTON_SIZE = (75, 50) 
        
        self.QRCODE_IMAGE_SIZE = (self.WIDTH - self.TAB_VIEW_PADX, self.WIDTH - self.TAB_VIEW_PADY)

        self.BUTTON_PADX = 5
        self.BUTTON_WIDTH = self.QRCODE_IMAGE_SIZE[0] // 7 - self.BUTTON_PADX + 1

        self.DATA_ENTRY_SIZE = (
            self.WIDTH - self.GENERATE_BUTTON_SIZE[0] - 15,
            self.GENERATE_BUTTON_SIZE[1] - 10
        )

        self.HISTORY_LEN = 0

        # Викликаємо метод який змінює основні параметри вікна на потрібні
        self.configure_app()

        # Створюємо TAB_VIEW зверху додатку
        self.TAB_VIEW = CTkTabview(
            master = self,
            width = self.WIDTH,
            height = self.HEIGHT,
            fg_color = THEME["CTk"]["fg_color"],
            segmented_button_fg_color = THEME["CTk"]["fg_color"],
            segmented_button_unselected_color = THEME["CTkButton"]["fg_color"],
            segmented_button_unselected_hover_color = THEME["CTkButton"]["hover_color"],
            segmented_button_selected_color = THEME["CTkButton"]["hover_color"],
            segmented_button_selected_hover_color = THEME["CTkButton"]["hover_color"]
        )

        self.TAB_VIEW.place(x = 0, y = 0)
        
        self.generate_frame()
        self.profile_frame()
    
    # Метод фрейму у якому генерується QR-КОД
    def generate_frame(self):
        self.GENERATE_FRAME = self.TAB_VIEW.add("Генерація")

        
        self.QRCODE_IMAGE = QRCodeImage(
            master = self.GENERATE_FRAME,
            width = self.QRCODE_IMAGE_SIZE[0],
            height = self.QRCODE_IMAGE_SIZE[1]
        )
        self.QRCODE_IMAGE.place(x = 0, y = 0)

        
        
        self.CHANGE_BG_COLOR_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/change_bg.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.change_bg_color
        )
        ToolTip(self.CHANGE_BG_COLOR_BUTTON, "Зміна кольору фону")
        self.CHANGE_BG_COLOR_BUTTON.place(x = 0, y = self.QRCODE_IMAGE._current_height + 10)

        self.CHANGE_FG_COLOR_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/change_fg.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.change_fg_color
        )
        ToolTip(self.CHANGE_FG_COLOR_BUTTON, "Зміна кольору блоків")
        
        self.CHANGE_FG_COLOR_BUTTON.place(x = self.BUTTON_WIDTH * 1 + self.BUTTON_PADX, y = self.QRCODE_IMAGE._current_height + 10)
         
        self.CHOOSE_MODULE_DRAWER_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/set_module.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.set_module_type
        )
        ToolTip(self.CHOOSE_MODULE_DRAWER_BUTTON, "Змінити тип відображення модулів")
        self.CHOOSE_MODULE_DRAWER_BUTTON.place(x = self.BUTTON_WIDTH * 2 + self.BUTTON_PADX * 2, y = self.QRCODE_IMAGE._current_height + 10)
        
        self.GRADIENT_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/gradient.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.gradient
        )

        ToolTip(self.GRADIENT_BUTTON, "Задіяти градієнт")
        self.GRADIENT_BUTTON.place(x = self.BUTTON_WIDTH * 3 + self.BUTTON_PADX * 3, y = self.QRCODE_IMAGE._current_height + 10)

        
        self.ADD_IMAGE_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/add_image.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.add_image
        )
        ToolTip(self.ADD_IMAGE_BUTTON, "Додати зображення")
        self.ADD_IMAGE_BUTTON.place(x = self.BUTTON_WIDTH * 4 + self.BUTTON_PADX * 4, y = self.QRCODE_IMAGE._current_height + 10)
        
        self.SETTINGS_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/settings.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.qr_settings
        )
        ToolTip(self.SETTINGS_BUTTON, "Налаштування")
        self.SETTINGS_BUTTON.place(x = self.BUTTON_WIDTH * 5 + self.BUTTON_PADX * 5, y = self.QRCODE_IMAGE._current_height + 10)


        self.SAVE_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = 50,
            border_width = 1,
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/save.png")), size = (35, 35)),
            command = self.QRCODE_IMAGE.save_image
        )
        ToolTip(self.SAVE_BUTTON, "Зберегти зображення")
        self.SAVE_BUTTON.place(x = self.BUTTON_WIDTH * 6 + self.BUTTON_PADX * 6, y = self.QRCODE_IMAGE._current_height + 10)

        
        self.DATA_ENTRY = CTkEntry(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH * 6 + self.BUTTON_PADX * 3,
            height = self.DATA_ENTRY_SIZE[1],
            fg_color = THEME["CTkEntry"]["fg_color"],
            border_color = THEME["CTkEntry"]["border_color"],
            border_width = 1
        )
        self.DATA_ENTRY.place(x = 0, y = self.HEIGHT - self.DATA_ENTRY_SIZE[1] * 2 - 15)


        self.GENERATE_BUTTON = CTkButton(
            master = self.GENERATE_FRAME,
            width = self.BUTTON_WIDTH,
            height = self.GENERATE_BUTTON_SIZE[1],
            text = '',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            border_width = 1,
            image = CTkImage(Image.open(os.path.abspath("resources/images/buttons/generate.png")), size = (40, 40)),
            command = self.QRCODE_IMAGE.generate
        )
        ToolTip(self.GENERATE_BUTTON, "Згенерувати QRCode")
        self.GENERATE_BUTTON.place(x = self.BUTTON_WIDTH * 6 + self.BUTTON_PADX * 6, y = self.HEIGHT - self.DATA_ENTRY_SIZE[1] * 2 - 20)
        

    def profile_frame(self):
        self.PROFILE_FRAME = self.TAB_VIEW.add("Профіль")

        self.ADD_AVATAR_BUTTON = CTkButton(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 100,
            text = '+',
            fg_color = THEME["CTkButton"]["fg_color"],
            border_color = THEME["CTkButton"]["border_color"],
            hover_color = THEME["CTkButton"]["hover_color"],
            border_width = 1,
            font = CTkFont(family = None, size = 22),
            command = self.add_avatar
        )
        self.ADD_AVATAR_BUTTON.place(x = 10, y = 10)
        
        
        self.USERNAME_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 15)
        )
        self.USERNAME_LABEL.place(x = 120, y = 20)

        self.EMAIL_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 13)
        )
        self.EMAIL_LABEL.place(x = 120, y = 50)
        
        self.DATE_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 15)
        )
        self.DATE_LABEL.place(x = 120, y = 80)
     

        self.SELECT_THEME = SelectTheme(
            master = self.PROFILE_FRAME,
            fg_color = THEME["CTkOptionMenu"]["fg_color"],
            button_color = THEME["CTkOptionMenu"]["button_color"],
            button_hover_color = THEME["CTkOptionMenu"]["button_hover_color"],
            width = 100,
            height = 25
        )
        self.SELECT_THEME.place(x = 10, y = 130)


        self.HISTORY_FRAME = CTkScrollableFrame(
            master = self.PROFILE_FRAME,
            width = self.WIDTH - 50,    
            height = 400,
            fg_color = THEME["CTkFrame"]["fg_color"],
            border_color = THEME["CTkFrame"]["border_color"]
        )
        
        self.HISTORY_FRAME.place(x = 8, y = 190)

        
    def add_qrcode_to_history(self, qrcode_path):
        qrcode_info_frame = CTkFrame(
            master = self.HISTORY_FRAME,
            width = self.WIDTH - 70,
            height = 120,
            border_width = 1,
            fg_color = THEME["CTkFrame"]["fg_color"],
            border_color = THEME["CTkFrame"]["border_color"]
        )
        
        qrcode_pil_img = Image.open(qrcode_path)
        CTkLabel(
            master = qrcode_info_frame,
            text = '',
            image = CTkImage(qrcode_pil_img, size=(110, 110))
        ).place(x = 5, y = 5)
        
        size = qrcode_pil_img.width, qrcode_pil_img.height
        current_time = datetime.fromtimestamp(os.path.getctime(qrcode_path))
        ukraine_timezone = pytz.timezone('Europe/Kiev')
        ukraine_time = current_time.astimezone(ukraine_timezone)
        date = ukraine_time.strftime('%Y-%m-%d %H:%M:%S')
        filetype = qrcode_pil_img.format
        
        self.FILE_NAME = os.path.basename(qrcode_path)
        self.QRCODE_IMAGE_NAME_LABEL = CTkLabel(
            master = qrcode_info_frame,
            width = 100,
            height = 10,
            text = f"Назва QR-коду: {self.FILE_NAME}")
        
        self.QRCODE_IMAGE_NAME_LABEL.place(x = 120, y = 20)

        self.IMAGE_SIZE_LABEL = CTkLabel(
            master = qrcode_info_frame,
            width = 10,
            height = 10,
            text = f"Розмір QR-коду: {size}"
        )
        self.IMAGE_SIZE_LABEL.place(x = 120, y = 40)
        
        self.IMAGE_DATE_LABEL = CTkLabel(
            master = qrcode_info_frame,
            width = 10,
            height = 10,
            text = f"Дата створення QR-коду: {date}"
        )
        self.IMAGE_DATE_LABEL.place(x = 120, y = 60)
        
        self.IMAGE_FORMAT_LABEL = CTkLabel(
            master = qrcode_info_frame,
            width = 10,
            height = 10,
            text = f"Формат зображення QR-коду: {filetype}"
        )
        self.IMAGE_FORMAT_LABEL.place(x = 120, y = 80)

        qrcode_info_frame.grid(row = self.HISTORY_LEN, column = 0, padx = 10, pady = 10)
        self.HISTORY_LEN += 1
        
       


    def set_profile_data(self, creation_date, username, email):
        self.DATE_LABEL.configure(text = f"Дата створення вашого аккаунту: {creation_date}")
        self.USERNAME_LABEL.configure(text = f"Ім'я користувача: {username}")
        self.EMAIL_LABEL.configure(text = f"Пошта користувача: {email}")

    
    # def show_avatar(self, profile_name):
    
    
    
    def add_avatar(self):
        try:
            with filedialog.askopenfile(mode = 'r', filetypes = SETTINGS["supported_import_types"]) as image:
                image_path = image.name
                dst_path = os.path.abspath(f"resources/profiles/{self.QRCODE_IMAGE.PROFILE_NAME}/avatar.png")
                shutil.copy2(image_path, dst_path)
        
                self.AVATAR_LABLE = CTkLabel(
                    master = self.PROFILE_FRAME,
                    width = 100,
                    height = 100,
                    text = '',
                    image = CTkImage(dark_image = Image.open(dst_path), size = (100, 100))
                )
                self.AVATAR_LABLE.place(x = 10, y = 10)
        
        except FileNotFoundError: pass
        
        


        
    # Метод у якому задаються параметри головного вікна
    def configure_app(self) -> None:
        
        # Викликаємо метод конструктор батьківського класу
        super().__init__()
        
        # Задаємо колір фону вікна
        self.configure(fg_color = THEME["CTk"]["fg_color"])
        
        # Змінюємо розмір вікна та центруємо його
        self.center_app()
        
        # Забороняємо змінювати розмір вікна
        self.resizable(False, False)
        # Встановлюємо іконку вікна
        self.iconbitmap(os.path.abspath("resources/images/app.ico"))

        # Встанвлюємо назву вікна
        self.title("QR-Code Key Generator")
    
    # Функція розміщювання вікна додатку у центрі вікна
    def center_app(self) -> None:
        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}')

    def destroy(self):
        super().destroy()
        exit()


app = MainApp()