from typing import Any

import allure
import pytest
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование принятия заказа')
class TestCreateOrder:
    @allure.sub_suite('Тестирование успешного создания заказа')
    @allure.title('Проверка того, что можно указать один из цветов / оба цвета / '
                  'ни одного из цветов')
    @allure.description('Выполняем POST запрос /api/v1/orders с указанием неоходимого набора '
                        'данных c различными вариациями выбора цветов. Ожидаем "track" в теле '
                        'ответа')
    @pytest.mark.parametrize('color', [['BLACK'],
                                       ['GREY'],
                                       ['BLACK', 'GREY'],
                                       []])
    def test_create_order_with_different_color_status_code_is_created(self,
                                                                      order_data: dict[str, Any],
                                                                      color: str) -> None:
        order_data['color'] = color
        response = requests.post(url=Entrypoints.orders,
                                 data=order_data)

        assert response.status_code == 201 and 'track' in response.json()
