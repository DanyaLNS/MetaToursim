from pyowm import OWM
from pyowm.utils.config import get_default_config

def get_current_weather(place):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM('adf16c0648b3158457a35940e55b5fef')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    w = observation.weather
    return {
        'Статус' : str(w.detailed_status),
        'Температура' : str(w.temperature('celsius')['temp']),
        'Влажность' : str(w.humidity),
        'Скорость ветра' : str(w.wind()['speed'])
    }