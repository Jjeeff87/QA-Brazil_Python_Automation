import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage



class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.driver.get(data.URBAN_ROUTES_URL)


    def test_set_route(self):
        page = UrbanRoutesPage(self.__class__.driver)
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)


    def test_select_comfort(self):
     pass

    def test_fill_phone_number(self):
     pass


    def test_fill_card(self):
          pass

    def test_comment_for_driver(self):
        page = UrbanRoutesPage(self.__class__.driver)
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.fill_comment(data.MESSAGE_FOR_DRIVER)


    def test_order_blanket_and_handkerchiefs(self):
        pass

    def test_order_2_ice_creams(self):
       pass

    def test_car_search_model_appears(self):
        # Adicionar em S8
        pass

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

