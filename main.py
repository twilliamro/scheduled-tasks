import os
import requests
from datetime import datetime, timezone
from timezonefinder import TimezoneFinder
import pytz
from twilio.rest import Client

# ##With Secrets
# # #for Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
# # for weather information
API_key = os.environ.get("API_key")
MY_LAT = os.environ.get("MY_LAT")
MY_LONG = os.environ.get("MY_LONG")

# Optional: Add validation
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN]):
    raise ValueError("Missing required Twilio environment variables")
    

#FindTimezone from Coordinates
tf = TimezoneFinder()
timezone_str = tf.timezone_at(lat=MY_LAT, lng=MY_LONG)
print(f"Timezone: {timezone_str}")
# Create timezone OBJECT from the string
timezone_obj = pytz.timezone(timezone_str)

parameters = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":API_key,
    "units": "metric",
    "cnt": 8,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()

# if id < 700: bring_umbrela: data['list'][0-3]['weather'][0]['id']
for i, forecast in enumerate(data['list']):
    weather_id = forecast['weather'][0]["id"]
    if weather_id < 700:
        weather_main = forecast['weather'][0]["main"]
        dt_txt = forecast['dt_txt']

        # Convert dt_txt to UTC datetime
        utc_dt = datetime.fromisoformat(dt_txt)
        utc_dt = pytz.UTC.localize(utc_dt)

        #convert to local time usein timezoe object
        local_dt = utc_dt.astimezone(timezone_obj)
        #Call strftime() on the datetime object, NOT on the string
        formatted_time = local_dt.strftime('%d/%m/%Y %H:%M:%S')

        print(f"Take a Umbrela!!! at {formatted_time}, Weather: {weather_main}  ID= {weather_id}")

#get complete weather forecast for timezone_str and present in timezone_str timezone
sms_short_message = []
for i, forecast in enumerate(data['list']):
    temp_min = forecast['main']["temp_min"]
    temp_max = forecast['main']["temp_max"]
    weather_main = forecast['weather'][0]["main"]
    weather_id = forecast['weather'][0]["id"]
    dt_txt = forecast['dt_txt']

    # Convert dt_txt to UTC datetime
    utc_dt = datetime.fromisoformat(dt_txt)
    utc_dt = pytz.UTC.localize(utc_dt)

    # ✅ Convert to local time using timezone OBJECT
    local_dt = utc_dt.astimezone(timezone_obj)

    # ✅ Call strftime() on the datetime object
    formatted_time = local_dt.strftime('%d/%m/%Y %H:%M:%S')
    print(f"At {formatted_time}, Temperature: from {temp_min} to {temp_max}, Weather {weather_main}  ID= {weather_id}")

    sms_short_message.append(f"At {formatted_time},{temp_min}oC to {temp_max}oC, {weather_main}")
sms_short_weather_forecast = "\n".join(sms_short_message)
print(sms_short_weather_forecast)


# send an SMS with the weather prediction (message) with twilio
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
print(TWILIO_ACCOUNT_SID)
print(TWILIO_AUTH_TOKEN)
print(TWILIO_PHONE_NUMBER)
print(MY_PHONE_NUMBER)
# message = client.messages.create(
#     from_=TWILIO_PHONE_NUMBER,
#     body=sms_short_weather_forecast,
#     to=MY_PHONE_NUMBER,
# )

# print(message.status)
