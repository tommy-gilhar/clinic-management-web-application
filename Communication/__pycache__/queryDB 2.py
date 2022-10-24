# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:20:14 2020

@author: hadas
"""
from Initialization.serverlnitiation import *
import pandas as pd
import os
from datetime import date

dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)

# cursor = connect2server()
cursor, con = connect2serverDB(database="emr")


# get the basic info of patient id=1  using 'where' patient ID =1 and Doctor id =21
# taken from tables patients
# output the patient's full name, Age, and Diabetes_type
# save output to csv and return the dataframe output
def user_patient_info(patientID, doc_id):
    try:
        cursor.execute(
            f"SELECT Full_Name, Age, Diabetes_type FROM patients WHERE patientID = {patientID} AND DOC_ID = {doc_id}"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=["Full_Name", "Age", "Diabetes_type"])
        df.to_csv(
            f"{dir_path}\\{patientID}_patients.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\{patientID}_patients.csv")),
        )
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return e


# get patient id=2 active_drugs (Date (when the drug was prescribed by the doc), Medicine_name,dosage_mg)
# from table drugs which including all patients activated and history drugs
# (active drug is defined by the active column in the drugs table where 1 mean active and 0 mean non active(history))
# where patientID =2 and Active=1
def UserActiveDrugs(patientID):
    try:
        cursor.execute(
            f"SELECT Date, Medicine_name, dosage_mg FROM drugs WHERE patientID = {patientID} AND Active=1"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=["Date", "Medicine_name", "dosage[mg]"])
        df.to_csv(
            f"{dir_path}\\{patientID}_activeDrugs.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\{patientID}_activeDrugs.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


# insert a new drug to patient id =9 including the date (the current day taken from datetime library),
# the medicine name which is 'Tresiba' and the dosage 200 mg
def add_new_drug(patientID, Medicine_name, dosage_mg):
    date_str = date.today().strftime("%Y-%m-%d")
    try:
        cursor.execute(
            f"INSERT INTO drugs\
                     VALUES ('{date_str}', '{patientID}', '{Medicine_name}', '{dosage_mg}','1')"
        )
        con.commit()
        cursor.execute(f"SELECT * FROM drugs")
        res = cursor.fetchall()
        df = pd.DataFrame(
            res, columns=["Date", "patientID", "Medicine_name", "dosage[mg]", "Active"]
        )
        df.to_csv(
            f"{dir_path}\\new_activeDrugs.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\new_activeDrugs.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


# in order to cancel a drug form the activated drugs we need to update the active cell from 1 to 0.
# in this query we update the active cell from 1 to 0 (in the drugs table) where patient ID =2
#  and medicine_name is 'Isoniazid'
def cancel_drug(patientID, Medicine_name):
    try:
        cursor.execute(
            f"UPDATE drugs SET Active='0' WHERE \
        Active='1' AND \
        Medicine_name='{Medicine_name}' AND\
        patientID='{patientID}'"
        )
        con.commit()
        cursor.execute(f"SELECT * FROM drugs")
        res = cursor.fetchall()
        df = pd.DataFrame(
            res, columns=["Date", "patientID", "Medicine_name", "dosage[mg]", "Active"]
        )
        df.to_csv(
            f"{dir_path}\\After_cancel_activeDrugs.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\After_cancel_activeDrugs.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


# in order to change a specific drug dosage from activated drugs  we need to first use the cancel_drug function
# that will update the active cell from 1 to 0 in the drugs table (make it an history(non activated))
# and then to use the add_new_drug function to insert the same drug_name with the new dosage.
# it is important to note that specific patient can't has a specific medicine more then once in active mode(active =1).
# in here we change the  medicine 'Tresiba' dosage of patient id=1 from  200 (originally) to 300.


def change_drug_dosage(patientID, Medicine_name, new_dosage):
    try:
        cancel_drug(patientID, Medicine_name)
        df = add_new_drug(patientID, Medicine_name, new_dosage)
        df.to_csv(
            f"{dir_path}\\After_change_activeDrugs.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\After_change_activeDrugs.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


"""
lab_result_per_patient_and_per_interval
The query takes patient id and time-frame defined by user and returns all columns from labresults.csv of the patient and time-frame provided.
The result of query saved in res. The type of res is a list of tuples. 
Because of the res type tuples we print each tuple, save in dataframe and save dataframe to csv BY USING THE LOOP.
When saving dataframe to csv, there is a function for adding headers for columns in csv: 
    it checks if such csv already exists:
        1) if yes - it just adds tuples to csv
        2) if no - it adds headers and then tuple (values in res) itself.
The function built with TRY and EXCEPT, and if something wrong with something under TRY, then the function will print an error and what's wrong
"""


def lab_result_per_patient_and_per_interval(patientID, interval):
    try:
        cursor.execute(
            f"SELECT * FROM labresults WHERE patientID = {patientID} AND Date >= date_sub(NOW(),interval {interval})"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(
            res,
            columns=[
                "Date",
                "patientID",
                "HbA1C",
                "AST",
                "ALT",
                "ALBUMIN",
                "KETONE",
                "GLUCOSE",
                "BILIRUBIN",
                "PROTEIN",
                "LDL",
                "HDL",
            ],
        )
        df.to_csv(
            f"{dir_path}\\{patientID}_lab_results_for_{interval}.csv",
            sep=",",
            index=False,
            mode="a",
            header=(
                not os.path.exists(
                    f"{dir_path}\\{patientID}_lab_results_for_{interval}.csv"
                )
            ),
        )
        return df
    except Exception as e:
        print(e)
        return e


"""
get_latest_lab_result_per_patient
The query takes patient id and return the last lab results of that patient from labresults.csv.
The result of query saved in res. The type of res is list of tuples. 
Because of the res type tuples we print each tuple, save in dataframe and save dataframe to csv BY USING THE LOOP.
When saving dataframe to csv, there is a function for adding headers for columns in csv: 
    it checks if such csv already exists:
        1) if yes - it just adds tuples to csv
        2) if no - it adds headers and then tuple (values in res) itself.
The function built with TRY and EXCEPT, and if something wrong with something under TRY, then the function will print an error and what's wrong
"""


def get_latest_lab_result_per_patient(patientID):
    try:
        cursor.execute(
            f"SELECT * FROM labresults WHERE Date IN (SELECT max(Date) FROM labresults where patientID = {patientID})"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(
            res,
            columns=[
                "Date",
                "patientID",
                "HbA1C",
                "AST",
                "ALT",
                "ALBUMIN",
                "KETONE",
                "GLUCOSE",
                "BILIRUBIN",
                "PROTEIN",
                "LDL",
                "HDL",
            ],
        )
        df.to_csv(
            f"{dir_path}\\Patient_{patientID}_latest_lab_result.csv",
            sep=",",
            index=False,
            mode="a",
            header=(
                not os.path.exists(
                    f"{dir_path}\\Patient_{patientID}_latest_lab_result.csv"
                )
            ),
        )
        return df
    except Exception as e:
        print(e)
        return e


"""
get_over_7_hba1c_patients
The query search for patients that have HbA1C higher than 7 and displays the most recent such result per each patient where HbA1C was > 7. 
Shows all columns from labresults.csv.
The result of query saved in res. The type of res is list of tuples. 
Because of the res type tuples we print each tuple, save in dataframe and save dataframe to csv BY USING THE LOOP.
When saving dataframe to csv, there is a function for adding headers for columns in csv: 
    it checks if such csv already exists:
        1) if yes - it just adds tuples to csv
        2) if no - it adds headers and then tuple (values in res) itself.
The function built with TRY and EXCEPT, and if something wrong with something under TRY, then the function will print an error and what's wrong
"""


def get_over_7_hba1c_patients():
    try:
        cursor.execute(
            f"SELECT * FROM labresults WHERE Date IN (SELECT max(Date) FROM labresults where HBA1C > 7  group by patientID)"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(
            res,
            columns=[
                "Date",
                "patientID",
                "HbA1C",
                "AST",
                "ALT",
                "ALBUMIN",
                "KETONE",
                "GLUCOSE",
                "BILIRUBIN",
                "PROTEIN",
                "LDL",
                "HDL",
            ],
        )
        df.to_csv(
            f"{dir_path}\\over_7_hba1c_patiens.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\over_7_hba1c_patiens.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


"""
asc_hba1c_per_patient
The query displays HbA1C and it's Date per provided patient ID and order them in ascending order by date value. (Thus we can observe how specific patient manage her or his diabetes)  
Shows only Date and HbA1C columns from labresults.csv.
The result of query saved in res. The type of res is list of tuples. 
Because of the res type tuples we print each tuple, save in dataframe and save dataframe to csv BY USING THE LOOP.
When saving dataframe to csv, there is a function for adding headers for columns in csv: 
    it checks if such csv already exists:
        1) if yes - it just adds tuples to csv
        2) if no - it adds headers and then tuple (values in res) itself.
The function built with TRY and EXCEPT, and if something wrong with something under TRY, then the function will print an error and what's wrong
"""


def asc_hba1c_per_patient(patientID):
    try:
        cursor.execute(
            f"SELECT Date, HBA1C FROM labresults WHERE patientID = {patientID} order by Date asc"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=["Date", "HbA1C"])
        df.to_csv(
            f"{dir_path}\\{patientID}_HbA1C.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\{patientID}_HbA1C.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


def main():
    patientID = "1"
    print(f"Results for patient: {patientID}")
    print("\nqueryUserPatientInfo")
    user_patient_info(patientID, "21")
    print("\nqueryUserActiveDrugs")
    UserActiveDrugs(patientID)
    print("\nadd_new_drug")
    add_new_drug(patientID, "Glipizide", "100")
    print("\ncancel_drug")
    cancel_drug(patientID, "Tresiba")
    print("\nchange_drug_dosage")
    change_drug_dosage(patientID, "Praluent", 200)
    print("\nlab_result_per_patient_and_per_interval")
    lab_result_per_patient_and_per_interval(patientID, "1 year")
    print("\nget_latest_lab_result_per_patient")
    get_latest_lab_result_per_patient(patientID)
    print("\nover_7_hba1c_patients")
    get_over_7_hba1c_patients()
    print("\nasc_hba1c_per_patient")
    asc_hba1c_per_patient_result = asc_hba1c_per_patient(patientID)
    if not type(asc_hba1c_per_patient_result) != Exception:
        for i in asc_hba1c_per_patient_result:
            print(i)
    else:
        print(asc_hba1c_per_patient_result)


if __name__ == "__main__":
    main()
