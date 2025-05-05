from typing import Any

import allure
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование получения заказа по его номеру')
class TestGetOrder:
    @allure.sub_suite('Тестирование успешного получения заказа')
    @allure.title('Проверка того, что успешный запрос возвращает объект с заказом')
    @allure.description('Выполняем GET запрос /api/v1/orders/track/ с указанием id заказа в '
                        'качестве query параметра. Предварительно создаем заказ')
    def test_get_order_status_code_is_ok(self, order_data: dict[str, Any]) -> None:
        # создаем заказ для получения информации о нем далее
        create_response = requests.post(url=Entrypoints.orders,
                                        data=order_data)
        order_id = create_response.json()['track']
        response = requests.get(url=Entrypoints.orders_track,
                                params={'t': order_id})

        assert response.status_code == 200 and 'order' in response.json()

    @allure.sub_suite('Тестирование возврата ошибки при некорректном запросе получения заказа')
    @allure.title('Проверка того, запрос без номера заказа возвращает ошибку')
    @allure.description('Выполняем GET запрос /api/v1/orders/track/ без указания id заказа в '
                        'качестве query параметра')
    def test_get_order_without_track_status_code_is_bad_request(self) -> None:
        response = requests.get(url=Entrypoints.orders_track)

        assert (response.status_code == 400 and
                'Недостаточно данных для поиска' in response.json()['message'])

    @allure.sub_suite('Тестирование возврата ошибки при некорректном запросе получения заказа')
    @allure.title('Проверка того, запрос с несуществующим заказом возвращает ошибку')
    @allure.description('Выполняем GET запрос /api/v1/orders/track/ с указанием неверного id '
                        'заказа в качестве query параметра. Предварительно создаем заказ')
    def test_get_order_with_incorrect_track_status_code_is_not_found(
            self, order_data: dict[str, Any]) -> None:
        # создаем заказ для получения информации о нем далее
        create_response = requests.post(url=Entrypoints.orders,
                                        data=order_data)
        order_id = int(create_response.json()['track'])
        response = requests.get(url=Entrypoints.orders_track,
                                params={'t': order_id + 100})

        assert response.status_code == 404 and 'Заказ не найден' in response.json()['message']
