import csv
from datetime import datetime
import pandas as pd
import mysql.connector

now = datetime.now()
formatted_date = now.strftime('%H:%M')

#csv_path = pathlib.Path.cwd() / "tsrtc_data6.csv"
#csv_path = "C:\\Users\\kodal\\OneDrive\\Desktop\\Redbus_data\\tsrtc_data6.csv"
#csv_path1 = "C:\\Users\\kodal\\OneDrive\\Desktop\\Redbus_data\\ksrtc_data6.csv"

df = pd.read_csv('correctData_RSRTC.csv')



cnx = mysql.connector.connect(user = "root",host = "localhost",password ="Savithri@508",database = "redbus_data")
cursor = cnx.cursor()

sql ="insert into redbus_data_of_10states(route_name,route_url,bus_name,bus_type,departure_time,arrival_time,duration,price,star_rating,seat_availability) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"    
for index,row in df.iterrows():

    cursor.execute(sql,(row['Route_Name'],row['Route_URL'],row['Bus_Name'],row['Bus_Type'],row['Departure_Time'],row['Arrival_Time'],row['Duration'],row['Fare'],row['Rating'],row['Seat_Availability']))

cnx.commit()

print(cursor.rowcount)

cursor.close()
cnx.close()
