# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:13:45 2019

@author: Bhageerath
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from matplotlib.ticker import PercentFormatter
df = pd.read_csv(r"C:\Users\Bhageerath\Desktop\GTA\birthdate.csv")
df1 = pd.read_excel(r"C:\Users\Bhageerath\Desktop\GTA\USPopulation_total.xlsx")
df2 = pd.read_excel(r"C:\Users\Bhageerath\Desktop\GTA\US_female.xlsx")
df1.describe()
df2
df
df['Birthdate'].describe()

df['PAGE'] = np.where(df['PAGE'].isnull(),2019.0-df['YEAR'],df['PAGE'])
#ceo_ages = df['PAGE'][np.bitwise_and(df['CEO']==1,df['GENDER']=='FEMA')]
#ceo_ages = df['PAGE'][np.bitwise_and(df['CEO']==1,df['GENDER']=='MALE')]
#ceo_ages = df['PAGE'][df['CEO']==1]
#ceo_ages = df['PAGE'][df['CEO_top']==1]
ceo_ages = df['PAGE'][np.bitwise_and(df['CEO_top']==1,df['GENDER']=='FEMA')]
svp_ages = df['PAGE'][np.bitwise_and(df['SVP']==1,df['PAGE']>0)]
vp_ages = df['PAGE'][np.bitwise_and(df['VP']==1,df['PAGE']>0)]

df['Astrological_Sign'] = df['Astrological_Sign'][df['Astrological_Sign'].notnull()]

def toString(x):
    return str(x).lower()


num_to_month = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November",
                "12":"December","nan":"nan"}

def to_month(x):
    x = str(x)
    month = ''
    for i in range(len(x)):
        if x[i] == '/':
            break
        month += x[i]
    return num_to_month[month]



def month_filter(x, months):
    name = ""
    for i in months:
        name += i
        name += " "
    if x in months:
        return name
    else:
        return "Rest"





def june_july_filter(x):
    return month_filter(x, ["June","July"])
    
def june_july_august_filter(x):
    return month_filter(x, ["June","July", "August"])

def sep_oct_november(x):
    return month_filter(x, ["September","October","November"])



print(df['Birthdate'][0])
df['Birthdate'] = df['Birthdate'].apply(to_month)

print(df['Birthdate'])
df['Astrological_Sign'] = df['Astrological_Sign'].apply(toString)
print(df['Astrological_Sign'])

ceo_birthdate = df['Birthdate'][df['CEO']==1]
ceo_male_birthdate = ceo_birthdate[df['GENDER']=='MALE']

ceo_male_birthdate.count()
print((ceo_male_birthdate.value_counts()/ceo_male_birthdate.count())*100)
kk = ((ceo_male_birthdate.value_counts()/ceo_male_birthdate.count())*100).to_frame()
yk = ((ceo_birthdate.value_counts()/ceo_birthdate.count())*100).to_frame()

kk = kk.rename(columns={"Birthdate":"Ceo_Male"})
yk = yk.rename(columns={"Birthdate":"Ceo"})
frs = [yk,kk]
df5 = pd.concat(frs,axis=1,sort=False)
print(df5)
df5.to_excel("D:/kk.xlsx")


def birth_day_graph(designation, gender="", func=None):
    birthdate = df['Birthdate'][df[designation] == 1]
    bin_size = 12
    if gender != "":
        birthdate = birthdate[df['GENDER']== gender]
    if func != None:
        birthdate = birthdate.apply(func)
        bin_size = 2
    plt.hist(birthdate,bins=bin_size)
    #plt.hist(birthdate, weights=np.ones(len(birthdate)) / len(birthdate),bins=bin_size)
    #plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xticks(rotation=90)
    plt.savefig("D:/GTA/"+designation+gender+str(func)[9:16])
    plt.show()

def birth_day_number(designation, gender="", func=None):
    birthdate = df['Birthdate'][df[designation] == 1]
    if gender != "":
        birthdate = birthdate[df['GENDER']== gender]
    if func != None:
        birthdate = birthdate.apply(func)
    birthdate = ((birthdate.value_counts()/birthdate.count())*100).to_frame()
    return birthdate.rename(columns={"Birthdate":designation+"_"+gender+"_"+str(func)[9:22]})
    
    #plt.hist(birthdate, weights=np.ones(len(birthdate)) / len(birthdate),bins=bin_size)
    #plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

def  get_percentage(month, df):
    return (df['Birthdate'][df['Birthdate']==month]).count()/df['Birthdate'].count()

def get_months_in_order(df):
    percentages = []
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    for i in months:
        percentages.append(get_percentage(i,df))
    return percentages



print(df1["%"])
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def display(df,df1,name):
    ax = plt.axes()
    ax.plot(get_months_in_order(df),color='Red')
    y = df1["%"]
    ax.plot(y[:12],color='Blue')
    x = [i for i in range(12)]
    ax.legend(['Red - ' + str(name), 'Blue - FEMALE_US_Population'])  
    plt.xticks(x,labels=months,rotation=90)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.show()
    
    
    
    
    
x = [i for i in range(12)]
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
plt.plot(get_months_in_order(df[df['CEO']==1]),color='Red')
plt.plot(get_months_in_order(df[df['SVP']==1]),color='Yellow')
plt.plot(get_months_in_order(df[df['VP']==1]),color='Blue')
plt.plot(get_months_in_order(df[df1['%']==1]),color='Orange')
plt.xticks(x,labels=months,rotation=90)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.show()


positions = df.columns[21:]
funcs = [None,june_july_filter,june_july_august_filter,sep_oct_november]
df_total_months = []
df_sep_months = []
for i in positions:
    for j in ["","MALE", "FEMA"]: 
        for k in funcs:
            #print(i +" "+ j + " "+str(k)+" graph")
            if k == None:
                df_total_months.append(birth_day_number(i,j,k))
            else:
                df_sep_months.append(birth_day_number(i,j,k))
                
df_total = pd.concat(df_total_months,axis=1,sort=False)
df_sep = pd.concat(df_sep_months,axis=1,sort=False)

df_total.to_excel("D:/total_months_report.xlsx")
df_sep.to_excel("D:/sep_months_report.xlsx")


for i in positions:
    display(df[np.bitwise_and(df[i]==1,df['GENDER']=="FEMA")],df2,i)
    
#for i in positions:
 #   display(df[df[i]==1],i)





ceo_june_july = ceo_birthdate.apply(june_july_filter)
print(ceo_june_july)
hist = plt.hist(ceo_june_july,bins=2)
plt.xticks(rotation=90)
plt.show()

ceo_june_july_August = ceo_birthdate.apply(june_july_august_filter)
print(ceo_june_july_august)
hist = plt.hist(ceo_june_july_August,bins=2)
plt.xticks(rotation=90)
plt.show()




ceo_gender = df['GENDER'][df['CEO']==1]
svp_gender = df['GENDER'][np.bitwise_and(df['SVP']==1,df['PAGE']>0)]
vp_gender = df['GENDER'][np.bitwise_and(df['VP']==1,df['PAGE']>0)]
ceo_astro = df['Astrological_Sign'][df['CEO']==1]
print(ceo_astro.describe())

print(ceo_ages.describe())
print(svp_ages.describe())
print(vp_ages.describe())
print(ceo_gender.describe())
print(svp_gender.describe())
print(vp_gender.describe())

hist = plt.hist(df['Birthdate'],bins=12)
plt.xticks(rotation=90)
t = plt.show()

hist = plt.hist(ceo_ages,bins=90)
plt.show()
hist = plt.hist(svp_ages,bins=90)
plt.show()
hist = plt.hist(vp_ages,bins=90)
plt.show()
hist = plt.hist(ceo_gender,bins=2)
plt.show()
hist = plt.hist(svp_gender,bins=2)
plt.show()
hist = plt.hist(vp_gender,bins=2)
plt.show()
hist = plt.hist(ceo_astro,bins=90)
plt.xticks(rotation=90)
plt.show()

#df['PAGE'] = 
df1 = pd.read_excel(r"C:\Users\Bhageerath\Desktop\GTA\USpopulation_total.xlsx")
df1
df1.drop([1930], axis=1)
df1.drop(df1.index[-1])

df1.plot(x='Month', y='Avg', kind='bar') 
h = plt.show()

df2 = pd.read_excel(r"C:\Users\Bhageerath\Desktop\GTA\US_male.xlsx")
df2.drop(['Unnamed: 1'],axis=1)
df2.columns
df3 = pd.read_excel(r"C:\Users\Bhageerath\Desktop\GTA\US_female.xlsx")
df3 
df3.columns
df3.drop(['Unnamed: 1'],axis=1)

df1.mean(axis = 1, skipna = True) 
df2.mean(axis = 1, skipna = True) 
df3.mean(axis = 1, skipna = True) 

df1[1931]['January']
print(df1[1931]['January'])

df1.describe() 
df2.describe()
df3.describe()
df1[1931].describe()
df1.apply(pd.Series.describe, axis=1)
