import allure
import pytest
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование логина курьера')
class TestLoginCourier:
    @allure.sub_suite('Тестирование успешного логина курьера')
    @allure.title('Проверка того, что успешный запрос id курьера')
    @allure.description('Выполняем POST запрос /api/v1/courier/login с указанием логина и пароля '
                        'в качестве data параметров. Предварительно создаем курьера')
    def test_login_courier_status_code_is_ok(self, courier_data: dict[str, str]) -> None:
        # создаем курьера для последующего логина
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        courier_data.pop('firstName')
        response = requests.post(url=Entrypoints.courier_login,
                                 data=courier_data)

        assert response.status_code == 200 and 'id' in response.json()

    @allure.sub_suite('Тестирование возврата ошибки при некорректном логине курьера')
    @allure.title('Проверка того, что система вернёт ошибку, если неправильно указать логин '
                  'или пароль курьера')
    @allure.description('Выполняем POST запрос /api/v1/courier/login с указанием неверное '
                        'значения логина и пароля в качестве data параметров. Предварительно '
                        'создаем курьера')
    @pytest.mark.parametrize('incorrect_data_field', ['login', 'password'])
    def test_login_courier_with_incorrect_data_status_code_is_not_found(
            self,
            courier_data: dict[str, str],
            incorrect_data_field: str) -> None:
        # создаем курьера для последующего логина
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        courier_data.pop('firstName')
        courier_data[incorrect_data_field] = 'incorrect_data_value'
        response = requests.post(url=Entrypoints.courier_login,
                                 data=courier_data)

        assert (response.status_code == 404 and
                'Учетная запись не найдена' in response.json()['message'])

    @allure.sub_suite('Тестирование возврата ошибки при некорректном логине курьера')
    @allure.title('Проверка того, что для авторизации нужно передать все обязательные поля')
    @allure.description('Выполняем POST запрос /api/v1/courier/login с отсутствующим значение '
                        'логина или пароля. Предварительно создаем курьера')
    @pytest.mark.parametrize('exclude_data_field', ['login', 'password'])
    def test_login_courier_without_some_data_status_code_is_bad_request(
            self,
            courier_data: dict[str, str],
            exclude_data_field: str) -> None:
        # создаем курьера для последующего логина
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        courier_data.pop('firstName')
        courier_data.pop(exclude_data_field)
        response = requests.post(url=Entrypoints.courier_login,
                                 data=courier_data)

        assert (response.status_code == 400 and
                'Недостаточно данных для входа' in response.json()['message'])
