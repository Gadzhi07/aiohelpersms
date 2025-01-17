import asyncio
import aiohttp
import platform

from typing import Dict, Optional

if platform.system() == "Windows":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class HelperSMSError(Exception):
	pass


class HelperSMS:
	path_prefix = "https://api.helper20sms.ru"


	def __init__(self, api_key: str) -> None:
		"""__init__
		Args:
			api_key (str): HelperSMS api key
		"""
		self.__headers = {
			"api-key": api_key,
		}	
	
	
	async def get_balance(self) -> Dict:
		"""Получить информацию о балансе
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"balance": 20.22
				}
			}
		"""
		method = "GET"
		path = "/api/balance"
		return await self._request(method, path)


	async def get_countries(self) -> Dict:
		"""Получить список стран
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Россия"
					}
				]
			}
		"""
		method = "GET"
		path = "/api/countries"
		return await self._request(method, path)


	async def get_services(self, country_id: int):
		"""Получить список сервисов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 6104,
						"name": "Вконтакте"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise HelperSMSError("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/services/{country_id}"
		return await self._request(method, path)


	async def get_operators(self, country_id: int):
		"""Получить список операторов определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					"mtt",
					"megafon",
					"beeline"
				]
			}
		"""
		if not isinstance(country_id, int):
			raise HelperSMSError("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/operators/{country_id}"
		return await self._request(method, path)

	
	async def get_price(
		self,
		service_id: int,
		reorder_ability: Optional[bool] = False,
	) -> Dict:
		"""Получить цену СМС для сервиса
		Args:
			service_id (int): Айди сервиса
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise HelperSMSError("Argument service_id must be an integer")
		if not isinstance(reorder_ability, bool):
			raise HelperSMSError("Argument reorder_ability must be an boolean")

		method = "GET"
		path = f"/api/price/{service_id}"
		data = {
			'reorder_ability': reorder_ability
		}

		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return await self._request(method, path, data)



	async def get_number(
		self,
		service_id: int,
		operator_code: Optional[str] = 'any',
		reorder_ability: Optional[bool] = False,
		max_price: Optional[int] = 0,
	) -> Dict:
		"""Купить номер для получения СМС
		Args:
			service_id (int): Айди сервиса
			operator_code: (Optional[str], optional): Код оператора. Default value: any
			reorder_ability (Optional[bool], optional): Возможность повторной покупки номера после конца аренды. Default value: false
			max_price (Optional[int], optional): Максимальная цена. Default value: 0
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise HelperSMSError("Argument service_id must be an integer")
		if not isinstance(operator_code, str):
			raise HelperSMSError("Argument operator_code must be an string")
		if not isinstance(reorder_ability, bool):
			raise HelperSMSError("Argument reorder_ability must be an boolean")
		if not isinstance(max_price, int):
			raise HelperSMSError("Argument max_price must be an integer")

		method = "POST"
		path = "/api/number"
		data = {
			'service_id': service_id,
			'operator_code': operator_code,
			'reorder_ability': reorder_ability,
			'max_price': max_price
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]
		
		return await self._request(method, path, data)


	
	async def set_order_status(
		self,
		order_id: int,
		status: str
	) -> Dict:
		"""Изменить статус для заказа
		Args:
			order_id (int): Номер заказа
			status: (str): Статус заказа. Допустимые значения: CANCEL, FINISH
		Returns:
			Dict: {
				"status": true
			}
		"""
		if not isinstance(order_id, int):
			raise HelperSMSError("Argument order_id must be an integer")
		if not isinstance(status, str):
			raise HelperSMSError("Argument status must be an string")

		method = "POST"
		path = "/api/order_status"
		data = {
			'order_id': order_id,
			'status': status,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return await self._request(method, path, data)



	async def get_codes(
		self,
		order_id: int,
	) -> Dict:
		"""Получить список полученных кодов для номера
		Args:
			order_id (int): Номер заказа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"codes":
					[
						"5423",
						"125423",
						"4158"
					]
				}
			}
		"""
		if not isinstance(order_id, int):
			raise HelperSMSError("Argument order_id must be an integer")

		method = "GET"
		path = f"/api/codes/{order_id}"

		return await self._request(method, path)
	


	async def get_rent_services(
		self,
		country_id: int,
	) -> Dict:
		"""Получить список сервисов для аренды определённой страны
		Args:
			country_id (int): Айди страны
		Returns:
			Dict: {
				"status": true,
				"data":
				[
					{
						"id": 1,
						"name": "Alibaba"
					}
				]
			}
		"""
		if not isinstance(country_id, int):
			raise HelperSMSError("Argument country_id must be an integer")

		method = "GET"
		path = f"/api/rent_services/{country_id}"

		return await self._request(method, path)



	async def get_rent_price(
		self,
		service_id : int,
		rent_time: int,
	) -> Dict:
		"""Получить цену аренды для сервиса
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"price": 20.04,
					"service": "vk"
				}
			}
		"""
		if not isinstance(service_id, int):
			raise HelperSMSError("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise HelperSMSError("Argument rent_time must be an integer")

		method = "GET"
		path = f"/api/rent_price/{service_id}/{rent_time}"

		return await self._request(method, path)



	async def get_rent_number(
		self,
		service_id : int,
		rent_time: int,
		operator_code: Optional[str] = 'any',
	) -> Dict:
		"""Купить номер для аренды
		Args:
			service_id (int): Айди сервиса
			rent_time (int): Период аренды номера. Минимум 4 часа
			operator_code: (Optional[str], optional): Код оператора. Default value: any
		Returns:
			Dict: {
				"status": true,
				"data":
				{
					"order_id": 1,
					"number": "79851478547",
					"service": "vk",
					"price": 20.22
				}
			}
		"""
		if not isinstance(service_id, int):
			raise HelperSMSError("Argument service_id must be an integer")
		if not isinstance(rent_time, int):
			raise HelperSMSError("Argument rent_time must be an integer")
		if not isinstance(operator_code, str):
			raise HelperSMSError("Argument operator_code must be an string")

		method = "POST"
		path = "/api/rent_number"
		data = {
			'service_id': service_id,
			'rent_time': rent_time,
			'operator_code': operator_code,
		}
		for key, value in data.copy().items():
			if value is None:
				del data[key]

		return await self._request(method, path, data)

	async def _request(self, method: str, path: str, data: dict = {}) -> Dict:
		url = self.path_prefix + path

		async with aiohttp.ClientSession() as session:
			async with session.request(
				method, url, headers=self.__headers, json=data
			) as response:
				result = await response.json()
				if isinstance(result, dict) and 'detail' in result:
					raise HelperSMSError(result)
				else:
					return result
