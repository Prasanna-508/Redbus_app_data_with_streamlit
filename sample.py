import streamlit as st
import sqlalchemy


conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from redbus_data_of_10states;', ttl=600)



routes_names_list = df['route_name'].unique().tolist()
bus_type_list = df['bus_type'].unique().tolist()






with st.form("form1"):
    st.header("Red Bus Data")
    

    option1 = st.selectbox("select the Route Name:",routes_names_list)
    option2 = st.selectbox("select the bus type",("SEETER","SLEEPER"))
    option3 = st.selectbox("select AC type",("A.C","NON.AC"))
    option4 =st.selectbox("select the rating",("1.5 - 2.5","2.5 - 3.0","3.0-4.5","4.5-5"))
    #option5 = st.selectbox("starting time",("04:30 - 06:00","06:00 -08:00","08:00-10:00","10:00-12:00","12:00 - 14:00","14:00-16:00","16:00-18:00","18:00-20:00","20:00-22:00","22:00 - 23:30","23:30 - 3:00","3:00 - 4:30"),)
    option6 = st.selectbox("Bus Fare Range",("140-350","350-500","500-800","800-1000","1000-1200","1200-1500","1500 - 2000","2000-5000","5000-10000"))

    submitted = st.form_submit_button(label = "Submit", use_container_width= False)

if submitted:
    
    bustype = '%' + option2 + '%'
    rate1,rate2=option4.split('-')
    #time1,time2 = option5.split('-')
    price1,price2 = option6.split('-')
    st.write(option1,bustype,rate1,rate2,price1,price2)
    if option3 == 'NON.AC':
        type1,type2 = option3.split('.')
        type3 = '%' + type1 + '%' + type2 + '%'
        st.write(type3)
        df1 = conn.query('SELECT * FROM redbus_data_of_10states where route_name = "'+option1+'" and (upper(bus_type) like "'+bustype+'" and upper(bus_type) like "'+type3+'") and (star_rating between '+rate1+' and ' +rate2+') and (price between '+price1+' and '+price2+');') 
    else:
        type3 = '%NON%A%C%'
        st.write(type3)
        df1 = conn.query('SELECT * FROM redbus_data_of_10states where route_name = "'+option1+'" and (upper(bus_type) like "'+bustype+'" and upper(bus_type) not like "'+type3+'") and (star_rating between '+rate1+' and ' +rate2+') and (price between '+price1+' and '+price2+');')

        
    st.dataframe(df1)
 
else:
    st.dataframe(df)