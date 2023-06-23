import shutil, os

from customtkinter import *

from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import *
import qrcode

from settings import THEME
from modules.gui.tool_tip import ToolTip
from modules.gui.custom_button import Button
import modules.main_app as main_app
from settings import SETTINGS


DEFAULT = {
    "back_color": (255, 255, 255),
    "fill_color": (0, 0, 0),
    "module_type": None,
    "gradient": None,
    "image": None
}

QR_SETTINGS = DEFAULT.copy()


class ChooseModule(CTk):
    def __init__(self, app_size, preview_size, title, qrcode_image):
        super().__init__()        
        
        self.MODULES = {
            "square": SquareModuleDrawer(),
            "rounded": RoundedModuleDrawer(),
            "circle": CircleModuleDrawer(),
            "vertical": VerticalBarsDrawer(),
            "horizontal": HorizontalBarsDrawer(),
            "gapped": GappedSquareModuleDrawer()
        }

        self.QRCODE_IMAGE = qrcode_image
        self.QRCODE = self.QRCODE_IMAGE.QRCODE

        self.WIDTH, self.HEIGHT = app_size
        self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT = preview_size
        self.TITLE = title
        self.configure_app()
        self.preview_modules()

        

    # Метод з модулями
    def preview_modules(self):
        self.SQUARE_MODULE = self.create_preview(preview_type = "square")
        ToolTip(self.SQUARE_MODULE, "Зробити модулі квадратними")
        self.SQUARE_MODULE.place(x = 15, y = 20)

        self.ROUND_MODULE = self.create_preview(preview_type = "rounded")
        ToolTip(self.ROUND_MODULE, "Зробити модулі скругленними")
        self.ROUND_MODULE.place(x = 215, y = 20)

        self.CIRCLE_MODULE = self.create_preview(preview_type = "circle")
        ToolTip(self.CIRCLE_MODULE, "Зробити модулі круглими")
        self.CIRCLE_MODULE.place(x = 415, y = 20)

        self.VERTICAL_MODULE = self.create_preview(preview_type = "vertical")
        ToolTip(self.VERTICAL_MODULE, "Зробити модулі вертикальними")
        self.VERTICAL_MODULE.place(x = 15, y = 220)

        self.HORIZONTAL_MODULE = self.create_preview(preview_type = "horizontal")
        ToolTip(self.HORIZONTAL_MODULE, "Зробити модулі горизонтальними")
        self.HORIZONTAL_MODULE.place(x = 215, y = 220)

        self.GAPPED_MODULE = self.create_preview(preview_type = "gapped")
        ToolTip(self.GAPPED_MODULE, "Зробити модулі з зазорами")
        self.GAPPED_MODULE.place(x = 415, y = 220)
        

    def create_preview(self, preview_type):
        pil_image = Image.open(
            fp = os.path.abspath(f"resources/images/previews/{preview_type}.png")
        ).resize((self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT))
        
        pil_image = ImageTk.PhotoImage(
            image = pil_image,
            master = self
        )

        return Button(
            master = self,
            width = self.PREVIEW_WIDTH,
            height = self.PREVIEW_HEIGHT,
            image = pil_image,
            fg_color = THEME["CTkButton"]["fg_color"],
            hover_color = THEME["CTkButton"]["hover_color"], 
            border_color = THEME["CTkButton"]["border_color"],
            border_width = 1,
            command = (self.apply_to_qrcode, (preview_type,))
        )
    
    def apply_to_qrcode(self, preview_type):
        global QR_SETTINGS
        
        self.QRCODE_IMAGE.IMAGE = self.QRCODE.make_image(
            fill_color = QR_SETTINGS["fill_color"],
            back_color = QR_SETTINGS["back_color"],
            image_factory = StyledPilImage,
            module_drawer = self.MODULES[f"{preview_type}"]
        )
        self.QRCODE_IMAGE.IMAGE.save(self.QRCODE_IMAGE.QRCODE_IMAGE_PATH)
        self.QRCODE_IMAGE._handle()
        self.destroy()
        
    # Метод налаштування вікна
    def configure_app(self):  
        self.title(self.TITLE)
        self.center_app()
        self.iconbitmap("resources/images/app.ico")
        self.resizable(False, False)
        self.configure(fg_color = THEME["CTk"]["fg_color"])

    # Функція розміщювання вікна додатку у центрі вікна
    def center_app(self) -> None:
        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}')









class QRCodeImage(CTkLabel):
    def __init__(self, master, width, height):        
        
        self.WIDTH = width
        self.HEIGHT = height

        self.START_IMAGE_PATH = os.path.abspath("resources/images/default.png")
        

        self.QRCODE = None
        self.QRCODES = []
        self.QRCODE_IMAGE_PATH = os.path.abspath("resources/qrcode.png")
        self.PROFILE_NAME = ""

        self.VERSION = 1
        self.CORRECTION = qrcode.ERROR_CORRECT_H
        
        self.CORRECTIONS = {
            "L": qrcode.ERROR_CORRECT_L,
            "M": qrcode.ERROR_CORRECT_M,
            "Q": qrcode.ERROR_CORRECT_Q,
            "H": qrcode.ERROR_CORRECT_H
        }

        self.CTK_IMAGE = CTkImage(Image.open(self.START_IMAGE_PATH), size = (width, height))
        super().__init__(master = master, width = width, height = height, text = "", image = self.CTK_IMAGE)

    def generate(self) -> str:
        global QR_SETTINGS

        self.QRCODE = qrcode.QRCode(version = self.VERSION, border = 1, error_correction = self.CORRECTION)

        self.DATA = main_app.app.DATA_ENTRY.get()
        self.QRCODE.add_data(data = self.DATA)
        self.QRCODE.make(fit = True)
        
        self.IMAGE = self.QRCODE.make_image()
        self.IMAGE.save(self.QRCODE_IMAGE_PATH)
        QR_SETTINGS = DEFAULT.copy()
        self._handle()
            
    
    def view_qrcode_history(self, profile_name=None):
        qrcodes = [os.path.join(os.path.abspath(f"resources/profiles/{self.PROFILE_NAME}/qrcodes"), rel_qrcode_path) for rel_qrcode_path in self.QRCODES]
        for qrcode_path in qrcodes:
            main_app.app.add_qrcode_to_history(qrcode_path)
        
    def set_profile_name(self, profile_name):
        self.PROFILE_NAME = profile_name

    def set_qrcode_path(self):
        self.QRCODES = os.listdir(os.path.abspath(f"resources/profiles/{self.PROFILE_NAME}/qrcodes"))
        self.INUSERPROFILE_QRCODE_PATH = os.path.abspath(f"resources/profiles/{self.PROFILE_NAME}/qrcodes/{len(self.QRCODES) + 1}.png")


    def _handle(self):
        self.CTK_IMAGE = CTkImage(Image.open(self.QRCODE_IMAGE_PATH), size = (self.WIDTH, self.HEIGHT))

        self.place_forget()
        self.configure(image = self.CTK_IMAGE)
        self.place(x = 0, y = 0)





    def change_bg_color(self):
        if self.QRCODE:
            global QR_SETTINGS
            
            QR_SETTINGS["back_color"] = colorchooser.askcolor()[0]
            
            if QR_SETTINGS["back_color"]:
                self.IMAGE = self.QRCODE.make_image(
                    back_color = QR_SETTINGS["back_color"],
                    fill_color = QR_SETTINGS["fill_color"]
                )
                self.IMAGE.save(self.QRCODE_IMAGE_PATH)
                self._handle()
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")
    

    def change_fg_color(self):
        if self.QRCODE:
            global QR_SETTINGS
            
            QR_SETTINGS["fill_color"] = colorchooser.askcolor()[0]
            
            if QR_SETTINGS["fill_color"]:
                self.IMAGE = self.QRCODE.make_image(
                    back_color = QR_SETTINGS["back_color"],
                    fill_color = QR_SETTINGS["fill_color"]
                )
                self.IMAGE.save(self.QRCODE_IMAGE_PATH)
                self._handle()
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")
        
    def set_module_type(self):
        if self.QRCODE:
            global QR_SETTINGS
            
            choose_module_app = ChooseModule(
                app_size = (600, 400),
                preview_size = (150, 150),
                title = "Модулі",
                qrcode_image = self
            )
            choose_module_app.mainloop()
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")
        

    def gradient(self):
        if self.QRCODE:
            global QR_SETTINGS
            
            QR_SETTINGS["gradient"] = RadialGradiantColorMask(
                back_color = QR_SETTINGS["back_color"],
                center_color = (255, 255, 255),
                edge_color = QR_SETTINGS["fill_color"]
            )
            self.IMAGE = self.QRCODE.make_image(
                image_factory = StyledPilImage,
                color_mask = QR_SETTINGS["gradient"]
            )
            self.IMAGE.save(self.QRCODE_IMAGE_PATH)
            self._handle()
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")


    def add_image(self):
        if self.QRCODE:
            global QR_SETTINGS

            try:
                with filedialog.askopenfile(defaultextension=".png") as f:
                    QR_SETTINGS["image"] = f.name
                    qrcode_with_img = Image.open(self.QRCODE_IMAGE_PATH).convert("RGBA")

                    insert_image = Image.open(QR_SETTINGS["image"]).convert("RGBA")
            
                    insert_image = insert_image.resize((96, 96))
                    insert_image_width, insert_image_height = insert_image.size

                    x = qrcode_with_img.width  // 2 - insert_image_width // 2
                    y = qrcode_with_img.height // 2 - insert_image_height // 2

                    qrcode_with_img.paste(insert_image, (x, y), mask=insert_image)
                    qrcode_with_img.save(self.QRCODE_IMAGE_PATH)
                    
                    self._handle()
                    
            except TypeError:
                pass
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")


    def on_version_change(self, version):
        self.VERSION = int(version)
        self.VERSION_LABEL.configure(text = str(self.VERSION))
        self.QRCODE = qrcode.QRCode(version = self.VERSION, border = 1, error_correction = self.CORRECTION)
        self.QRCODE.add_data(data = self.DATA)
        self.QRCODE.make(fit = True)
    

    def on_correction_select(self, correction):
        self.CORRECTION = self.CORRECTIONS[correction.split()[0]]
        self.QRCODE = qrcode.QRCode(version = self.VERSION, border = 1, error_correction = self.CORRECTION)
        self.QRCODE.add_data(data = self.DATA)
        self.QRCODE.make(fit = True)


    def on_settings_window_destroy(self):
        global QR_SETTINGS
        
        self.SETTINGS_WINDOW.destroy()
        self.IMAGE = self.QRCODE.make_image()
        self.IMAGE.save(self.QRCODE_IMAGE_PATH)
        QR_SETTINGS = DEFAULT.copy()
        self._handle()

    

    def qr_settings(self):
        if self.QRCODE:
            global QR_SETTINGS
            
            self.SETTINGS_WINDOW = CTk()
            self.SETTINGS_WINDOW.protocol("WM_DELETE_WINDOW", self.on_settings_window_destroy)

            self.SETTINGS_WINDOW.configure(fg_color = THEME["CTk"]["fg_color"])
            self.SETTINGS_WINDOW.title("Налаштування QR-Код'у")
            self.SETTINGS_WINDOW.iconbitmap(os.path.abspath("resources/images/app.ico"))
            self.SETTINGS_WINDOW.resizable(width = False, height = False)

            center_x = self.winfo_screenwidth() // 2 - 175
            center_y = self.winfo_screenheight() // 2 - 75
            self.SETTINGS_WINDOW.geometry(f'350x150+{center_x}+{center_y}')


            self.VERSION_VALUE_LABEL = CTkLabel(
                master = self.SETTINGS_WINDOW,
                width = 20,
                height = 20,
                text = "Вкажіть версію QR-коду"
            )
            self.VERSION_VALUE_LABEL.place(x = 10, y = 10)


            self.VERSION_LABEL = CTkLabel(
                master = self.SETTINGS_WINDOW,
                width = 20,
                height = 20,
                text = '1'
            )
            self.VERSION_LABEL.place(x = 320, y = 30)

            self.QRCODE_VERSION_SCROLL = CTkSlider(
                master = self.SETTINGS_WINDOW,
                width = 300,
                height = 20,
                from_ = 1,
                to = 40,
                command = self.on_version_change
            )
            self.QRCODE_VERSION_SCROLL.place(x = 10, y = 30)

            
            self.ERROR_CORRECTION_LABEL = CTkLabel(
                master = self.SETTINGS_WINDOW,
                width = 20,
                height = 20,
                text = 'Вкажіть версію корегування'
            )
            self.ERROR_CORRECTION_LABEL.place(x = 90, y = 65)
            
            self.ERROR_CORRECTION_OPTION_MENU = CTkOptionMenu(
                master = self.SETTINGS_WINDOW,
                width = 75,
                height = 25,
                command = self.on_correction_select,
                values = ["L (Слабкий, 7%)", "M (Низький, 15%)", "Q (Середній, 25%)", "H (Високий, 30%)"]
            )
            self.ERROR_CORRECTION_OPTION_MENU.place(x = 115, y = 90)


            self.SETTINGS_WINDOW.mainloop()
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")




    def save_image(self):
        if self.QRCODE:
            # try:
            image_path = filedialog.asksaveasfilename(
                defaultextension = ".png",
                filetypes = SETTINGS["supported_import_types"]
            )
            shutil.copy2(
                src = self.QRCODE_IMAGE_PATH,
                dst = image_path
            )
            self.set_qrcode_path()
            shutil.copy2(
                src = self.QRCODE_IMAGE_PATH,
                dst = self.INUSERPROFILE_QRCODE_PATH
            )
            self.SAVE_PATH = image_path
            main_app.app.add_qrcode_to_history(qrcode_path=self.INUSERPROFILE_QRCODE_PATH)
                
        else:
            messagebox.showwarning("Увага!", "Будь ласка, створіть спочатку QR-Code!")