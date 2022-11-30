from datetime import datetime, timedelta

from odoo.tests import HttpCase, tagged

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

APP_MAIN_MENU_XMLID = "opa.menu_main"
TIMEOUT = 60


@tagged("post_install", "-at_install")
class TestOpaSelenium(HttpCase):

    def _get_app_button(self, xmlid: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, f"a[data-menu-xmlid='{xmlid}'][role='option']")

    def _get_menuitem(self, xmlid: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, f"a[data-menu-xmlid='{xmlid}'][role='menuitem']")

    def setUp(self):
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=webdriver.ChromeOptions())
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.get("http://172.17.0.1:8069/web/login")
        self.driver.find_element(By.ID, "login").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        self._get_app_button(APP_MAIN_MENU_XMLID).click()

    def test_app_menu_name(self):
        """Ensure the module's name is  displayed correctly on the navigation bar."""
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, f".o_menu_brand[data-menu-xmlid='{APP_MAIN_MENU_XMLID}']").text,
            "Open Academy"
        )

    def test_session_on_calendar(self):
        """Ensure that created sessions show on the dashboard's calendar."""
        session_title = "Random Test Session"

        self._get_menuitem("opa.menu_sessions").click()
        self.driver.find_element(By.CSS_SELECTOR, ".o_list_button_add").click()
        WebDriverWait(self.driver, TIMEOUT).until(expected_conditions.visibility_of_element_located((By.NAME, "title")))
        self.driver.find_element(By.NAME, "title").send_keys(session_title)

        course_fld = self.driver.find_element(By.XPATH, "//div[@name=\'course_id\']//input")
        course_fld.click()
        course_fld.send_keys("How to program Odoo")

        date = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
        starts_fld = self.driver.find_element(By.CSS_SELECTOR, "input[name='starts_on']")
        starts_fld.send_keys(date)

        ends_fld = self.driver.find_element(By.CSS_SELECTOR, "input[name='ends_on']")
        ends_fld.send_keys(date)

        self.driver.find_element(By.CSS_SELECTOR, "button.o_form_button_save").click()
        self._get_menuitem("opa.menu_dashboard").click()

        self.driver.find_element(
            By.XPATH, f"//div[contains(text(), '{session_title}') and contains(@class, 'event_title')]"
        )

    def tearDown(self) -> None:
        self.driver.quit()
