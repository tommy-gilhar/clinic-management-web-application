import sys
import tkinter
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from Communication.queryDB import *
from FrontEtd.menu_memory import MenuMemory

doc_id = ""
patient_id = ""
dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
blood_test_df = pd.DataFrame


class Frame1(ttk.Frame):
    def __init__(self, app: tkinter.Tk):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=10, width=150, height=10
        )
        self.__create_widgets(app)
        self.errorMassage = None
        return

    def get_doc_name(self, doctors_csv):
        global doc_id
        doc_name = " "
        doc_id = self.DoctorIDCombobox.get()
        for i in range(len(doctors_csv)):

            if str(doctors_csv.iloc[i]["DOC_ID"]) == doc_id:
                doc_name = doctors_csv.iloc[i]["Full_Name"]

        self.DoctorName.configure(state="normal")
        self.DoctorName.delete(0, "end")
        self.DoctorName.insert(0, doc_name)
        self.DoctorName.configure(state="readonly")

        # Delete currently selected patient name and ID
        self.PatientIDCombobox.set("")
        self.patientNameEntry.configure(state="normal")
        self.patientNameEntry.delete(0, "end")
        self.patientNameEntry.configure(state="readonly")
        return doc_name

    def get_patients_id(self, doc_id, patients_csv):
        patients_id = []
        for i in range(len(patients_csv)):
            if str(patients_csv.iloc[i]["DOC_ID"]) == doc_id:
                patients_id.append(patients_csv.iloc[i]["patientID"])
        self.PatientIDCombobox.delete(0, "end")
        self.PatientIDCombobox["values"] = patients_id
        return patients_id

    def get_patients_name(self, patients_csv):
        global patient_id
        patient_name = " "
        patient_id = self.PatientIDCombobox.get()
        for i in range(len(patients_csv)):
            if str(patients_csv.iloc[i]["patientID"]) == patient_id:
                patient_name = patients_csv.iloc[i]["Full_Name"]
        self.patientNameEntry.configure(state="normal")
        self.patientNameEntry.delete(0, "end")
        self.patientNameEntry.insert(0, patient_name)
        self.patientNameEntry.configure(state="readonly")
        self.master.unlock_buttons()
        return patient_name

    def __create_widgets(self, app):
        global doc_id
        self.columnconfigure([1, 2, 3, 4], weight=1, minsize=10)
        self.rowconfigure([1, 2], weight=1, minsize=50)

        # Doctor ID label
        self.labelDoctorID = tk.Label(
            self,
            text="Doctor ID",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelDoctorID.grid(column=1, row=1, padx=0, pady=5)
        # self.labelPatientID.pack(side=tk.LEFT)
        # Doctor ID Entry
        doctors_csv = pd.read_csv(f"{dir_path}\\doctors.csv")
        doctors_id = []
        doctors_name = []
        for i in range(len(doctors_csv)):
            doctors_id.append(doctors_csv.iloc[i]["DOC_ID"])
            doctors_name.append(doctors_csv.iloc[i]["Full_Name"])

        self.DoctorIDCombobox = ttk.Combobox(
            self, values=doctors_id, width=12, state="readonly"
        )
        self.DoctorIDCombobox.insert(0, "doctor id")
        self.DoctorIDCombobox.grid(column=2, row=1, padx=0, pady=5)
        self.DoctorIDCombobox.bind(
            "<<ComboboxSelected>>", lambda e: self.get_doc_name(doctors_csv)
        )

        # Patient first name label
        self.labelDoctorName = tk.Label(
            self,
            text="Doctor's Name",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelDoctorName.grid(column=3, row=1, padx=0, pady=5)

        # Doctor Name field
        self.DoctorName = tk.Entry(self, width=15, state="readonly")
        self.DoctorName.grid(column=4, row=1, padx=0, pady=5)

        # Patient ID label
        self.labelPatientID = tk.Label(
            self,
            text="Patient's ID",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientID.grid(column=1, row=2, padx=0, pady=5)
        # self.labelPatientID.pack(side=tk.LEFT)

        patients_csv = pd.read_csv(f"{dir_path}\\patients.csv")

        # Patient ID list
        self.PatientIDCombobox = ttk.Combobox(
            self, values=[" "], width=12, state="readonly"
        )
        self.PatientIDCombobox.insert(0, "patient's id")
        self.PatientIDCombobox.grid(column=2, row=2, padx=0, pady=5)
        self.PatientIDCombobox.bind(
            "<Button-1>",
            lambda e: self.get_patients_id(self.DoctorIDCombobox.get(), patients_csv),
        )

        self.labelPatientName = tk.Label(
            self,
            text="Patient's Name",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientName.grid(column=3, row=2, padx=0, pady=5)
        self.patientNameEntry = tk.Entry(self, width=15, state="readonly")
        self.patientNameEntry.grid(column=4, row=2, padx=0, pady=5)
        self.PatientIDCombobox.bind(
            "<<ComboboxSelected>>", lambda e: self.get_patients_name(patients_csv)
        )

        if self.master.menu_memory:
            self.DoctorIDCombobox.current(
                doctors_id.index(int(self.master.menu_memory.doctor))
            )
            self.get_doc_name(doctors_csv)
            patients_id = self.get_patients_id(
                self.DoctorIDCombobox.get(), patients_csv
            )
            self.PatientIDCombobox.current(
                patients_id.index(int(self.master.menu_memory.patient))
            )
            self.get_patients_name(patients_csv)
            self.master.frame2.get_patient()
        return True

    def id_error(self):
        self.errorMassage = tk.Label(
            self, text="ID error - numbers only please", fg="red", width=50, height=2
        )
        self.errorMassage.grid(column=1, row=2, columnspan=3, padx=5, pady=5)
        self.after(2000, self.errorMassage.destroy)
        return

    def clear_id_error(self):
        self.errorMassage.destroy()
        return


class Frame2(ttk.Frame):
    def __init__(self, app):
        super().__init__(
            master=app, relief=tk.RAISED, borderwidth=10, width=200, height=10
        )
        self.__create_widgets()

    def get_patient(self):
        global doc_id, patient_id
        if patient_id == "":
            messagebox.showinfo(
                "Patient ID Error",
                "Choose Doctor ID, then Patient ID and press Load Patient button again",
            )
            return
        user_info = user_patient_info(patient_id)
        self.PatientFullName.configure(state="normal")
        self.PatientFullName.delete(0, "end")
        self.PatientFullName.insert(0, user_info.iloc[0]["Full_Name"])
        self.PatientFullName.configure(state="readonly")

        self.PatientAge.configure(state="normal")
        self.PatientAge.delete(0, "end")
        self.PatientAge.insert(0, user_info.iloc[0]["Age"])
        self.PatientAge.configure(state="readonly")

        self.PatientGender.configure(state="normal")
        self.PatientGender.delete(0, "end")
        self.PatientGender.insert(0, user_info.iloc[0]["Gender"])
        self.PatientGender.configure(state="readonly")

        self.PatientDiabetes.configure(state="normal")
        self.PatientDiabetes.delete(0, "end")
        self.PatientDiabetes.insert(0, user_info.iloc[0]["Diabetes_type"])
        self.PatientDiabetes.configure(state="readonly")

        active_drugs = user_active_drugs(patient_id)
        self.drugs_text.configure(state="normal")
        self.drugs_text.delete("1.0", "end")
        self.drugs_text.insert("end", active_drugs.to_markdown(index=False))
        self.drugs_text.configure(state="disabled")

    def __create_widgets(self):
        self.columnconfigure([1, 2, 3, 4], weight=1, minsize=10)
        self.rowconfigure([1, 2, 3, 4, 6], weight=1, minsize=50)
        self.loadPatient = ttk.Button(
            self,
            style="TButton",
            text="Load Patient",
            command=lambda: self.get_patient(),
            width=40,
        )
        self.loadPatient.grid(column=1, row=1, padx=0, pady=5, columnspan=4)
        # FULL NAME
        self.labelPatientFullName = tk.Label(
            self,
            text="Full Name",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientFullName.grid(column=1, row=2, padx=0, pady=5)

        self.PatientFullName = tk.Entry(self, width=15, state="readonly")
        self.PatientFullName.grid(column=1, row=3, padx=0, pady=5)
        # AGE
        self.labelPatientAge = tk.Label(
            self,
            text="Age",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientAge.grid(column=2, row=2, padx=0, pady=5)

        self.PatientAge = tk.Entry(self, width=15, state="readonly")
        self.PatientAge.grid(column=2, row=3, padx=0, pady=5)

        # Gender
        self.labelPatientGender = tk.Label(
            self,
            text="Gender",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientGender.grid(column=3, row=2, padx=0, pady=5)

        self.PatientGender = tk.Entry(self, width=15, state="readonly")
        self.PatientGender.grid(column=3, row=3, padx=0, pady=5)

        # Diabetes
        self.labelPatientDiabetes = tk.Label(
            self,
            text="Diabetes Type",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.labelPatientDiabetes.grid(column=4, row=2, padx=0, pady=5)

        self.PatientDiabetes = tk.Entry(self, width=15, state="readonly")
        self.PatientDiabetes.grid(column=4, row=3, padx=0, pady=0)

        self.labeldrugs_text = tk.Label(
            self,
            text="Patient's active drugs:",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=25,
            height=1,
        )
        self.labeldrugs_text.grid(column=1, row=4, padx=0, pady=5, columnspan=2)

        self.drugs_text = scrolledtext.ScrolledText(
            self, width=50, height=5, wrap="word", state="disabled"
        )
        self.drugs_text.grid(column=1, row=5, padx=0, pady=0, columnspan=4)

        # Change Drug
        self.change_drug_btn = tk.Button(
            self,
            text="Change Drug",
            command=lambda: self.master.change_to_drug_window(patient_id, doc_id),
            width=20,
            state=tk.DISABLED,
        )
        self.change_drug_btn.grid(column=0, row=6, columnspan=3)

        # Blood Test
        self.blood_test_btn = tk.Button(
            self,
            text="View Blood Test",
            command=lambda: self.master.change_to_blood_test_window(patient_id, doc_id),
            width=20,
            state=tk.DISABLED,
        )
        self.blood_test_btn.grid(column=3, row=6, padx=7, columnspan=3)
        return True


class Frame4(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.create_button(app)

    def create_button(self, app):
        self.button = tk.Button(
            master=self,
            text="Exit",
            bg="light green",
            fg="black",
            font=("Times New Roman", 12),
            command=lambda: sys.exit(),
        )
        self.button.pack(side=tk.BOTTOM)


class Frame5(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.__create_widgets()
        return

    def __create_widgets(self):
        global patient_id
        self.columnconfigure([1, 2, 3, 4], weight=1, minsize=10)
        self.rowconfigure([1, 2], weight=1, minsize=50)
        # Patient ID
        self.patient_id_title_lbl = tk.Label(
            self,
            text="Patient's ID:",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.patient_id_title_lbl.grid(column=0, row=0, padx=0, pady=5)
        self.patient_id_lbl = tk.Entry(self, width=15, readonlybackground="white")
        self.patient_id_lbl.insert(tk.END, patient_id)
        self.patient_id_lbl.configure(state="readonly")
        self.patient_id_lbl.grid(column=1, row=0, padx=0, pady=5)

        # Interval
        self.time_interval_lbl = tk.Label(
            self,
            text="Time Interval:",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.time_interval_lbl.grid(column=0, row=1, padx=0, pady=5)
        self.number_interval_lbl = tk.Label(
            self,
            text="Number:",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.number_interval_lbl.grid(column=1, row=1, padx=0, pady=5)
        self.number_interval_combo_box = ttk.Combobox(
            self,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            width=12,
            state="readonly",
        )
        self.number_interval_combo_box.grid(column=2, row=1, padx=0, pady=5)

        self.time_interval_lbl = tk.Label(
            self,
            text="Time Frame:",
            fg="black",  # Set the text color to white
            bg="grey",  # Set the background color to black
            width=12,
            height=1,
        )
        self.time_interval_lbl.grid(column=3, row=1, padx=0, pady=5)
        self.time_interval_combo_box = ttk.Combobox(
            self,
            values=["DAY", "WEEK", "MONTH", "QUARTER", "YEAR"],
            width=12,
            state="readonly",
        )
        self.time_interval_combo_box.grid(column=4, row=1, padx=0, pady=5)
        self.time_interval_combo_box.bind(
            "<<ComboboxSelected>>", lambda e: self.__get_blood_test()
        )

    def __get_blood_test(self):
        global patient_id
        global blood_test_df
        interval = self.time_interval_combo_box.get()
        interval_number = self.number_interval_combo_box.get()
        interval = f"{interval_number} {interval}"
        blood_test_df = lab_result_per_patient_and_per_interval(patient_id, interval)
        # We are moving the df to the master in order to send it to the Blood test frame, to show the df
        self.master.show_blood_test()


class Frame6(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.__create_widgets()

    def __create_widgets(self):
        # Blood test view
        self.blood_test_text = scrolledtext.ScrolledText(
            self, width=135, height=10, wrap="word", state="disabled"
        )
        self.blood_test_text.grid(column=0, row=2, padx=0, pady=0, columnspan=4)

    def show_blood_test(self):
        global blood_test_df
        self.blood_test_text.configure(state="normal")
        self.blood_test_text.delete("1.0", "end")
        self.blood_test_text.insert("end", blood_test_df.to_markdown(index=False))
        self.blood_test_text.configure(state="disabled")


class Frame7(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.__create_widgets()

    def __create_widgets(self):
        self.back_menu_btn = ttk.Button(
            self,
            style="TButton",
            text="Back",
            command=lambda: self.master.change_blood_to_menu_view(),
            width=40,
        )
        self.back_menu_btn.grid(column=0, row=0, padx=0, pady=5)


class Frame8(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.__create_widgets()

    def __create_widgets(self):
        global patient_id
        self.columnconfigure([1, 2, 3, 4, 5, 6], weight=50, minsize=60)
        self.rowconfigure([1, 2, 3, 4], weight=1, minsize=50)

        self.drugs_text = scrolledtext.ScrolledText(
            self, width=50, height=5, wrap="word", state="disabled"
        )
        self.drugs_text.grid(column=1, row=0, padx=0, pady=0, columnspan=4)
        self.refresh_table()
        #####################################
        #           Change Dosage           #
        #####################################
        self.change_dosage_lbl = tk.Label(
            self,
            text="Change Dosage:",
            fg="black",  # Set the text color to white
            bg="gray",  # Set the background color to black
            width=12,
            height=1,
        )
        self.change_dosage_lbl.grid(column=0, row=1, padx=10)

        self.drug_name_lbl = tk.Label(
            self,
            text="Name",
            fg="black",  # Set the text color to white
            width=12,
            height=1,
        )
        self.drug_name_lbl.grid(column=1, row=1, padx=10)

        self.drug_name_combo_box = ttk.Combobox(
            self,
            values=self.active_drugs["Medicine_name"].tolist(),
            width=12,
            state="readonly",
        )
        self.drug_name_combo_box.grid(column=2, row=1, padx=10)

        self.drug_dosage_lbl = tk.Label(
            self,
            text="Dosage",
            fg="black",  # Set the text color to white
            width=12,
            height=1,
        )
        self.drug_dosage_lbl.grid(column=3, row=1, padx=10)

        self.drug_dosage_entry = tk.Entry(self, width=15, readonlybackground="white")
        self.drug_dosage_entry.grid(column=4, row=1, padx=10)

        self.drug_update_btn = ttk.Button(
            self,
            style="TButton",
            text="Update",
            command=lambda: self.drug_dosage(
                self.drug_name_combo_box.get(), self.drug_dosage_entry.get()
            ),
            width=10,
        )
        self.drug_update_btn.grid(column=5, row=1, padx=10)

        #####################################
        #           Add New Drug            #
        #####################################
        self.add_drug_lbl = tk.Label(
            self,
            text="Add Drug:",
            fg="black",  # Set the text color to white
            bg="gray",  # Set the background color to black
            width=12,
            height=1,
        )
        self.add_drug_lbl.grid(column=0, row=2, padx=10)

        self.add_drug_name_lbl = tk.Label(
            self,
            text="Name",
            fg="black",  # Set the text color to white
            width=12,
            height=1,
        )
        self.add_drug_name_lbl.grid(column=1, row=2, padx=10)

        self.new_drug_name_entry = tk.Entry(self, width=15, readonlybackground="white")
        self.new_drug_name_entry.grid(column=2, row=2, padx=10)

        self.add_drug_dosage_lbl = self.add_drug_name_lbl = tk.Label(
            self,
            text="Dosage",
            fg="black",  # Set the text color to white
            width=12,
            height=1,
        )
        self.add_drug_dosage_lbl.grid(column=3, row=2, padx=10)

        self.add_drug_dosage_entry = tk.Entry(
            self, width=15, readonlybackground="white"
        )
        self.add_drug_dosage_entry.grid(column=4, row=2, padx=10)

        self.add_drug_update_btn = ttk.Button(
            self,
            style="TButton",
            text="Update",
            command=lambda: self.new_drug(
                self.new_drug_name_entry.get(), self.add_drug_dosage_entry.get()
            ),
            width=10,
        )
        self.add_drug_update_btn.grid(column=5, row=2, padx=10)

        #####################################
        #####################################
        #           Delete Drug             #
        #####################################
        self.delete_drug_lbl = tk.Label(
            self,
            text="Delete Drug:",
            fg="black",  # Set the text color to white
            bg="gray",  # Set the background color to black
            width=12,
            height=1,
        )
        self.delete_drug_lbl.grid(column=0, row=3, padx=10)

        self.delete_drug_name_lbl = tk.Label(
            self,
            text="Name",
            fg="black",  # Set the text color to white
            width=12,
            height=1,
        )
        self.delete_drug_name_lbl.grid(column=1, row=3, padx=10)

        self.delete_drug_combo_box = ttk.Combobox(
            self,
            values=self.active_drugs["Medicine_name"].tolist(),
            width=12,
            state="readonly",
        )
        self.delete_drug_combo_box.grid(column=2, row=3, padx=10)

        self.delete_drug_update_btn = ttk.Button(
            self,
            style="TButton",
            text="Update",
            command=lambda: self.delete_drug(self.delete_drug_combo_box.get()),
            width=10,
        )
        self.delete_drug_update_btn.grid(column=5, row=3, padx=10)
        #####################################

    def drug_dosage(self, drug_name: str, dosage: str):
        global patient_id
        if any(c.isalpha() for c in dosage):
            messagebox.showinfo(
                "Value Error", f"Please enter a number, invalid value: {dosage}."
            )
            return
        change_drug_dosage(patient_id, drug_name, dosage)
        self.refresh_table()
        self.refresh_combo_box()

    def new_drug(self, drug_name: str, dosage: str):
        global patient_id
        if any(c.isalpha() for c in dosage):
            messagebox.showinfo(
                "Value Error", f"Please enter a number, invalid value: {dosage}."
            )
            return

        if not all(c.isalpha() for c in drug_name):
            messagebox.showinfo("Invalid Value", f'Invalid drug name: "{drug_name}".')
            return

        if drug_name in self.active_drugs["Medicine_name"].tolist():
            messagebox.showinfo(
                "Already Exists",
                f"Drug {drug_name} already exists in patient {patient_id}.",
            )
            return
        add_new_drug(patient_id, drug_name, dosage)
        self.refresh_table()
        self.refresh_combo_box()

    def delete_drug(self, drug_name: str):
        global patient_id
        cancel_drug(patient_id, drug_name)
        self.refresh_table()
        self.refresh_combo_box()

    def refresh_table(self):
        # Refresh top table
        global patient_id
        self.active_drugs = user_active_drugs(patient_id)
        self.drugs_text.configure(state="normal")
        self.drugs_text.delete("1.0", tk.END)
        self.drugs_text.insert("end", self.active_drugs.to_markdown(index=False))
        self.drugs_text.configure(state="disabled")

    def refresh_combo_box(self):
        # Refresh Combo Boxes
        self.delete_drug_combo_box["values"] = self.active_drugs[
            "Medicine_name"
        ].tolist()
        self.drug_name_combo_box["values"] = self.active_drugs["Medicine_name"].tolist()


class Frame9(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(
            self, master=app, relief=tk.RAISED, borderwidth=5, width=120, height=60
        )
        self.__create_widgets()

    def __create_widgets(self):
        self.back_menu_btn = ttk.Button(
            self,
            style="TButton",
            text="Back",
            command=lambda: self.master.change_drug_to_menu_view(),
            width=40,
        )
        self.back_menu_btn.grid(column=0, row=0, padx=0, pady=5)
