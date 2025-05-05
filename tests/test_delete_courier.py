import allure
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование удаления курьера')
class TestDeleteCourier:
    @allure.sub_suite('Тестирование успешного удаления курьера')
    @allure.title('Проверка того, что успешный запрос возвращает {{"ok":true}}')
    @allure.description('Выполняем DELETE запрос /api/v1/courier/ с указанием id курьера в '
                        'качестве path параметра. Предварительно создаем курьера')
    def test_delete_courier_status_code_is_ok(self, courier_data: dict[str, str]) -> None:
        # создаем курьера
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        # получаем id курьера
        courier_data.pop('firstName')
        login_response = requests.post(url=Entrypoints.courier_login,
                                       data=courier_data)
        courier_id = int(login_response.json()['id'])
        # удаляем курьера по его id
        response = requests.delete(url=f'{Entrypoints.courier}/{courier_id}')

        assert response.status_code == 200 and response.json() == {"ok": True}

    @allure.sub_suite('Тестирование возврата ошибки при некорректном удалении курьера')
    @allure.title('Проверка возврата ошибки если передать неверный id курьера')
    @allure.description('Выполняем DELETE запрос /api/v1/courier/ с указанием неверного id курьера '
                        'в качестве path параметра. Предварительно создаем курьера')
    def test_delete_courier_with_incorrect_id_status_code_is_not_found(
            self, courier_data: dict[str, str]) -> None:
        # создаем курьера
        requests.post(url=Entrypoints.courier,
                      data=courier_data)
        # получаем id курьера
        courier_data.pop('firstName')
        login_response = requests.post(url=Entrypoints.courier_login,
                                       data=courier_data)
        courier_id = int(login_response.json()['id'])
        # удаляем курьера по его id (некорректному)
        response = requests.delete(url=f'{Entrypoints.courier}/{courier_id + 100}')

        assert (response.status_code == 404 and
                'Курьера с таким id нет' in response.json()['message'])
