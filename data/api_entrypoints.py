SERVICE_BASE_URL = 'https://qa-scooter.praktikum-services.ru'
SERVICE_API_URL = f'{SERVICE_BASE_URL}/api/v1'


class Entrypoints:
    courier = f'{SERVICE_API_URL}/courier'
    courier_login = f'{SERVICE_API_URL}/courier/login'
    orders = f'{SERVICE_API_URL}/orders'
    orders_track = f'{SERVICE_API_URL}/orders/track'
    orders_accept = f'{SERVICE_API_URL}/orders/accept'
