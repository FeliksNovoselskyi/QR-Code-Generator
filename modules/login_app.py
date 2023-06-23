from datetime import date
import sqlite3
import os

from customtkinter import *
from tkinter import messagebox
import validators

import modules.utils.json_io as json_io 
import modules.main_app as main_app



SETTINGS = json_io.read_json(
    json_path = os.path.abspath('settings.json')
)

THEME = json_io.read_json(
    os.path.abspath(SETTINGS["color_theme"])
)


class LoginApp(CTk):
    def __init__(self) -> None:
        
        # Розміри вікна
        self.WIDTH = 350
        self.HEIGHT = 425
        
        # Викликаємо метод який змінює основні параметри вікна на потрібні
        self.configure_app()
        
        # Панель з двома кнопками у якій користувач обирає, яку дію він хоче виконати (Вхід/Реєстрація)
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
        
        
        # Відстань між кнопками відносно вікна
        self.PADX = 40
        self.PADY = 7
        
        # Розміри кнопок для кожного з фреймів авторизації та реєстрації користувача
        self.BUTTON_WIDTH = 250
        self.BUTTON_HEIGHT = 50
        

        # Розміщення віджетів для фреймів авторизації та реєстрації користувача
        self.login_frame()
        self.register_frame()        

        #
        self.TAB_VIEW.grid(row = 0, column = 0, sticky = NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Шлях до БД користувачів
        self.USERS_DB_PATH = os.path.abspath("resources/users.db")
        
        # Якщо БД не існує, створюємо її
        if not os.path.exists(self.USERS_DB_PATH):
            open(self.USERS_DB_PATH, 'w').close()
        
        # Підключення до БД та створення курсору
        self.CONN = sqlite3.connect(self.USERS_DB_PATH)
        self.CUR = self.CONN.cursor()


    # Метод у якому задаються параметри вікна авторизації
    def configure_app(self) -> None:
        
        # Викликаємо метод конструктор батьківського класу
        super().__init__()
        
        # Задаємо колір фону вікна
        self.configure(fg_color = THEME["CTk"]["fg_color"])
        
        # Змінюємо розмір вікна та центруємо його
        self.center_app()
        
        # Забороняємо користувачу змінювати розмір вікна
        self.resizable(width = False, height = False)

        # Встановлюємо іконку вікна
        self.iconbitmap(os.path.abspath("resources/images/app.ico"))

        # Встанвлюємо назву вікна
        self.title("Авторизація до додатку")
        
    def center_app(self) -> None:
        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}')
    
    # Метод у якому створюються та розміщуються віджети для фрейму авторизації користувача
    def login_frame(self) -> None:
        signin_frame = self.TAB_VIEW.add("Вхід")
        signin_frame.configure(fg_color = THEME["CTk"]["fg_color"])
        
        self.L_EMAIL_ENTRY = CTkEntry(
            master = signin_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.L_EMAIL_ENTRY.insert(0, "Введіть електронну пошту")
        

        self.L_PASSWORD_ENTRY = CTkEntry(
            master = signin_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.L_PASSWORD_ENTRY.insert(0, "Введіть пароль")


        login_button = CTkButton(
            master = signin_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            text = "Увійти",
            command = self.sign_in,
            border_color = THEME["CTkButton"]["border_color"],
            fg_color = THEME["CTkButton"]["fg_color"],
        )
        
        signin_frame.grid_rowconfigure(0, weight=1)
        signin_frame.grid_rowconfigure(4, weight=1)
        signin_frame.grid_columnconfigure(0, weight=1)
        signin_frame.grid_columnconfigure(1, weight=1)
        signin_frame.grid_columnconfigure(2, weight=1)
        
        
        self.L_EMAIL_ENTRY.grid(row = 1, column = 1, padx = self.PADX, pady = self.PADY * 2)
        self.L_PASSWORD_ENTRY.grid(row = 2, column = 1, padx = self.PADX, pady = self.PADY)
        login_button.grid(row = 3, column = 1, padx = self.PADX, pady = self.PADY * 2)
    
    
    # Метод у якому створюються та розміщуються віджети для фрейму з регистрацією
    def register_frame(self) -> None:
        signup_frame = self.TAB_VIEW.add("Реєстрація")
        signup_frame.configure(fg_color = THEME["CTk"]["fg_color"])
        
        self.R_USERNAME_ENTRY = CTkEntry(
            master = signup_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.R_USERNAME_ENTRY.insert(0, "Введіть ім'я користувача")
        

        self.R_EMAIL_ENTRY = CTkEntry(
            master = signup_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.R_EMAIL_ENTRY.insert(0, "Введіть електронну пошту")


        self.R_PASSWORD_ENTRY = CTkEntry(
            master = signup_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.R_PASSWORD_ENTRY.insert(0, "Введіть пароль")


        self.R_CONFIRM_PASSWORD_ENTRY = CTkEntry(
            master = signup_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            border_color = THEME["CTkEntry"]["border_color"],
            fg_color = THEME["CTkEntry"]["fg_color"],
            corner_radius = 7,
            border_width = 1
        )
        self.R_CONFIRM_PASSWORD_ENTRY.insert(0, "Введіть пароль ще раз")

        
        register_button = CTkButton(
            master = signup_frame,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            text = "Зареєструватись",
            command = self.sign_up,
            border_color = THEME["CTkButton"]["border_color"],
            fg_color = THEME["CTkButton"]["fg_color"]
        )
        
        self.R_USERNAME_ENTRY.grid(row = 0, column = 0, padx = self.PADX, pady = self.PADY * 2)
        self.R_EMAIL_ENTRY.grid(row = 1, column = 0, padx = self.PADX, pady = self.PADY)
        self.R_PASSWORD_ENTRY.grid(row = 2, column = 0, padx = self.PADX, pady = self.PADY * 2)
        self.R_CONFIRM_PASSWORD_ENTRY.grid(row = 3, column = 0, pady = self.PADY)
        register_button.grid(row = 4, column = 0, padx = self.PADX, pady = self.PADY * 2, sticky = NSEW)


    # Метод який реєструє користувача в базі данних
    def sign_up(self) -> None:
        self.CUR.execute("""
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY,
        login TEXT,
        email TEXT,
        password TEXT,
        creationdate TEXT)
        """)
        
        incoming_login = self.R_USERNAME_ENTRY.get()
        logins = [login[0] for login in self.CUR.execute("SELECT login FROM users").fetchall()]
            
        if incoming_login not in logins:
            incoming_email = self.R_EMAIL_ENTRY.get()
        
            if validators.email(incoming_email):
                incoming_password = self.R_PASSWORD_ENTRY.get()
                
                if len(incoming_password) >= 8:
                    
                    if incoming_password == self.R_CONFIRM_PASSWORD_ENTRY.get():
                        add_user_query = "INSERT INTO users (login, email, password, creationdate) VALUES (?, ?, ?, ?)"
                        
                        creation_date = date.today()
                        user_values = (incoming_login, incoming_email, incoming_password, creation_date)
                        
                        self.CUR.execute(add_user_query, user_values)
                        self.CONN.commit()
                        self.CONN.close()
                        self.destroy(success_login = True)

                        main_app.app.set_profile_data(
                            creation_date = creation_date,
                            username = incoming_login,
                            email = incoming_email
                        )
                        profile_path = os.path.abspath(f"resources/profiles/{incoming_login}")
                        
                        if not os.path.exists(profile_path):
                            os.mkdir(profile_path)
                            os.mkdir(os.path.join(profile_path, "qrcodes"))
                        
                        main_app.app.QRCODE_IMAGE.set_profile_name(profile_name = incoming_login)
                        main_app.app.QRCODE_IMAGE.set_qrcode_path()
                        
                        # main_app.app.QRCODE_IMAGE.PROFILE_NAME = incoming_login
                        
                        

                        messagebox.showinfo("Успішно!", "Користувача зарєстровано!")
                        main_app.app.mainloop()
                    else:
                        messagebox.showwarning("Увага!", "Введені паролі не співпадають!")
                
                else:
                    messagebox.showwarning("Увага!", "Довжина паролю має бути як мінімум 8 символів!")
                
            else:
               messagebox.showwarning("Увага!", "Будь ласка, вкажіть корректну електронну пошту!")
        
        else:
            messagebox.showwarning("Увага!", "Такий користувач вже існує!")
            
        
                
    def sign_in(self):
        users = self.CUR.execute("SELECT email, password, creationdate, login FROM users").fetchall()
        emails = [user[0] for user in users]
        
        incoming_email = self.L_EMAIL_ENTRY.get()

        if incoming_email in emails:      
            incoming_password = self.L_PASSWORD_ENTRY.get()
            user_index = emails.index(incoming_email)
            user_password_in_db = users[user_index][1]
            user_creation_date = users[user_index][2]
            username  = users[user_index][3]

            if incoming_password == user_password_in_db:
                self.destroy(success_login = True)
                messagebox.showinfo("Успішно!", "Вхід до профілю виконано!")
                self.CONN.close()
                main_app.app.set_profile_data(
                    creation_date = user_creation_date,
                    username = username,
                    email = incoming_email
                )
                
                main_app.app.QRCODE_IMAGE.set_profile_name(profile_name = username)
                main_app.app.QRCODE_IMAGE.set_qrcode_path()
                main_app.app.QRCODE_IMAGE.view_qrcode_history()
                main_app.app.mainloop()
            else:
                messagebox.showerror("Помилка!", "Невірне ім'я користувача/пароль")
        else:
            messagebox.showerror("Помилка!", "Невірне ім'я користувача/пароль")


    def destroy(self, success_login = False):
        super().__init__()
        if not success_login: exit()


login_app = LoginApp()