from selenium.common import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.by import By


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ========== locators (HTML que você mandou) ==========
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    CALL_TAXI_BUTTON = (By.XPATH, "//button[normalize-space()='Chamar um táxi' or contains(.,'Chamar um táxi')]")

    # Comfort cards (no seu HTML: button[data-for='tariff-card-4'])
    COMFORT_BUTTON = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    COMFORT_ACTIVE = (
        By.XPATH,
        "//div[contains(@class,'tcard') and contains(@class,'active')]//div[@class='tcard-title' and normalize-space()='Comfort']",
    )

    # Step do pedido (no HTML aparece #comment)
    COMMENT_FIELD = (By.ID, "comment")
    PHONE_STEP_BUTTON = (
        By.XPATH,
        "//*[contains(@class,'np-button') and .//div[normalize-space()='Número de telefone']]",
    )

    PHONE_INPUT_FALLBACK = [
        (By.XPATH, "//*[normalize-space()='Número de telefone']/ancestor::form//input[not(@id='comment')][1]"),
        (By.XPATH, "//*[contains(@class,'form')]//input[not(@id='comment')][1]"),
        (By.CSS_SELECTOR, "input.input:not(#comment)"),
    ]
    # Telefone: o HTML não mostrou id=phone; então usamos fallback tel input
    PHONE_STEP_TITLE = (By.XPATH, "//*[normalize-space()='Número de telefone']")

    PHONE_INPUT_FALLBACK = [
        (By.XPATH,
         "//*[normalize-space()='Número de telefone']/ancestor::*[contains(@class,'form')][1]//input[not(@id='comment')]"),
        (By.XPATH, "//*[normalize-space()='Número de telefone']/following::input[not(@id='comment')][1]"),
        (By.CSS_SELECTOR, "input:not(#comment)"),
    ]

    CARD_CVV_INPUT = (By.ID, "code")
    # número do cartão: geralmente também é card-input, mas sem id garantido
    CARD_NUMBER_FALLBACK = [
        (By.CSS_SELECTOR, "input.card-input:not(#code)"),
        (By.XPATH, "//input[contains(@class,'card-input') and @id!='code']"),
        (By.CSS_SELECTOR, "input.card-input"),
    ]

    ADD_CARD_BUTTON = (By.XPATH, "//button[normalize-space()='Adicionar' or normalize-space()='Add']")

    REQUISITES_HEADER = (
        By.XPATH,
        "//*[contains(@class,'reqs-head') and contains(.,'Requisitos do pedido') or "
        "contains(@class,'reqs-header') and contains(.,'Requisitos do pedido')]"
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

    # Modal de busca de carro (busca aparece após pedido)
    CAR_SEARCH_MODAL = (
        By.XPATH,
        "//*[contains(.,'Busca') or contains(.,'car search') or contains(.,'Car search') or contains(@class,'car') or contains(@class,'cars')]",
    )

    ETA_IN_MODAL = (
        By.XPATH,
        "//*[contains(@class,'eta') or contains(.,'min') or contains(.,'minutos')][1]"
    )

    ORDER_HEADER_TITLE = (By.CSS_SELECTOR, ".order-header-title")

    class UrbanRoutesPage:
        ORDER_HEADER_TITLE = (By.CSS_SELECTOR, ".order-header-title")

    # ========== helpers ==========
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

    def _clear_and_type(self, el, text):
        try:
            el.clear()
        except Exception:
            self.driver.execute_script("arguments[0].value = '';", el)
        el.send_keys(text)

    def _type_first_locator(self, locators, text):
                overlay = (By.CSS_SELECTOR, "div.overlay")
                try:
                    self.wait.until(EC.invisibility_of_element_located(overlay))
                except Exception:
                    pass

                def input_enabled(d):
                    try:
                        e = d.find_element(*loc)
                        return e.is_enabled() and e.is_displayed()
                    except Exception:
                        return False

                self.wait.until(input_enabled)
                return

    # ========== main.py: endereços ==========
    def _enter_locations(self, from_text, to_text):
        # remove e digita
        from_el = self.wait.until(EC.presence_of_element_located(self.FROM_FIELD))
        self._scroll_into_view(from_el)
        self._clear_and_type(from_el, from_text)

        to_el = self.wait.until(EC.presence_of_element_located(self.TO_FIELD))
        self._scroll_into_view(to_el)
        self._clear_and_type(to_el, to_text)

    def _get_value(self, locator):
        return self._find(locator).get_attribute("value")

    def _get_from_location(self):
        return self._get_value(self.FROM_FIELD)

    def _get_to_location(self):
        return self._get_value(self.TO_FIELD)

    # ========== main.py: fluxo ==========
    def click_taxi_option(self):
        self._click(self.CALL_TAXI_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.COMMENT_WRAPPER))
        self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))

    def click_comfort_icon(self):
        self._click(self.COMFORT_BUTTON)

    def click_comfort_active(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.COMFORT_ACTIVE))
            return True
        except TimeoutException:
            return False

    def _clear_and_type(self, el, text: str):
        # tenta normal primeiro (se funcionar)
        try:
            el.clear()
            el.send_keys(text)
            return
        except Exception:
            pass

        # fallback: setar via JS + eventos
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

    def open_phone_step(self):
        btn = self.wait.until(EC.presence_of_element_located(self.PHONE_STEP_BUTTON))

        overlay = (By.CSS_SELECTOR, "div.overlay")
        try:
            self.wait.until(EC.invisibility_of_element_located(overlay))
        except Exception:
            pass

        self._scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)

        # espera o step/título (ou qualquer coisa do step) aparecer
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Número de telefone']")))

    def fill_phone(self, phone_number):
        el = self.wait_until_phone_step_ready()

        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].focus();", el)

        self._clear_and_type(el, phone_number)

    def wait_until_phone_step_ready(self):
        # Espera aparecer qualquer input (exceto #comment)
        loc_any_input = (By.CSS_SELECTOR, "input:not(#comment)")
        el = self.wait.until(EC.presence_of_element_located(loc_any_input))
        self._scroll_into_view(el)

        # retorna o input encontrado
        return el



    def open_phone_modal(self):
        # em muitos fluxos, isso equivale a voltar/confirmar o taxi novamente
        self.click_taxi_option()

    def fill_card(self, card_number, card_code):
        # 1) number
        number_input = self.wait.until(EC.presence_of_element_located((By.ID, "number")))
        self._scroll_into_view(number_input)
        self.driver.execute_script("arguments[0].click();", number_input)

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];

            input.focus();
            input.value = value;

            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));

            // eventos de teclado para acionar validações que dependem de key events
            input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true, key: '1' }));
            input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true, key: '1' }));
            """,
            number_input, card_number
        )

        # TAB do number para que a UI "avance" e valide
        try:
            number_input.send_keys("\ue00d")
        except Exception:
            pass

        # 2) code
        code_input = self.wait.until(EC.presence_of_element_located((By.ID, "code")))
        self._scroll_into_view(code_input)
        self.driver.execute_script("arguments[0].click();", code_input)

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
            code_input, card_code
        )

        # finaliza (blur/tab) para habilitar o botão
        try:
            code_input.send_keys("\ue00d")
        except Exception:
            pass

        self.driver.execute_script("arguments[0].blur();", code_input)

        # deixa o front recalcular (muito comum em validação)
        self.driver.implicitly_wait(0)
        import time
        time.sleep(0.8)

        # 3) tenta esperar habilitar, mas com fallback de clique mesmo assim
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

    def _wait_any_visible(self, locators):
                last_exc = None
                for loc in locators:
                    try:
                        el = self.wait.until(EC.presence_of_element_located(loc))
                        self._scroll_into_view(el)
                        self.wait.until(EC.visibility_of_element_located(loc))
                        return el
                    except Exception as e:
                        last_exc = e
                raise TimeoutException("Nenhum dos locators do fallback ficou visível.") from last_exc

    def fill_comment(self, comment):
            self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.COMMENT_FIELD))
            el = self._find(self.COMMENT_FIELD)
            self._scroll_into_view(el)
            self._clear_and_type(el, comment)

    REQUISITES_HEADER = (By.XPATH, "//*[contains(@class,'reqs-head') and contains(.,'Requisitos do pedido')]")

    def order_blanket_and_handkerchiefs(self):
        self.wait.until(EC.presence_of_element_located(self.REQUISITES_HEADER))
        sw = self.wait.until(EC.presence_of_element_located(self.BLANKET_SWITCH))
        self._scroll_into_view(sw)

        self.driver.execute_script("arguments[0].click();", sw)

        self.wait.until(EC.presence_of_element_located(self.BLANKET_SWITCH_ASSERT))

    def order_2_ice_creams(self):
            plus = self.wait.until(EC.presence_of_element_located(self.ICE_CREAM_PLUS))
            self._scroll_into_view(plus)
            for _ in range(2):
                self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS))
                try:
                    plus.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", plus)

    def assert_car_search_model_visible(self):
        self.wait.until(EC.presence_of_element_located(self.CAR_SEARCH_MODAL))
        self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

        # depois que o modal estiver visível, o header/ETA costuma renderizar
        header = self.ORDER_HEADER_TITLE
        self.wait.until(EC.presence_of_element_located(header))


    def click_order_button(self):
        locator = (By.CSS_SELECTOR, ".results-text button.round, .results-text button.button.round, button.round")
        btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(locator))
        btn.click()

    def assert_order_created_eta_exists(self):
        def header_text_ready(d):
            titles = d.find_elements(*self.ORDER_HEADER_TITLE)
            for t in titles:
                txt = (t.text or "").strip().lower()
                if "motorista vai chegar em" in txt and "min" in txt:
                    return txt
            return False

        eta_text = self.wait.until(header_text_ready, "ETA não carregou no modal do pedido")

        assert "motorista vai chegar em" in eta_text
        assert "min" in eta_text