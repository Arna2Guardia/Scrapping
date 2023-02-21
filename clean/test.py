# import des librairies dont nous aurons besoin
import pandas as pd
import numpy as np
import re

# chargement et affichage des données
data = pd.read_csv('operations.csv')


def tests():
    print(data.dtypes)
    print(data.isnull().sum())
    data_null = data.isnull().sum()
    print(data_null[data_null>0])
    print(data.loc[data[['date_operation', 'libelle', 'montant', 'solde_avt_ope']].duplicated(keep=False),:])


tests()

def datetime():
    data['date_operation'] = pd.to_datetime(data['date_operation'])
    print(data.dtypes)

#datetime()
#print(data.loc[data['montant'].isnull(),:])

def montantsNull():
    data_null = data.loc[data['montant'].isnull(),:]
    for index in data_null.index:
    # calcul du montant à partir des soldes précédents et actuels
        data.loc[index, 'montant'] = data.loc[index+1, 'solde_avt_ope'] - data.loc[index, 'solde_avt_ope']
#montantsNull()

def categNull():
    data.loc[data['categ'].isnull(), 'categ'] = 'FACTURE TELEPHONE'
# categNull()
# print(data.loc[data['categ'].isnull(),:])
# print(data.loc[data['libelle'] == 'PRELEVEMENT XX TELEPHONE XX XX', :])

def duplicate():
    data.drop_duplicates(subset=['date_operation', 'libelle', 'montant', 'solde_avt_ope'], inplace=True, ignore_index=True)
# duplicate()
# print(data.loc[data[['date_operation', 'libelle', 'montant', 'solde_avt_ope']].duplicated(keep=False),:])

#print(data.describe())
# a = data.loc[data['montant']==-15000,:].index[0]
# print(a) 
# print(data.iloc[a-1:a+2,:])

def outliers():
    data.loc[data['montant']==-15000, 'montant'] = -14.39
#outliers().

#print(data.loc[data['montant']==-15000, 'montant'])
def deleteError():
    datetime()
    montantsNull()
    categNull()
    duplicate()
    outliers() 

