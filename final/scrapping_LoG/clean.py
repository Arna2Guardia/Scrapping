# import des librairies dont nous aurons besoin
import pandas as pd
import numpy as np
import re

# chargement et affichage des données
data = pd.read_csv('cleaned_tab.csv')
print(data)


def tests(data,columns):
    print(data.dtypes)
    print(data.isnull().sum())
    data_null = data.isnull().sum()
    print(data_null[data_null>0])
    print(data.loc[data[columns].duplicated(keep=False),:])
tests(data,["Name"])

def duplicate(data,columns):
    data.drop_duplicates(subset=columns, inplace=True, ignore_index=True)

def clean(data,columns):
    duplicate(data,columns)
    data.to_csv("cleaned_links.csv", index=False)

clean(data,["Name"])
