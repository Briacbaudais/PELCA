import customtkinter as ctk
import os
from PIL import Image
from tkinter import Text

ctk.set_appearance_mode("dark")

class DarkModeColors:
    def __init__(self):
        self.bg_color = "#2E2E2E"
        self.fg_color = "#FFFFFF"
        self.button_color = "#4E4E4E"
        self.separator_color = "#242424"


# Récupérer les chemins des variables d'environnement
icon_path = os.getenv('ICON_PATH', os.path.join('assets','icon.ico'))
image_path = os.getenv('IMAGE_PATH', os.path.join('assets','first_image.png'))


class FrameBase(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color=DarkModeColors().bg_color)


class MainFrame(FrameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=10, pady=10, fill='both', expand=True)


class LeftFrame(FrameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side='left', padx=10, pady=10, fill='y')
        self.create_widgets()

    def create_widgets(self):
        colors = DarkModeColors()
        label_file_path = ctk.CTkLabel(self, text="Select Input File:", fg_color=colors.bg_color, text_color=colors.fg_color)
        label_file_path.grid(row=0, column=0, padx=5, pady=5)

        entry_file_path = ctk.CTkEntry(self, width=300, fg_color=colors.button_color, text_color=colors.fg_color)
        entry_file_path.grid(row=0, column=1, padx=5, pady=5)

        button_browse = ctk.CTkButton(self, text="Browse", command=self.browse_file, fg_color=colors.button_color, text_color=colors.fg_color)
        button_browse.grid(row=0, column=2, padx=5, pady=5)

        button_run = ctk.CTkButton(self, text="Run Script", command=self.run_script_threaded, fg_color=colors.button_color, text_color=colors.fg_color)
        button_run.grid(row=1, column=0, columnspan=3, pady=10)

        self.loading_label = ctk.CTkLabel(self, text="", fg_color=colors.bg_color, text_color=colors.fg_color)
        self.loading_label.grid(row=2, column=0, columnspan=3, pady=5)

        # Créez le widget console
        console_frame = ctk.CTkFrame(self, fg_color=colors.bg_color)
        console_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

        self.console_text = Text(console_frame, bg=colors.bg_color, fg=colors.fg_color, wrap='word', state='disabled')
        self.console_text.pack(padx=10, pady=10, fill='both', expand=True)

    def browse_file(self):
        # Placeholder for the actual implementation of browse_file
        pass

    def run_script_threaded(self):
        # Placeholder for the actual implementation of run_script_threaded
        pass


class RightFrame(FrameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side='right', fill='both', expand=True)

class SeparatorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=8, height=600, fg_color=DarkModeColors().separator_color)
        self.pack(side='left', fill='y')

class DataFrame(FrameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side='bottom', fill='x', padx=10, pady=10)

class NavButtonsFrame(FrameBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side='top', fill='x', padx=10, pady=10)


class PelcaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("PELCA")
        self.configure(bg=DarkModeColors().bg_color)
        self.after(201, lambda: self.iconbitmap(icon_path))
        top_image = ctk.CTkImage(dark_image=Image.open(image_path), size=(1654//4, 578//4))
        image_label = ctk.CTkLabel(self, image=top_image, text='')
        image_label.pack(pady=10)

        self.var_EI = ctk.StringVar()
        self.var_EI_manu = ctk.StringVar()
        self.var_EI_use = ctk.StringVar()
        self.var_fault_cause = ctk.StringVar()
        self.var_RU_age = ctk.StringVar()

        self.main_frame = MainFrame(self)
        self.left_frame = LeftFrame(self.main_frame)
        self.right_frame = RightFrame(self.main_frame)
        self.separator_frame = SeparatorFrame(self.main_frame)
        self.data_frame = DataFrame(self.right_frame)
        self.nav_buttons_frame = NavButtonsFrame(self.right_frame)
        self.plot_frame = ctk.CTkFrame(self.right_frame, fg_color=DarkModeColors().bg_color)
        self.plot_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        self.plot_frame.pack_propagate(False)

        selection_frame = ctk.CTkFrame(self.right_frame, fg_color=DarkModeColors().bg_color)
        selection_frame.pack(side='right', fill='y', padx=10, pady=10)

        # Frame pour les espaces en haut et en bas
        top_spacer = ctk.CTkFrame(self.right_frame, fg_color=DarkModeColors().bg_color)
        top_spacer.pack(side='top', fill='both', expand=True)

        bottom_spacer = ctk.CTkFrame(self.right_frame, fg_color=DarkModeColors().bg_color)
        bottom_spacer.pack(side='bottom', fill='both', expand=True)

        self.prev_button = ctk.CTkButton(self.nav_buttons_frame, text="Previous", command=self.show_prev_plot, fg_color=DarkModeColors().button_color, text_color=DarkModeColors().fg_color, state="disabled")
        self.save_button = ctk.CTkButton(self.nav_buttons_frame, text="Save All", command=self.save_plot, fg_color=DarkModeColors().button_color, text_color=DarkModeColors().fg_color, state="disabled")
        self.save_selected_button = ctk.CTkButton(self.nav_buttons_frame, text="Save", command=self.save_selected_plot, fg_color=DarkModeColors().button_color, text_color=DarkModeColors().fg_color, state="disabled")
        self.next_button = ctk.CTkButton(self.nav_buttons_frame, text="Next", command=self.show_next_plot, fg_color=DarkModeColors().button_color, text_color=DarkModeColors().fg_color, state="disabled")

        self.create_checkboxes()
        self.create_save_button()

        self.prev_button.pack(side='left', padx=5, pady=5)
        self.next_button.pack(side='left', padx=5, pady=5)
        self.save_selected_button.pack(side='left', padx=5, pady=5)
        self.save_button.pack(side='top', fill='x', padx=5, pady=10)

        self.nav_buttons_frame.grid_columnconfigure(0, weight=1)
        self.nav_buttons_frame.grid_columnconfigure(1, weight=1)
        self.nav_buttons_frame.grid_columnconfigure(2, weight=1)


      

        self.current_index = 0

    def show_next_plot(self):
        # Placeholder for the actual implementation of show_next_plot
        pass

    def create_checkboxes(self):
        checkbox_EI = ctk.CTkCheckBox(self, text="Impact total", variable=self.var_EI, onvalue='EI', offvalue='', state="disabled")
        checkbox_EI.pack(side='left', padx=5)

        checkbox_EI_manu = ctk.CTkCheckBox(self, text="Impact manufact.", variable=self.var_EI_manu, onvalue='EI_manu', offvalue='', state="disabled")
        checkbox_EI_manu.pack(side='left', padx=5)

        checkbox_EI_use = ctk.CTkCheckBox(self, text="Impact use", variable=self.var_EI_use, onvalue='EI_use', offvalue='', state="disabled")
        checkbox_EI_use.pack(side='left', padx=5)

        checkbox_fault_cause = ctk.CTkCheckBox(self, text="Fault cause", variable=self.var_fault_cause, onvalue='fault_cause', offvalue='', state="disabled")
        checkbox_fault_cause.pack(side='left', padx=5)

        checkbox_RU_age = ctk.CTkCheckBox(self, text="RU age", variable=self.var_RU_age, onvalue='RU_age', offvalue='', state="disabled")
        checkbox_RU_age.pack(side='left', padx=5)

    def create_save_button(self):
        save_data_button = ctk.CTkButton(self, text="Save Data", command=self.save_data_to_excel, fg_color=DarkModeColors().button_color, text_color=DarkModeColors().fg_color, state="disabled")
        save_data_button.pack(side='left', padx=10)

    def save_data_to_excel(self):
        # Placeholder for the actual implementation of save_data_to_excel
        pass

    def show_prev_plot(self):
        # Placeholder for the actual implementation of show_prev_plot
        pass

    def save_plot(self):
        # Placeholder for the actual implementation of save_plot
        pass

    def save_selected_plot(self):
        # Placeholder for the actual implementation of save_selected_plot
        pass

if __name__ == "__main__":
    app = PelcaGUI()
    app.mainloop()
