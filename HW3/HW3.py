import openmeteo_requests
import datetime

class IncreaseSpeed():
  def __init__(self, current_speed=0, max_speed=0):
    
    self.c_speed = current_speed
    self.m_speed = max_speed

  def __iter__(self):
    return self 
  
  def __next__(self):
    self.c_speed += 10
    if self.c_speed < self.m_speed:
      return self.c_speed
    else: 
      print(self.m_speed)
      raise StopIteration
    
class DecreaseSpeed():

  def __init__(self, current_speed=0, min_speed=0):
    self.c_speed = current_speed
    self.m_speed = min_speed

  def __iter__(self):
    return self
  
  def __next__(self):
    self.c_speed -= 10
    if self.c_speed > self.m_speed:
      return self.c_speed
    else: 
      print(self.m_speed)
      raise StopIteration




class Car(IncreaseSpeed, DecreaseSpeed):
  
  total_car=0

  def __init__(self, max_speed: int, current_speed=0, on_a_road=True):
    Car.total_car = Car.total_car+1
    self.max_speed= max_speed
    self.c_speed = current_speed
    self.on_a_road = on_a_road

    

    IncreaseSpeed().__init__()
    DecreaseSpeed().__init__()

    

  def accelerate(self, upper_border=None):
    # check for state 
    self.border = upper_border
    if self.on_a_road:
      if self.border is not None and self.border > self.c_speed and self.border <= self.max_speed:

        speed_up = IncreaseSpeed(self.c_speed, self.border)

        for c in speed_up:
          print(c)

        self.c_speed = self.border

      else:

        if self.border is None or self.c_speed <= self.max_speed or self.border > self.max_speed:
          if (self.max_speed - self.c_speed) >= 10:
            self.c_speed += 10
            print(self.c_speed)
          else:
            self.c_speed = self.max_speed
            print(self.c_speed)
        else:
          print("The car cannot accelerate")  
    else:
      print("The car is parked!")

  def brake(self, lower_border=None):
    self.border = lower_border
    if self.on_a_road:
      if self.border is not None and self.border < self.c_speed and self.border >= 0:


        speed_down = DecreaseSpeed(self.c_speed, self.border)

        
        for c in speed_down:
          print(c)

        self.c_speed = self.border

      else:

        if (self.border is None or self.border < 0 or self.border > self.c_speed) and self.c_speed > 0:
          if self.c_speed >= 10:
            self.c_speed -= 10
            print(self.c_speed)
          else:
            self.c_speed = 0
            print(self.c_speed)
        else:
          print("The car have already stopped!")  
    else:
      print("The car is parked!")

# yourself: which one is regular, which is static and which is classmethod

  def parking(self):
    if self.on_a_road:
      
      self.brake(0)
      self.on_a_road = False
      print("The car is parked")
      Car.total_car -= 1
      
    else:
      print("The car has already been parked!")



  @classmethod
  def total_cars(cls):
    print("The number of cars on the road: ", cls.total_car)

  @staticmethod
  def show_weather():
    
    openmeteo = openmeteo_requests.Client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    "latitude": 59.9386, # for St.Petersburg
    "longitude": 30.3141, # for St.Petersburg
    "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
    "wind_speed_unit": "ms",
    "timezone": "Europe/Moscow"
    }

    response = openmeteo.weather_api(url, params=params)[0]

    # The order of variables needs to be the same as requested in params->current!
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_rain = current.Variables(2).Value()
    current_wind_speed_10m = current.Variables(3).Value()

    print(f"Current time: {datetime.date.fromtimestamp(current.Time()+response.UtcOffsetSeconds())} {response.TimezoneAbbreviation().decode()}")
    print(f"Current temperature: {round(current_temperature_2m, 0)} C")
    print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
    print(f"Current rain: {current_rain} mm")
    print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")
