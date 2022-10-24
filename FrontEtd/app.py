
from views import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Appointment Manager")
        self.geometry("1280x960")
        self.resizable(True, True)
        # layout on the root window
        self.columnconfigure([1], weight=1, minsize=10)
        self.rowconfigure([1, 2, 3, 4], weight=1, minsize=50)
        self.menu_memory = None
        self.__create_frames()

    def __create_frames(self):
        # create the top frame
        self.frame2 = Frame2(self)
        self.frame2.grid(column=1, row=2, padx=5, pady=5)
        self.frame1 = Frame1(self)
        self.frame1.grid(column=1, row=1, padx=5, pady=5)
        self.frame4 = Frame4(self)
        self.frame4.grid(column=1, row=4, padx=5, pady=5)

    def change_to_blood_test_window(self, id_patient: str, id_doctor: str):
        self.menu_memory = MenuMemory(id_doctor, id_patient)
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame4.destroy()
        self.frame5 = Frame5(self)
        self.frame5.grid(column=1, row=0, padx=5, pady=5)
        self.frame6 = Frame6(self)
        self.frame6.grid(column=1, row=1, padx=5, pady=5)
        self.frame7 = Frame7(self)
        self.frame7.grid(column=1, row=2, padx=5, pady=5)

    def show_blood_test(self):
        self.frame6.show_blood_test()

    def change_blood_to_menu_view(self):
        self.frame5.destroy()
        self.frame6.destroy()
        self.frame7.destroy()
        self.__create_frames()

    def change_to_drug_window(self, id_patient: str, id_doctor: str):
        self.menu_memory = MenuMemory(id_doctor, id_patient)
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame4.destroy()
        self.frame8 = Frame8(self)
        self.frame8.grid(column=1, row=1, padx=5, pady=5)
        self.frame9 = Frame9(self)
        self.frame9.grid(column=1, row=2, padx=5, pady=5)

    def change_drug_to_menu_view(self):
        self.frame8.destroy()
        self.frame9.destroy()
        self.__create_frames()

    def unlock_buttons(self):
        self.frame2.blood_test_btn.configure(state=tk.NORMAL)
        self.frame2.change_drug_btn.configure(state=tk.NORMAL)


if __name__ == "__main__":
    app = App()
    app.mainloop()
