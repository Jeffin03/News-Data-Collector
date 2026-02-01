# imports
import csv , requests
# gets the data from the api call 
rawData = requests.get('https://api.open-meteo.com/v1/forecast?latitude=12.9719&longitude=77.5937&hourly=temperature_2m&forecast_days=1')
todayData = rawData.json() 

date = todayData.get('hourly').get('time')[1][0:10] # gets the current date 
temperature = todayData.get('hourly').get('temperature_2m') # List of current day's temperature (hourly)
temperature.insert(0,date) # puts the current date at the start of the list

with open('HourlyTemperature.csv', 'a', encoding='UTF8') as f:
     writer = csv.writer(f)
     writer.writerow(temperature) # appends the current day's temperatures

print(todayData)

