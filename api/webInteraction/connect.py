from selenium import webdriver


class ConnectAuditUI:
    browser = None

    def __init__(self, url):
        self.browser = webdriver.Ie()
        self.browser.get(url)

    def get_ui_value(self, path):
        return self.browser.find_element_by_xpath(xpath=path).text


def main():
    url = r'http://172.26.18.110/AuditUI/home'
    path = r'//html/body/app/div/div/my-index/div/section/div[1]/div[1]/controllerdetail-partial/div/table/tbody/tr[1]/td[2]'
    audit_ui_test = ConnectAuditUI(url=url)
    x = audit_ui_test.get_ui_value(path=path)
    print x


if __name__ == "__main__":
    main()
