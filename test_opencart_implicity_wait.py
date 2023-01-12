import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(10)
url = 'https://demo.opencart.com/'


def test_explict_wait_iphone():
    """В этом тесте всплывающее уведомление о добавлении в корзину принудительно закрывается, сразу после закрытия
    проверяется отсутствие элемента уведомления"""
    driver.get(url)
    driver.maximize_window()
    title = driver.title
    assert title == "Your Store"
    iphone_page_mini = driver.find_element(By.XPATH, '//a[contains(text(),"iPhone")]')
    iphone_page_mini.click()
    title_iphone = driver.title
    assert title_iphone == "iPhone"
    add_to_cart_button = driver.find_element(By.ID, 'button-cart')
    add_to_cart_button.click()
    alert_close = driver.find_element(By.CLASS_NAME, "btn-close")
    alert_close.click()
    alert = driver.find_elements(By.XPATH, "//*[@class='fas fa-check-circle']")  # Так как прописано неявное
    # ожидаение, вебдрайвер ждёт элемент 10 секунд
    assert len(alert) == 0


def test_explict_wait_samsung_syncmaster():
    """В этом тесте всплывающее уведомление о добавлении в корзину принудительно не закрывается, поэтому прописан sleep
        после которого проверяется отсутствие элемента уведомления в DOM дереве"""
    driver.get(url)
    driver.maximize_window()
    title = driver.title
    assert title == "Your Store"
    time.sleep(2)  # sleep нужен что бы успел отрендерится блок с категориями товаров
    element_menu_to_hover_over = driver.find_element(By.XPATH, '//a[contains(text(),"Components")]')
    hover = ActionChains(driver).move_to_element(element_menu_to_hover_over)
    hover.perform()
    monitor_in_menu = driver.find_element(By.XPATH, '//a[contains(text(),"Monitors")]')
    monitor_in_menu.click()
    title_iphone = driver.title
    assert title_iphone == "Monitors"
    sync_master_card = driver.find_element(By.XPATH, '//a[contains(text(),"SyncMaster")]')
    sync_master_card.click()
    add_to_cart_button = driver.find_element(By.ID, 'button-cart')
    add_to_cart_button.click()
    time.sleep(10)  # Ждём 10 секунд, после них элемента уведомления гарантированно не должно быть в DOM дереве
    alert = driver.find_elements(By.XPATH, "//*[@class='fas fa-check-circle']")
    assert len(alert) == 0
