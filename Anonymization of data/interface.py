import customtkinter as ctk
from tkinter import filedialog


class InterfaceApp:
    def __init__(self, root: ctk.CTk):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Anonymization of data App")

        self.input_file = ""
        self.button_ds_anon = None
        self.button_k_anon_calc = None
        self.input_file_button = None
        self.input_file_label = None

        self.create_interface()

    def create_interface(self) -> None:
        """ Create a label to show the selected input file """
        self.input_file_label = ctk.CTkLabel(self.root, text="Input file: Not Selected")
        self.input_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        """ Create a button to select the input file """
        self.input_file_button = ctk.CTkButton(self.root, text="Select", command=self.select_input_file)
        self.input_file_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        """ Create a button to start dataset anonymization """
        self.button_ds_anon = ctk.CTkButton(self.root, text="Dataset anonymization", command=self.start_ds_anon)
        self.button_ds_anon.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        """ Create a button to start calculating k-anonymity """
        self.button_k_anon_calc = ctk.CTkButton(self.root, text="Calculating k-anonymity", command=self.start_k_anon_calc)
        self.button_k_anon_calc.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    def select_input_file(self) -> None:
        self.input_file = filedialog.askopenfilename()
        if self.input_file:
            self.input_file_label.configure(text="Input file: Selected")

    def start_ds_anon(self) -> None:
        pass

    def start_k_anon_calc(self) -> None:
        pass


if __name__ == "__main__":
    window = ctk.CTk()
    InterfaceApp(window)
    window.mainloop()
