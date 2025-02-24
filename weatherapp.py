#weather app
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget): #class will inherit from parent of QWidget
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                           font-family: calibri;
                           }
                           QLabel#city_label{
                           font-size: 40px;
                           font-style: italic;
                           }
                           QLineEdit#city_input{
                           font-size: 40px;
                           }
                           QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight: bold;
                           }
                           QLabel#temperature_label{
                           font-size: 75px;
                           }
                           QLabel#emoji_label{
                           font-size: 100px;
                           font-family: Segoe UI emoji;
                           }
                           QLabel#description_label{
                           font-size: 50px
                           }
            """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        
        api_key = "bd3b97685964a915dbf147662896c57a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        #put our dangerous code (code that may cause an exception) in this block
        try:
            response = requests.get(url) #pass in our url into the get method of the requests module
            response.raise_for_status()#raises an exception if there is an http error (not done automatically)
            data = response.json() #convert data to readable data

            #if our data object at key "cod" is the value 200, display weather
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:nNo response from the server")
                case _:
                    self.display_error(f"HTTP Error Occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            print("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout Error\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too Many Redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k*9/5)-459.67
        weather_id = data["weather"][0]["id"]
        #fetching data, at key 'weather', value is in a list but a list of only 1 item
        #index 0 fetches the one item, then at the key of 'description', we'll get our
        #weather description
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.01f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description.capitalize()}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 504:
            return "🌦️"
        elif 530 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 511:
            return "❄️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id == 801:
            return "⛅"
        elif 802<= weather_id <= 804:
            return "☁️"
        else:
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = WeatherApp() #construct our object
    weatherApp.show()
    sys.exit(app.exec_())