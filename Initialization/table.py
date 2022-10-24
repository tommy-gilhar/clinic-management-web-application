import pandas as pd
from datetime import datetime
import numpy as np


class Table:
    def __init__(self, table_name, csv_file_name, pks=[], fks=[], ref_tables=[], refs=[]):
        # allocate all relational tableName attributes from csvFile
        self.headers = {}
        self.csvFileName = csv_file_name
        self.tableName = table_name
        self.data = pd.DataFrame()
        self.pks = pks
        self.fks = fks
        self.ref_tables = ref_tables
        self.refs = refs
        try:
            # read csv file into table variable
            self.data = pd.read_csv(self.csvFileName)
            self.headers = self.data.columns
        except FileNotFoundError:
            print("incorrect file name")
        except:
            print("table importing went wrong")
        finally:
            # convert time-stamp format to mysql readable one
            if "Timestamp" in self.data.columns:
                for i in range(self.data.shape[0]):
                    self.data.loc[i, "Timestamp"] = datetime.strptime(
                        self.data.loc[i, "Timestamp"][:-6], "%Y/%m/%d %I:%M:%S %p"
                    )
            for i in self.data.columns:
                if "Date" in i:
                    for j in range(self.data.shape[0]):
                        if isinstance(self.data.loc[j, i], str):
                            print(self.data.loc[j, i])
                            self.data.loc[j, i] = datetime.strptime(
                                self.data.loc[j, i], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")

            # convert np.nan's to nones
            self.data = self.data.where(pd.notnull(self.data), None)
        return
