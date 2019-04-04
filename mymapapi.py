# coding:utf-8
from PIL import Image
import requests

def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={0}&format=json".format(address)
    
    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return toponym[0]["GeoObject"] if toponym else None


# Получаем координаты объекта по его адресу.
def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return (None,None)
    
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)

def get_spn(address):
    toponym = geocode(address)
    if not toponym:
        return(None, None)
    toponym_coords = toponym["Point"]["pos"]
    #Долгота longitude   широта lattitute
    toponym_lon, toponym_lat = toponym_coords.split(" ")
    ll = ",".join([toponym_lon, toponym_lat])
    #рамка
    envelope = toponym["boundedBy"]["Envelope"]
    x1,y1 = envelope["lowerCorner"].split(" ")
    x2,y2 = envelope["upperCorner"].split(" ")
    dx = abs(float(x1) - float(x2)) / 2.0
    dy = abs(float(y1) - float(y2)) / 2.0
    spn = "{0},{1}".format(dx, dy)
    return (ll, spn)

#Поиск организации
def find_org(ll, spn, request, locale="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
    "apikey": api_key,
    "text": request,
    "lang": locale,
    "ll": ll,
    "spn:" :spn,
    "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))

    # Получаем первую найденную организацию.
    
    organization = json_response["features"][0]
    return organization


def get_file_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = "http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}".format(**locals())
    else:
        map_request = "http://static-maps.yandex.ru/1.x/?l={map_type}".format(**locals())

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Error request")
        return None
    
    #Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Error write map_file")
        return None

    im = Image.open(map_file)
    rgb_im = im.convert('RGB')
    rgb_im.save("res.png")
    return "res.png"