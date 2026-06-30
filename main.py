import data
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(0)

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

    def _prepare_flow_for_taxi_and_comfort(self):
        self.page.click_taxi_option()
        self.page.click_comfort_icon()
        assert self.page.is_comfort_active()
        self.page.wait_until_phone_step_ready()

    def test_set_route(self):
        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO

    def test_select_comfort(self):
        self._prepare_flow_for_taxi_and_comfort()
        assert self.page.is_comfort_active()

    def test_fill_phone_number(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_phone(data.PHONE_NUMBER)
        assert self.page.get_inserted_phone_value() == data.PHONE_NUMBER

    def test_fill_card(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.get_current_payment_method() != ""

    def test_comment_for_driver(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_comment(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.order_blanket_and_handkerchiefs()
        assert self.page.is_blanket_and_handkerchiefs_checked()

    def test_order_2_ice_creams(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.order_2_ice_creams()
        assert self.page.get_current_icecream_amount() == 2

    def test_car_search_model_appears(self):
        self._prepare_flow_for_taxi_and_comfort()
        self.page.fill_comment(data.MESSAGE_FOR_DRIVER)
        self.page.click_order_button()
        assert self.page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()