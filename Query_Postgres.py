
#This script will download a data set on Causes of Death in the United States. It will connect to PostgreSQL and load the data into a table. It will prompt a user to input a year and a state. It will then perform an SQL query using a where statement to find causes of death for the given year and state.

#download the data set from the website - Change download address as needed
#link to data: https://data.cdc.gov/api/views/bi63-dtpu/rows.csv?accessType=DOWNLOAD	
	#pip3 install wget

import psycopg2
from psycopg2.extensions import AsIs
import wget
import csv

def get_data():

    print('Downloading data on leading causes of death in the USA')
    url = 'https://data.cdc.gov/api/views/bi63-dtpu/rows.csv?accessType=DOWNLOAD'
    wget.download(url, '/home/monte/Documents/Python Scripts/data.csv')
    
get_data()    

#set Python working directory to folder with download

def setwd():
    import os
    os.chdir('/home/monte/Documents/Python Scripts/')
    
setwd()    

#clean data column that gives syntax errors
#install pandas package: pip3 install pandas

def clean_data():
    import pandas as pd
    data = pd.read_csv('./data.csv')
    drop = data.drop('113 Cause Name', axis=1)
    drop.to_csv('cause_death.csv')
    
clean_data()    

#connect to PostgreSQL server, create a table and import the data
# install packages: 
# C Compiler: sudo apt install build-essential
# Python header: sudo apt install python-dev
# Libpq package: sudo apt install libpq-dev
# Psycopg2: pip3 install psycopg2

def import_data():
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    cur=conn.cursor()
    
    cur.execute("""CREATE TABLE Cause_of_Death(ID integer, Year integer, "Cause Name" text, 
    State text, Deaths numeric, "Age-adjusted Death Rate" numeric)""")
    conn.commit()

    with open('cause_death.csv', 'r') as f:
        next(f)
        cur.copy_from(f, 'Cause_of_Death', sep = ',')
        conn.commit()

import_data()

#get input from user


query1 = int(input('please enter a year: '))
query2 = str(input('please enter a state with the first letter capitalized: '))

#query table with user input, print results

def query_table(query1, query2):
	conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
	cur=conn.cursor()	
	cur.execute("""SELECT "Cause Name", Deaths, Year, State FROM Cause_of_Death WHERE Year= %s AND State = %s;""", (AsIs(query1), (query2)))
	data=cur.fetchall()
	for row in data:
		print(row)
	conn.commit()

query_table(query1, query2)




