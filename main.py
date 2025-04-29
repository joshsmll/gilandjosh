import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "2394d865ad2e4d4f881130607252904"
API_URL = "http://api.weatherapi.com/v1/current.json"

# Mapping weather conditions to icons
ICON_MAP = {
    "Sunny": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Sun-icon.png",
    "Clear": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Moon-icon.png",
    "Partly cloudy": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Partly-Cloudy-Day-icon.png",
    "Cloudy": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Clouds-icon.png",
    "Overcast": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Overcast-icon.png",
    "Rain": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Rain-icon.png",
    "Snow": "https://icons.iconarchive.com/icons/icons8/windows-8/256/Weather-Snow-icon.png"
}

def get_weather(location):
    params = {
        "key": API_KEY,
        "q": location
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        current = data['current']
        condition = current['condition']['text']
        temp_c = current['temp_c']
        feelslike_c = current['feelslike_c']
        humidity = current['humidity']
        wind_kph = current['wind_kph']

        return {
            "condition": condition,
            "temp_c": temp_c,
            "feelslike_c": feelslike_c,
            "humidity": humidity,
            "wind_kph": wind_kph
        }
    else:
        return None

def fetch_and_display():
    location = entry.get()
    weather = get_weather(location)
    if weather:
        # Update text label
        label_result.config(
            text=(
                f"Condition: {weather['condition']}\n"
                f"Temp: {weather['temp_c']}°C\n"
                f"Feels like: {weather['feelslike_c']}°C\n"
                f"Humidity: {weather['humidity']}%\n"
                f"Wind: {weather['wind_kph']} km/h"
            )
        )

        # Display appropriate weather icon
        icon_url = ICON_MAP.get(weather['condition'], ICON_MAP.get("Cloudy"))
        icon_response = requests.get(icon_url)
        image_data = Image.open(BytesIO(icon_response.content))
        image_data = image_data.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image_data)
        label_icon.config(image=photo)
        label_icon.image = photo
    else:
        label_result.config(text="Could not fetch weather data.")
        label_icon.config(image='')

# GUI Setup
root = tk.Tk()
root.title("Weather Pixel App")
root.geometry("300x350")

entry = tk.Entry(root, width=25)
entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=fetch_and_display)
search_button.pack(pady=5)

label_result = tk.Label(root, text="Enter ZIP or City", justify="left")
label_result.pack(pady=10)

label_icon = tk.Label(root)
label_icon.pack()

root.mainloop()
