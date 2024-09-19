
import mysql.connector
from mysql.connector import errorcode



cnx = mysql.connector.connect(user = "root",host = "localhost",password ="Savithri@508",database = "redbus_data")
cursor = cnx.cursor()
query = "CREATE TABLE redbus_data_of_10states(id int not null AUTO_INCREMENT primary key,route_name varchar(100),route_url varchar(100),bus_name varchar(100),bus_type varchar(100),departure_time time,arrival_time time,duration varchar(20),price int,star_rating float,seat_availability int)"
try:
    cursor.execute(query)
except mysql.connector.ProgrammingError as err:
  if err.errno == errorcode.ER_SYNTAX_ERROR:
    print("Check your syntax!")
  else:
    print("Error: {}".format(err))


cursor.close()
cnx.close()