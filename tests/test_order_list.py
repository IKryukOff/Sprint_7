import allure
import requests
from data.api_entrypoints import Entrypoints


@allure.parent_suite('Тестирование API сервиса заказа самоката')
@allure.suite('Тестирование получения списка заказов')
class TestOrderList:
    @allure.sub_suite('Тестирование успешного получения списка заказов')
    @allure.title('Проверка того, что успешный запрос возвращает "orders" со списком заказов')
    @allure.description('Выполняем GET запрос /api/v1/orders')
    def test_get_order_list_status_code_is_ok_with_orders(self) -> None:
        response = requests.get(url=Entrypoints.orders)

        assert response.status_code == 200 and 'orders' in response.json()
