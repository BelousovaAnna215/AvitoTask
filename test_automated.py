import os
import time
import pytest
from playwright.sync_api import sync_playwright

URL = "https://www.avito.ru/avito-care/eco-impact"
URL_LOGIN = "https://www.avito.ru/#login?authsrc=h"

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        yield browser
        browser.close()


# Проверка загрузки страницы
def test_url_availability(browser):
    page = browser.new_page()
    page.goto(URL)
    assert page.url == URL, "Expected URL"


# Проверка входа пользователя с корректными данными
def test_user_login(browser):
    username = input("Введите логин (телефон или почта): ")
    password = input("Введите пароль: ")
    page = browser.new_page()
    page.goto(URL_LOGIN)
    time.sleep(5)
    page.fill('input[name="login"]', username)
    page.fill('input[name="password"]', password)
    page.click('span.css-1kdcmzd', button='left')
    time.sleep(5)
    code = input("Введите проверочный код: ")
    page.fill('input[name="code"]', code)
    page.click('span.css-1kdcmzd:has-text("Подтвердить")', button='left')
    time.sleep(5)
    new_elem = 'a.index-module-nav-link-YtJag.index-module-profile-AWXhu'
    element = page.query_selector(new_elem)
    assert element, "authorization failed"


# Сохранение снимков счетчиков
def test_screenshot(browser):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    page = browser.new_page()
    page.goto(URL)
    time.sleep(3)

    elements = page.query_selector_all(".desktop-impact-item-eeQO3")
    assert len(elements) >= 6, "Not enough elements found on the page."

    num = 1
    for i in range(6):
        if i % 2 == 0:
            continue
        element = elements[i]
        screenshot_path = f"{output_dir}/screenshot{num}.png"
        element.screenshot(path=screenshot_path)
        assert os.path.exists(screenshot_path), "Screenshot was not saved."
        num += 1
