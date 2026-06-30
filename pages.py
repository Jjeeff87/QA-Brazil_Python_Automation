from selenium.common import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ========== locators ==========
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[normalize-space()='Chamar um táxi' or contains(.,'Chamar um táxi')]")

    COMFORT_BUTTON = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    COMFORT_ACTIVE = (
        By.XPATH,
        "//div[contains(@class,'tcard') and contains(@class,'active')]//div[@class='tcard-title' and normalize-space()='Comfort']",
    )

    PHONE_STEP_BUTTON = (
        By.XPATH,
        "//*[contains(@class,'np-button') and .//div[normalize-space()='Número de telefone']]",
    )
    PHONE_STEP_TITLE = (By.XPATH, "//*[normalize-space()='Número de telefone']")
    PHONE_INPUT_ANY = (By.CSS_SELECTOR, "input:not(#comment)")

    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CVV_INPUT = (By.ID, "code")
    ADD_CARD_BUTTON = (By.XPATH, "//button[normalize-space()='Adicionar' or normalize-space()='Add']")
    CURRENT_PAYMENT_METHOD = (By.XPATH, '//div[contains(@class, "pp-value-text")]')

    REQUISITES_HEADER = (
        By.XPATH,
        "//*[contains(@class,'reqs-head') and contains(.,'Requisitos do pedido')]"
    )

    BLANKET_SWITCH = (
        By.XPATH,
        "//div[contains(@class,'r-sw-container')][.//div[contains(@class,'r-sw-label') and contains(.,'Cobertor e lençóis')]]"
        "//input[contains(@class,'switch-input')]"
    )
    BLANKET_SWITCH_ASSERT = (
        By.XPATH,
        "//div[contains(@class,'r-sw-container')]"
        "[.//div[contains(@class,'r-sw-label') and contains(.,'Cobertor e lençóis')]]"
        "[contains(@class,'active') or contains(@class,'on') or contains(@class,'selected') or contains(@class,'checked')]"
    )

    COMMENT_WRAPPER = (By.XPATH,
                        "//div[contains(@style,'margin-top') or contains(@class,'input-container')][.//input[@id='comment']]")
    COMMENT_FIELD = (By.CSS_SELECTOR, "input#comment")

    ICE_CREAM_PLUS = (By.CLASS_NAME, "counter-plus")
    ICE_CREAM_COUNT = (By.CLASS_NAME, "counter-value")

    CAR_SEARCH_MODAL = (
        By.XPATH,
        "//*[contains(.,'Busca') or contains(@class,'car') or contains(@class,'cars')]",
    )
    ORDER_HEADER_TITLE = (By.CSS_SELECTOR, ".order-header-title")
    ORDER_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button.smart-button")

    # ========== helpers privados ==========
    def _scroll_into_view(self, el):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'center'});", el
        )

    def _find(self, locator):
        return self.driver.find_element(*locator)

    def _click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self._scroll_into_view(el)
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            el.click()
        except (TimeoutException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].click();", el)

    def _clear_and_type(self, el, text: str):
        try:
            el.clear()
            el.send_keys(text)
            return
        except Exception:
            pass
        # fallback via JS + eventos, para campos controlados por framework JS
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.focus();
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            el,
            text
        )

    def _get_value(self, locator):
        return self._find(locator).get_attribute("value")

    def _set_value_via_js(self, el, value):
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.focus();
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, key: '1' }));
            input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, key: '1' }));
            """,
            el, value
        )

    # ========== ENDEREÇOS (públicos) ==========
    def enter_locations(self, from_text, to_text):
        from_el = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        self._scroll_into_view(from_el)
        self._clear_and_type(from_el, from_text)

        to_el = self.wait.until(EC.presence_of_element_located(self.TO_FIELD))
        self._scroll_into_view(to_el)
        self._clear_and_type(to_el, to_text)

    def get_from_location(self):
        return self._get_value(self.FROM_FIELD)

    def get_to_location(self):
        return self._get_value(self.TO_FIELD)

    # ========== TÁXI / TARIFA (públicos) ==========
    def click_taxi_option(self):
        self._click(self.CALL_TAXI_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.COMMENT_WRAPPER))
        self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))

    def click_comfort_icon(self):
        self._click(self.COMFORT_BUTTON)

    def is_comfort_active(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.COMFORT_ACTIVE))
            return True
        except TimeoutException:
            return False

    # ========== TELEFONE (públicos) ==========
    def wait_until_phone_step_ready(self):
        el = self.wait.until(EC.presence_of_element_located(self.PHONE_INPUT_ANY))
        self._scroll_into_view(el)
        return el

    def open_phone_step(self):
        btn = self.wait.until(EC.presence_of_element_located(self.PHONE_STEP_BUTTON))
        overlay = (By.CSS_SELECTOR, "div.overlay")
        try:
            self.wait.until(EC.invisibility_of_element_located(overlay))
        except Exception:
            pass
        self._scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.PHONE_STEP_TITLE))

    def fill_phone(self, phone_number):
        el = self.wait_until_phone_step_ready()
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].focus();", el)
        self._clear_and_type(el, phone_number)

    def get_inserted_phone_value(self):
        el = self.wait_until_phone_step_ready()
        return el.get_attribute("value")

    # ========== CARTÃO (públicos) ==========
    def fill_card(self, card_number, card_code):
        number_input = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_INPUT))
        self._scroll_into_view(number_input)
        self.driver.execute_script("arguments[0].click();", number_input)
        self._set_value_via_js(number_input, card_number)
        try:
            number_input.send_keys("\ue00d")
        except Exception:
            pass

        code_input = self.wait.until(EC.presence_of_element_located(self.CARD_CVV_INPUT))
        self._scroll_into_view(code_input)
        self.driver.execute_script("arguments[0].click();", code_input)
        self._set_value_via_js(code_input, card_code)
        try:
            code_input.send_keys("\ue00d")
        except Exception:
            pass
        self.driver.execute_script("arguments[0].blur();", code_input)

        # Em vez de time.sleep fixo, esperamos explicitamente o front recalcular
        # o estado do botão "Adicionar" (até ficar habilitado ou o timeout estourar).
        try:
            def add_button_enabled(d):
                btn = d.find_element(*self.ADD_CARD_BUTTON)
                return btn.is_displayed() and btn.is_enabled() and not btn.get_attribute("disabled")

            self.wait.until(add_button_enabled)
        except TimeoutException:
            pass

        add_btn = self.driver.find_element(*self.ADD_CARD_BUTTON)
        self._scroll_into_view(add_btn)
        try:
            add_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", add_btn)

    def get_current_payment_method(self):
        return self._find(self.CURRENT_PAYMENT_METHOD).text

    # ========== COMENTÁRIO (públicos) ==========
    def fill_comment(self, comment):
        self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.COMMENT_FIELD))
        el = self._find(self.COMMENT_FIELD)
        self._scroll_into_view(el)
        self._clear_and_type(el, comment)

    def get_comment(self):
        return self._get_value(self.COMMENT_FIELD)

    # ========== COBERTOR E LENÇÓIS (públicos) ==========
    def order_blanket_and_handkerchiefs(self):
        self.wait.until(EC.presence_of_element_located(self.REQUISITES_HEADER))
        sw = self.wait.until(EC.presence_of_element_located(self.BLANKET_SWITCH))
        self._scroll_into_view(sw)
        self.driver.execute_script("arguments[0].click();", sw)

    def is_blanket_and_handkerchiefs_checked(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.BLANKET_SWITCH_ASSERT))
            return True
        except TimeoutException:
            return False

    # ========== SORVETES (públicos) ==========
    def order_2_ice_creams(self):
        plus = self.wait.until(EC.presence_of_element_located(self.ICE_CREAM_PLUS))
        self._scroll_into_view(plus)
        for _ in range(2):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS))
            try:
                plus.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", plus)

    def get_current_icecream_amount(self):
        return int(self._find(self.ICE_CREAM_COUNT).text.strip())

    # ========== PEDIDO (públicos) ==========
    def click_order_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON_LOCATOR))
        btn.click()

    def is_car_search_modal_visible(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.CAR_SEARCH_MODAL))
            self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
            self.wait.until(EC.presence_of_element_located(self.ORDER_HEADER_TITLE))
            return True
        except TimeoutException:
            return False