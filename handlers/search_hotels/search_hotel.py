import requests
import json
import os
from typing import Iterable, List, Union, Callable
from dotenv import load_dotenv
from datetime import datetime
from googletrans import Translator
from telebot.types import InputMediaPhoto
from icecream import ic

load_dotenv()


def search_region(city: str) -> List:
	"""
	Функция, для поиска регионов по заданному пункту назначение.

	:param city: [str] - пункту назначение, вводится пользователем.
	:return: [list[dict]] - список, со словарями внутри (название региона: ID региона).
	"""
	ic()
	dict_region = list()
	translator = Translator()
	querystring = {"q": city}

	headers = {
		"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	url = "https://hotels4.p.rapidapi.com/locations/v3/search"
	response = requests.get(url, headers=headers, params=querystring)
	ic(response)
	if response.status_code == requests.codes.ok:
		city_info = json.loads(response.text)
		if len(city_info.get('sr')) > 0:
			for dict_object in city_info.get('sr'):
				if dict_object.get('type') == 'CITY' or dict_object.get('type') == 'NEIGHBORHOOD':
					name_region = dict_object.get('regionNames').get('displayName')
					id_region = dict_object.get('gaiaId')
					result = translator.translate(name_region, dest='ru')
					dict_region.append({result.text: id_region})

	return dict_region


def search_info(id_region: str, count: Union[int, str], sort: str, start_data: str, end_data: str,
				list_dist: list = None, max_price: int = 150, min_price: int = 1, foto: str = None,
				amount_foto: str = 0) -> Union[Iterable, Callable]:
	"""
	Функция-поисковик, по переданным данным из хандлеров выполняет поиск нужной информации.
	:param id_region: Индитифакатор региона пребывания
	:param count: Кол-во отелей.
	:param sort: Сортировка (по цене, по удалённости от центра или количества гостей)
	:param list_dist: Список сгенерированный из диапазона расстояний введённый пользователем
	:param max_price: Максимальная цена
	:param min_price: Минимальная цена
	:param start_data: Начало бронирования.
	:param end_data: Окончание бронирования.
	:param foto: Показывать фото или нет.
	:param amount_foto: Кол-во фото.
	:return: [str] - Возвращает в хандлер текст с найденной информацией.
	"""
	ic()
	ic(id_region)

	in_date = datetime.strptime(start_data, '%d-%m-%Y')
	out_date = datetime.strptime(end_data, '%d-%m-%Y')
	diff_date = out_date - in_date
	amount_hotels = int(count)
	hotel_id = str()
	hotel_name = str()
	hotel_location = str()
	hotel_price = str()
	list_url_foto = list()
	hotels_found: int = 0

	try:
		payload = {
			"currency": "USD",
			"eapid": 1,
			"locale": "en_US",
			"siteId": 300000001,
			"destination": {"regionId": id_region},
			"checkInDate": {
				"day": in_date.day,
				"month": in_date.month,
				"year": in_date.year
			},
			"checkOutDate": {
				"day": out_date.day,
				"month": out_date.month,
				"year": out_date.year
			},
			"rooms": [
				{
					"adults": 2
				}
			],
			"resultsStartingIndex": 0,
			"resultsSize": 200,
			"sort": sort,
			"filters": {"price": {
				"max": max_price,
				"min": min_price
			}}
		}
		headers = {
			"content-type": "application/json",
			"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
			"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
		}
		url = "https://hotels4.p.rapidapi.com/properties/v2/list"
		search_hotels = requests.post(url, json=payload, headers=headers)
		ic(search_hotels)
		if search_hotels.status_code == requests.codes.ok:
			all_hotels = json.loads(search_hotels.text)
			len_list_hotels = len(all_hotels.get('data').get('propertySearch').get('properties'))
			if 'errors' in all_hotels.keys():
				raise AttributeError
			if len_list_hotels >= amount_hotels:
				index = 0
				while hotels_found < amount_hotels:
					if list_dist is not None:
						flag = True
						while flag:
							hotel_info_dist = all_hotels.get('data').get('propertySearch').get('properties')[index]
							distance = hotel_info_dist.get('destinationInfo').get('distanceFromDestination').get('value')
							if int(distance) in list_dist:
								hotel_id = hotel_info_dist.get('id')
								hotel_name = hotel_info_dist.get('name')
								hotel_location = hotel_info_dist.get('destinationInfo').get(
									'distanceFromDestination').get('value')
								hotel_price = hotel_info_dist.get('price').get('lead').get('amount')
								flag = False
								index += 1
							else:
								index += 1

					else:
						hotel_info = all_hotels.get('data').get('propertySearch').get('properties')[index]
						hotel_id = hotel_info.get('id')
						hotel_name = hotel_info.get('name')
						hotel_location = hotel_info.get('destinationInfo').get('distanceFromDestination').get('value')
						hotel_price = hotel_info.get('price').get('lead').get('amount')
						index += 1

					payload = {
						"currency": "USD",
						"eapid": 1,
						"locale": "en_US",
						"siteId": 300000001,
						"propertyId": hotel_id
					}
					headers = {
						"content-type": "application/json",
						"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
						"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
					}
					url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
					search_hotels_info = requests.post(url, json=payload, headers=headers)
					ic(search_hotels_info)
					if search_hotels_info.status_code == requests.codes.ok:
						hotels_info = json.loads(search_hotels_info.text)
						hotel_address = hotels_info.get('data').get('propertyInfo').get('summary') \
							.get('location').get('address').get('addressLine')

						total_cost = int(hotel_price) * diff_date.days

						text = f'\U0001F4C4\nНазвание отеля: {hotel_name}\nАдрес: {hotel_address}' \
							f'\nРасстояние до центра: {hotel_location} ml ' \
							f'\nЦена за ночь: {int(hotel_price)} \U0001F4B0' \
							f'\nПроживание на {diff_date.days} ночи(-ей), составит: {total_cost} \U0001F4B0'

						if foto is not None:
							num_foto = 0
							while num_foto < int(amount_foto):
								hotel_foto = hotels_info.get('data').get('propertyInfo').get('propertyGallery') \
									.get('images')[num_foto].get('image').get('url')
								list_url_foto.append(InputMediaPhoto(media=hotel_foto))
								num_foto += 1

							hotels_found += 1
							yield list_url_foto, text
							list_url_foto.clear()

						else:
							hotels_found += 1
							yield text
					else:
						raise IndexError
			else:
				yield f'К сожалению, отелей нашлось только {len_list_hotels} \U0001F612\n'
				new_func = search_info(id_region=id_region, count=len_list_hotels, sort=sort, start_data=start_data,
										end_data=end_data, list_dist=list_dist, max_price=max_price, min_price=min_price,
										foto=foto, amount_foto=amount_foto)
				for elem in new_func:
					yield elem
		else:
			raise IndexError

	except AttributeError:
		yield 'Не получилось обработать запрос \U0001F612\n' \
				'Пожалуйста, попробуйте снова.'
	except IndexError:
		yield 'Сервер не отвечает \U0001F612\n' \
			'Пожалуйста, попробуйте снова.'
