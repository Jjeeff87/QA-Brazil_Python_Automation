from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(., 'Chamar um táxi')]")
    COMFORT_TARIFF = (By.XPATH, "(//button[contains(@class, 'tcard-i')])[5]")
    PHONE_FIELD = (By.ID, "phone")
    CARD_NUMBER = (By.ID, "number")
    CARD_CODE = (By.ID, "code")
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_SWITCH = (By.XPATH, "//span[@class='slider round']")
    ICE_CREAM_PLUS = (By.CLASS_NAME, "counter-plus")


    def __init__(self, driver):
        self.driver = driver

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.FROM_FIELD).send_keys(address_from)
        self.driver.find_element(*self.TO_FIELD).send_keys(address_to)

    def call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_comfort(self):
        comfort = Select(self.driver.find_element(*self.COMFORT_TARIFF))
        self.driver.execute_script("arguments[0].click();", comfort)

    def fill_phone(self, phone):
        self.driver.find_element(*self.PHONE_FIELD).click()
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)

    def open_phone_modal(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def fill_card(self, number, code):
        self.driver.find_element(*self.CARD_NUMBER).send_keys(number)
        self.driver.find_element(*self.CARD_CODE).send_keys(code)

    def fill_comment(self, comment):
        self.driver.find_element(*self.COMMENT_FIELD).send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_SWITCH).click()

    def order_2_ice_creams(self):
        for _ in range(2):
            self.driver.find_element(*self.ICE_CREAM_PLUS).click()





