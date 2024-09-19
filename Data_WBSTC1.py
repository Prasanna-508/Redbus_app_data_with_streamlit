from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver = webdriver.Chrome()
# URL to scrape
routes_url = 'https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile'

# Open the routes URL
driver.get(routes_url)
time.sleep(5)

routes_names = []
routes_urls =[]
all_buses =[]
actions = ActionChains(driver)

route_elements = driver.find_elements(By.XPATH,"//a[@class='route']")
for route in route_elements:
    if route not in routes_names:
        routes_names.append(route.text)
for route in route_elements:
    routes_urls.append(route.get_attribute('href'))

def scroll_and_collect():
   
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height




def extract_bus_details(route_name,route_url):
    driver.get(route_url)
    time.sleep(5)
    wait  = WebDriverWait(driver,30)

    try:
        view_buses_button = driver.find_elements(By.XPATH,"//div[@class = 'button']")

        for button in view_buses_button:
            try:
                button.location_once_scrolled_into_view
                actions.move_to_element(button).click().perform()
                time.sleep(5)
            except Exception as e:
                print(f"error occuried while clicking the button: {e}")
                continue
        
        scroll_and_collect()

        bus_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'bus-item')))
        buses =[]
        for bus in bus_items:
            try:
                bus_name = bus.find_element(By.CSS_SELECTOR, "div[class='travels lh-24 f-bold d-color']").text
                bus_type = bus.find_element(By.CSS_SELECTOR, "div[class='bus-type f-12 m-top-16 l-color evBus']").text
                departure_time = bus.find_element(By.CSS_SELECTOR, "div[class='dp-time f-19 d-color f-bold']").text
                arrival_time = bus.find_element(By.CSS_SELECTOR, "div[class='bp-time f-19 d-color disp-Inline']").text
                duration = bus.find_element(By.CSS_SELECTOR, "div[class='dur l-color lh-24']").text
                fare = bus.find_element(By.CSS_SELECTOR, "div[class='fare d-block']").text
                rating = bus.find_element(By.CSS_SELECTOR,"div[class='rating-sec lh-24']").text
                seat_availability = bus.find_element(By.CSS_SELECTOR,"div[class='column-eight w-15 fl']").text
                buses.append({
                'Route_Name': route_name,
                'Route_URL': route_url,
                'Bus_Name': bus_name,
                'Bus_Type': bus_type,
                'Departure_Time': departure_time,
                'Arrival_Time': arrival_time,
                'Duration': duration,
                'Fare': fare,
                'Rating': rating,
                "Seat_Availability" : seat_availability
                
                })
            except Exception as e:
                print(f"Error extracting data for a bus: {e}")
                pass  # Handle the case where some elements might not be found
        return buses
    
    except Exception as e:
        print("no buses found:{e}")


for i in range(len(routes_names)):
    route_name = routes_names[i]
    route_url = routes_urls[i]

    all_buses.extend(extract_bus_details(route_name,route_url))
    


driver.quit()
df = pd.DataFrame(all_buses)

# Print the DataFrame
print(df)

df.to_csv('wbstc_data5.csv', index=False)




