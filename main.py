import data
import pytest
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

        # Melhor evitar implicitly_wait "alto" e preferir esperas explícitas no Page Object
        cls.driver.implicitly_wait(0)
        cls.driver.get(data.URBAN_ROUTES_URL)

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        # Coloca o fluxo no início (definindo origem/destino)
        self.page._enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

    def _prepare_flow_for_taxi_and_comfort(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()

        # Assert mais direto (evita comparação is True)
        assert self.page.click_comfort_active()

        # Espera pelo passo do telefone (como você comentou: não existe id="phone" nesse step do HTML)
        self.page.wait_until_phone_step_ready()

    def test_set_route(self):
        assert self.page._get_from_location() == data.ADDRESS_FROM
        assert self.page._get_to_location() == data.ADDRESS_TO

    def test_select_method(self):
        self._prepare_flow_for_taxi_and_comfort()

    def test_select_comfort(self):
        self._prepare_flow_for_taxi_and_comfort()

    def test_fill_phone_number(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_phone(data.PHONE_NUMBER)

    def test_fill_card(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_comment_for_driver(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_comment(data.MESSAGE_FOR_DRIVER)

    def test_order_blanket_and_handkerchiefs(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.order_blanket_and_handkerchiefs()

    def test_order_2_ice_creams(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.order_2_ice_creams()

    def test_car_search_model_appears(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.open_phone_modal()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()