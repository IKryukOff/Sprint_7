import allure
import pytest
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование создания курьера')
class TestCreateCourier:
    @allure.sub_suite('Тестирование успешного создания курьера')
    @allure.title('Проверка того, что успешный запрос возвращает {{"ok": true}}')
    @allure.description('Выполняем POST запрос /api/v1/courier с указанием необходимых data '
                        'параметров (логин, пароль, имя)')
    def test_create_courier_status_code_is_created(self, courier_data: dict[str, str]) -> None:
        response = requests.post(url=Entrypoints.courier,
                                 data=courier_data)

        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.sub_suite('Тестирование возврата ошибки при некорректном запросе создания курьера')
    @allure.title('Проверка того, что нельзя создать двух одинаковых курьеров')
    @allure.description('Выполняем POST запрос /api/v1/courier с указанием необходимых data '
                        'параметров (логин, пароль, имя) ДВАЖДЫ. При втором запросе получаем '
                        'ожидаемую ошибку')
    def test_create_courier_with_same_data_status_code_is_conflict(
            self,
            courier_data: dict[str, str]) -> None:
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        response = requests.post(url=Entrypoints.courier,
                                 data=courier_data)

        assert (response.status_code == 409 and
                'Этот логин уже используется' in response.json()['message'])

    @allure.sub_suite('Тестирование возврата ошибки при некорректном запросе создания курьера')
    @allure.title('Проверка необходмости передачи всех обязательные полей')
    @allure.description('Выполняем POST запрос /api/v1/courier без указания логина, пароля или '
                        'имени ожидаем ошибку отсутствия необходимых данных')
    @pytest.mark.parametrize('exclude_data_field', ['login', 'password', 'firstName'])
    def test_create_courier_without_some_data_status_code_is_bad_request(
            self,
            courier_data: dict[str, str],
            exclude_data_field: str) -> None:
        courier_data.pop(exclude_data_field)
        response = requests.post(url=Entrypoints.courier,
                                 data=courier_data)

        assert response.status_code == 400 and 'Недостаточно данных' in response.json()['message']
