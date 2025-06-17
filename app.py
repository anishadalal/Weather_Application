from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '8e46bc59840cc39120ffa82743648d8c'  # Replace with your API key

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    forecast = []

    if request.method == 'POST':
        city = request.form['city'].strip()

        # Current weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        current_res = requests.get(current_url)

        # Forecast weather
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_res = requests.get(forecast_url)

        if current_res.status_code == 200 and forecast_res.status_code == 200:
            data = current_res.json()
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'icon': data['weather'][0]['icon']
            }

            forecast_data = forecast_res.json()
            dates_added = set()
            for entry in forecast_data['list']:
                date, time = entry['dt_txt'].split(' ')
                if time == "12:00:00" and date not in dates_added:
                    forecast.append({
                        'date': date,
                        'temp': entry['main']['temp'],
                        'desc': entry['weather'][0]['description'],
                        'icon': entry['weather'][0]['icon']
                    })
                    dates_added.add(date)
                if len(forecast) == 5:
                    break
        else:
            weather['error'] = "City not found or API error."

    return render_template('index.html', weather=weather, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)
