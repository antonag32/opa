from odoo.tests import HttpCase, tagged

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

APP_MAIN_MENU_XMLID = "opa.menu_main"


@tagged("post_install", "-at_install")
class TestOpaSelenium(HttpCase):

    def _get_app_button(self, xmlid: str) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, f"a[data-menu-xmlid='{xmlid}'][role='option']")

    def setUp(self):
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=webdriver.ChromeOptions())
        self.driver.implicitly_wait(60)
        self.driver.get("http://172.17.0.1:8069/web/login")
        self.driver.find_element(By.ID, "login").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

    def test_app_menu_name(self):
        self._get_app_button(APP_MAIN_MENU_XMLID).click()
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, f".o_menu_brand[data-menu-xmlid='{APP_MAIN_MENU_XMLID}']").text,
            "Open Academy"
        )

    def tearDown(self) -> None:
        self.driver.quit()
