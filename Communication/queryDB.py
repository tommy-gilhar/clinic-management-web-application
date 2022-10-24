# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:20:14 2020

@author: hadas
"""
from Initialization.serverlnitiation import *
import pandas as pd
import os
from datetime import date
from datetime import datetime

dir_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)

# cursor = connect2server()
cursor, con = connect2server_db(database="emr")


# get the basic info of selected patient
# taken from tables patients
# output the patient's full name, Age, and Diabetes_type
# save output to csv and return the dataframe output
def user_patient_info(patient_id):
    try:
        cursor.execute(
            f"SELECT Full_Name, Age, Gender, Diabetes_type FROM "
            f"patients WHERE patientID = {patient_id} "
        )
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=["Full_Name", "Age", "Gender", "Diabetes_type"])
        df.to_csv(
            f"{dir_path}\\{patient_id}_patients.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\{patient_id}_patients.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


# get patient active_drugs including the date (when the drug was prescribed by the doc), medicine name and dosage(mg))
# Taken from table drugs which including all patients activated and history drugs
# (active drug is defined by the active column in the drugs table where 1 mean active and 0 mean non active(history))


def user_active_drugs(patient_id):
    try:
        cursor.execute(
            f"SELECT Date, Medicine_name, dosage_mg FROM drugs WHERE patientID = {patient_id} AND Active=1"
        )
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=["Date", "Medicine_name", "dosage_mg"])
        df.to_csv(
            f"{dir_path}\\{patient_id}_activeDrugs.csv",
            sep=",",
            index=False,
            mode="a",
            header=(not os.path.exists(f"{dir_path}\\{patient_id}_activeDrugs.csv")),
        )
        return df
    except Exception as e:
        print(e)
        return e


# Insert a new drug to patient
# Return and save the updated drug table

def add_new_drug(patient_id, medicine_name, dosage_mg):
    date_str = date.today().strftime("%Y-%m-%d")
    try:
        cursor.execute(
            f"INSERT INTO drugs\
                     VALUES ('{date_str}', '{patient_id}', '{medicine_name}', '{dosage_mg}','1')"
        )
        con.commit()
        cursor.execute(f"SELECT * FROM drugs")
        res = cursor.fetchall()
        df = pd.DataFrame(
            res, columns=["Date", "patientID", "Medicine_name", "dosage_mg", "Active"]
        )
        for i, d in enumerate(df.iloc[:, 0]):
            d_d = datetime.strptime(d, "%Y-%m-%d")
            df.iloc[i, 0] = d_d.strftime("%d/%m/%Y")
        df.to_csv(f"{dir_path}\\drugs.csv", sep=",", index=False)
        return df
    except Exception as e:
        print(e)
        return e


# in order to cancel a drug form the activated drugs we need to update the active cell from 1 to 0.
# in this query we update the active cell from 1 to 0 (in the drugs table) w
def cancel_drug(patient_id, medicine_name):
    try:
        cursor.execute(
            f"UPDATE drugs SET Active='0' WHERE \
        Active='1' AND \
        Medicine_name='{medicine_name}' AND\
        patientID='{patient_id}'"
        )
        con.commit()
        cursor.execute(f"SELECT * FROM drugs")
        res = cursor.fetchall()
        df = pd.DataFrame(
            res, columns=["Date", "patientID", "Medicine_name", "dosage_mg", "Active"]
        )
        df.to_csv(f"{dir_path}\\drugs.csv", sep=",", index=False)
        return df
    except Exception as e:
        print(e)
        return e


# in order to change a specific drug dosage from activated drugs  we need to first use the cancel_drug function
# that will update the active cell from 1 to 0 in the drugs table (make it a history(non activated))
# and then to use the add_new_drug function to insert the same drug_name with the new dosage.
# it is important to note that specific patient can't has a specific medicine more than once in active mode(active =1).


def change_drug_dosage(patient_id, medicine_name, new_dosage):
    try:
        cancel_drug(patient_id, medicine_name)
        df = add_new_drug(patient_id, medicine_name, new_dosage)
        df.to_csv(f"{dir_path}\\drugs.csv", sep=",", index=False)
        return df
    except Exception as e:
        print(e)
        return e


# lab_result_per_patient_and_per_interval
# The query takes patient id and time-frame defined by user and returns all columns
# taken from labresults.csv of the patient and time frame provided.


def lab_result_per_patient_and_per_interval(patient_id, interval):
    try:
        cursor.execute(f"SELECT * FROM labresults WHERE patientID = {patient_id} AND Date >= date_sub(NOW(),interval {interval.lower()})")
        res = cursor.fetchall()
        df = pd.DataFrame(res,
                          columns=["Date", "patientID", "HbA1C",
                                   "AST", "ALT", "ALBUMIN", "KETONE", "GLUCOSE",
                                   "BILIRUBIN", "PROTEIN", "LDL", "HDL"])
        df.to_csv(f"{dir_path}\\{patient_id}_lab_results_for_{interval}.csv",
                  sep=',', index=False, mode='a',
                  header=(not os.path.exists(f"{dir_path}\\{patient_id}_lab_results_for_{interval}.csv")))
        return df
    except Exception as e:
        print(e)
        return e


def main():
    patient_id = "1"
    print(f"Results for patient: {patient_id}")
    print("\nqueryUserPatientInfo")
    user_patient_info(patient_id)
    print("\nqueryUserActiveDrugs")
    user_active_drugs(patient_id)
    print("\nadd_new_drug")
    add_new_drug(patient_id, "Glipizide", "100")
    print("\ncancel_drug")
    cancel_drug(patient_id, "Tresiba")
    print("\nchange_drug_dosage")
    change_drug_dosage(patient_id, "Praluent", 200)
    print("\nlab_result_per_patient_and_per_interval")
    lab_result_per_patient_and_per_interval(patient_id, "1 year")
    print("\nget_latest_lab_result_per_patient")


if __name__ == "__main__":
    main()
