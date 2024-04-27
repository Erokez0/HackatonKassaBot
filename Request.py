import httpx
from random import randint
from Keys import secretKey, sbpMerchantId


def reg_test_qr() -> dict:
    data = {"amount": 1987, "currency": "RUB", f"order": f"1-32-{randint(100, 999)}", "qrType": "QRDynamic",
            "sbpMerchantId": sbpMerchantId}
    r = httpx.post('https://pay-test.raif.ru/api/sbp/v2/qrs',
                   headers={'Content-Type': 'application/json', 'secretKey': secretKey},
                   json=data)
    return r.json()
def get_qr_status(qrid: str) -> str: # noqa
    """
    В первой строке при реальном запуске ссылка меняется, без теста
    :param qrid: qrId, идентификатор QR-кода, номер заказа
    :return: Статус заказа, QR-кода
    """
    get_data = httpx.get(f'https://pay-test.raif.ru/api/sbp/v2/qrs/{qrid}', # noqa
                         headers={'Authorization': f'Bearer {secretKey}'}) # noqa
    datadict: dict = get_data.json()
    return datadict.get('qrStatus')
