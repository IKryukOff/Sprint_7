from typing import Any

import allure
import pytest
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование принятия заказа')
class TestAcceptOrder:
    @allure.sub_suite('Тестирование успешного принятия заказа')
    @allure.title('Проверка того, что успешный запрос возвращает {{"ok":true}}')
    @allure.description('Выполняем PUT запрос /api/v1/orders/accept/ с указанием id заказа в '
                        'качестве path параметра и id курьера в качестве query параметра. '
                        'Предварительно создаем заказ и курьера')
    def test_accept_order_status_code_is_ok(self, order_data: dict[str, Any],
                                            courier_data: dict[str, str]) -> None:
        # создаем заказ и получаем его id
        order_response = requests.post(url=Entrypoints.orders,
                                       data=order_data)
        track_id = int(order_response.json()['track'])
        track_response = requests.get(url=Entrypoints.orders_track,
                                      params={'t': track_id})
        order_id = int(track_response.json()['order']['id'])
        # создаем УЗ курьера и получаем его id
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        courier_data.pop('firstName')
        login_response = requests.post(url=Entrypoints.courier_login,
                                       data=courier_data)
        courier_id = int(login_response.json()['id'])
        # принимаем заказ с указанием необходимых параметров
        response = requests.put(url=f'{Entrypoints.orders_accept}/{order_id}',
                                params={'courierId': courier_id})

        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.sub_suite('Тестирование возврата ошибки при некорректном принятия заказа')
    @allure.title('Проверка возврата ошибки если не передать id курьера')
    @allure.description('Выполняем PUT запрос /api/v1/orders/accept/ с указанием id заказа в '
                        'качестве path параметра и без указания id курьера в качестве query '
                        'параметра. Предварительно создаем заказ')
    def test_accept_order_without_courier_id_status_code_is_conflict(
            self, order_data: dict[str, Any]) -> None:
        # создаем заказ и получаем его id
        order_response = requests.post(url=Entrypoints.orders,
                                       data=order_data)
        track_id = int(order_response.json()['track'])
        track_response = requests.get(url=Entrypoints.orders_track,
                                      params={'t': track_id})
        order_id = int(track_response.json()['order']['id'])
        # принимаем заказ без указания id курьера
        response = requests.put(url=f'{Entrypoints.orders_accept}/{order_id}')

        assert (response.status_code == 400 and
                'Недостаточно данных для поиска' in response.json()['message'])

    @allure.sub_suite('Тестирование возврата ошибки при некорректном принятия заказа')
    @allure.title('Проверка возврата ошибки если передать неверный id заказа или курьера')
    @allure.description('Выполняем PUT запрос /api/v1/orders/accept/ с указанием неверного id '
                        'заказа в качестве path параметра или неверного id курьера в качестве '
                        'query параметра. Предварительно создаем заказ и курьера')
    @pytest.mark.parametrize('incorrect_id_object,message',
                             [['order', 'Заказа с таким id не существует'],
                              ['courier', 'Курьера с таким id не существует']])
    def test_accept_order_with_incorect_id_status_code_is_not_found(
            self, order_data: dict[str, Any],
            courier_data: dict[str, str],
            incorrect_id_object: str,
            message: str) -> None:
        # создаем заказ и получаем его id
        order_response = requests.post(url=Entrypoints.orders,
                                       data=order_data)
        track_id = int(order_response.json()['track'])
        track_response = requests.get(url=Entrypoints.orders_track,
                                      params={'t': track_id})
        order_id = int(track_response.json()['order']['id'])
        # создаем УЗ курьера и получаем его id
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        courier_data.pop('firstName')
        login_response = requests.post(url=Entrypoints.courier_login,
                                       data=courier_data)
        courier_id = int(login_response.json()['id'])
        # изменяем id на некорректное значение
        if incorrect_id_object == 'order':
            order_id += 100
        elif incorrect_id_object == 'courier':
            courier_id += 100
        # принимаем заказ с указанием необходимых некорректных параметров
        response = requests.put(url=f'{Entrypoints.orders_accept}/{order_id}',
                                params={'courierId': courier_id})

        assert (response.status_code == 404 and
                message in response.json()['message'])
