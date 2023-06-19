import os, shutil

from customtkinter import *
from PIL import Image 

from settings import *
from modules.gui.select_theme import SelectTheme
from modules.gui.qrcode_image import QRCodeImage
from modules.gui.tool_tip import ToolTip
from modules.utils.json_io import *

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
            height = self.QRCODE_IMAGE_SIZE[1],
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
            command = self.add_avatar
        )
        self.ADD_AVATAR_BUTTON.place(x = 10, y = 10)
        
        self.USERNAME_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 20)
        )
        self.USERNAME_LABEL.place(x = 110, y = 15)

        self.EMAIL_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 20)
        )
        self.EMAIL_LABEL.place(x = 110, y = 45)
        
        self.DATE_LABEL = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 20,
            font = CTkFont(family = None, size = 20)
        )
        self.DATE_LABEL.place(x = 110, y = 75)
     

        self.SELECT_THEME = SelectTheme(
            master = self.PROFILE_FRAME,
            fg_color = THEME["CTkOptionMenu"]["fg_color"],
            button_color = THEME["CTkOptionMenu"]["button_color"],
            button_hover_color = THEME["CTkOptionMenu"]["button_hover_color"],
            width = 100,
            height = 25
        )
        self.SELECT_THEME.place(x = 10, y = 130)

    def set_profile_data(self, creation_date, username, email):
        self.DATE_LABEL.configure(text = f"Дата створення вашого аккаунту: {creation_date}")
        self.USERNAME_LABEL.configure(text = f"Ім'я користувача: {username}")
        self.EMAIL_LABEL.configure(text = f"Пошта користувача: {email}")

    def add_avatar(self):
        try:
            with filedialog.askopenfile(mode = 'r',
                                        filetypes = SETTINGS["supported_import_types"]
                                        ) as image:

                image_path = image.name
                images_path = os.path.abspath("resources/images/avatars/avatar.png")
                shutil.copy2(image_path, images_path)
        except FileNotFoundError: pass
        
        self.AVATAR_LABLE = CTkLabel(
            master = self.PROFILE_FRAME,
            width = 100,
            height = 100,
            text = '',
            image = CTkImage(dark_image = Image.open("resources/images/avatars/avatar.png"), size = (100, 100))
        )
        self.AVATAR_LABLE.place(x = 10, y = 10)
        
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