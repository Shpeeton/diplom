import allure
import pytest
from pages.main_page import MainPage
from data.test_data import CardData


@allure.feature("Оплата тура")
class TestPayment:

    @allure.story("Обычная оплата")
    @allure.title("Успешная оплата")
    def test_success_payment(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        assert page.success(), "Уведомление об успехе не появилось"
        status = db.get_payment_status()
        assert status == 'APPROVED', f"Статус в БД: {status}, ожидался APPROVED"

    @allure.story("Обычная оплата")
    @allure.title("Отказ в оплате")
    def test_declined_payment(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.DECLINED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        assert not page.success(), "Уведомление об успехе не должно появиться для отклоненной карты"
        status = db.get_payment_status()
        assert status == 'DECLINED', f"Статус в БД: {status}, ожидался DECLINED"

    @allure.story("Обычная оплата")
    @allure.title("Отправка пустой формы")
    def test_empty_form(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.submit()

        error_card = page.get_field_error("card")
        error_month = page.get_field_error("month")
        error_year = page.get_field_error("year")
        error_owner = page.get_field_error("owner")
        error_cvc = page.get_field_error("cvc")

        assert "Неверный формат" in error_card, f"Для карты ожидалось 'Неверный формат', получено '{error_card}'"
        assert "Неверный формат" in error_month, f"Для месяца ожидалось 'Неверный формат', получено '{error_month}'"
        assert "Неверный формат" in error_year, f"Для года ожидалось 'Неверный формат', получено '{error_year}'"
        assert "Поле обязательно для заполнения" in error_owner, f"Для владельца ожидалось 'Поле обязательно для заполнения', получено '{error_owner}'"
        assert "Поле обязательно для заполнения" in error_cvc, f"Для CVC ожидалось 'Поле обязательно для заполнения', получено '{error_cvc}'"

        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный номер карты (15 цифр)")
    def test_invalid_card_number(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.INVALID_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        error = page.get_field_error("card")
        assert "Неверный формат" in error, f"Ожидалось 'Неверный формат', получено '{error}'"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный месяц (13)")
    def test_invalid_month_13(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.INVALID_MONTH_13)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        error = page.get_field_error("month")
        assert "Неверно указан срок действия карты" in error, f"Ожидалось 'Неверно указан срок действия карты', получено '{error}'"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный месяц (00)")
    def test_invalid_month_00(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.INVALID_MONTH_00)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        assert page.error(), "Уведомление об ошибке не появилось"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный год (прошлый)")
    def test_invalid_year_past(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.INVALID_YEAR_PAST)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        error = page.get_field_error("year")
        assert "Истёк срок действия карты" in error, f"Ожидалось 'Истёк срок действия карты', получено '{error}'"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный месяц (00)")
    def test_invalid_month_00(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.INVALID_MONTH_00)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        assert not page.success(), "Уведомление об успехе не должно появиться"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Невалидный CVC (2 цифры)")
    def test_invalid_cvc_short(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.VALID_OWNER)
        page.fill_cvc(CardData.INVALID_CVC_SHORT)
        page.submit()

        error = page.get_field_error("cvc")
        assert "Неверный формат" in error, f"Ожидалась ошибка CVC, получено '{error}'"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Пустое поле владельца")
    def test_empty_owner(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.INVALID_OWNER_EMPTY)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        error = page.get_field_error("owner")
        assert "Поле обязательно для заполнения" in error, f"Ожидалось 'Поле обязательно для заполнения', получено '{error}'"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"

    @allure.story("Обычная оплата")
    @allure.title("Владелец с цифрами")
    def test_owner_with_numbers(self, driver, db_and_url):
        db, app_url = db_and_url
        page = MainPage(driver, app_url).open().buy()
        page.fill_card(CardData.APPROVED_CARD)
        page.fill_month(CardData.VALID_MONTH)
        page.fill_year(CardData.VALID_YEAR)
        page.fill_owner(CardData.INVALID_OWNER_NUMBERS)
        page.fill_cvc(CardData.VALID_CVC)
        page.submit()

        assert not page.success(), "Уведомление об успехе не должно появиться"
        status = db.get_payment_status()
        assert status is None, "Запись не должна создаваться в БД"