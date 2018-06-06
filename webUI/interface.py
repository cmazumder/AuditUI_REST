from urlparse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from setup_File import Env_variable as config_variable


class Interface:
    driver = None

    def __init__(self, url):
        # self.driver = webdriver.Ie()
        self.driver = webdriver.Firefox()
        self.driver.get(url)

    def navigate_to_url(self, url):
        self.driver.get(url)

    # def get_ui_value_xpath(self, path):
    #     try:
    #         if self.driver.find_element_by_xpath(xpath=path):
    #             return self.driver.find_element_by_xpath(xpath=path).text
    #         else:
    #
    #             return self.driver.find_element_by_xpath(xpath=path).text
    #     except Exception as E:
    #         print E.msg

    def get_ui_value_xpath(self, path):
        self.wait_for_page_load(path)
        try:
            return self.driver.find_element_by_xpath(xpath=path).text
        except Exception as E:
            print E.message

    def wait_for_angular(self, selenium_driver):
        selenium_driver.set_script_timeout(10)
        selenium_driver.execute_async_script("""
            callback = arguments[arguments.length - 1];
            angular.element('html').injector().get('$browser').notifyWhenNoOutstandingRequests(callback);""")

    def wait_for_page_load(self, page_element):
        # wait = WebDriverWait(self.driver, 20)
        # wait.until(EC.visibility_of_element_located((By.XPATH, page_element)))
        # wait.until(EC.visibility_of_element_located())
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, page_element)))
        except Exception as E:
            print E.message

    def __del__(self):
        self.driver.quit()


def main():
    url_dashboad = urljoin(config_variable.get("ApiURL_root"), 'AuditUI/home')

    audit_ui_test = Interface(url_dashboad)

    path = r'//controllerdetail-partial/div/table/tbody/tr[1]/td[2]'
    x = audit_ui_test.get_ui_value_xpath(path=path)
    print x
    path = r'//controllerdetail-partial/div/table/tbody/tr[2]/td[2]'
    print audit_ui_test.get_ui_value_xpath(path=path)

    url_dashboad = urljoin(config_variable.get("ApiURL_root"), 'AuditUI/egminfo')

    audit_ui_test.navigate_to_url(url=url_dashboad)
    path = r'//datatable-body-cell/div/div/div[2]/div/div/div/div[2]/div[2]'
    print audit_ui_test.get_ui_value_xpath(path)


if __name__ == "__main__":
    main()
