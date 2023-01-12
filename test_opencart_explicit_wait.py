from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://demo.opencart.com/'


def test_explict_wait_iphone():
    """В этом тесте всплывающее уведомление о добавлении в корзину принудительно закрывается, поэтому прописан wait
    на отсутствие уведомления в DOM дереве"""
    driver.get(url)
    driver.maximize_window()
    title = driver.title
    assert title == "Your Store"
    iphone_page_mini = driver.find_element(By.XPATH, '//a[contains(text(),"iPhone")]')
    iphone_page_mini.click()
    add_to_card_button_wait = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.ID, 'button-cart'))
    title_iphone = driver.title
    assert title_iphone == "iPhone"
    add_to_cart_button = driver.find_element(By.ID, 'button-cart')
    add_to_cart_button.click()
    alert_add_to_cart = WebDriverWait(driver, timeout=2).until(lambda d: d.find_element(By.XPATH, '//*[@class="fas '
                                                                                                  'fa-check-circle"]'))
    alert_close = driver.find_element(By.CLASS_NAME, "btn-close")
    alert_close.click()
    wait = WebDriverWait(driver, timeout=1)  # Проверяем отсутствие уведомления после закрытия уведомления
    alert_dissapear = wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='fas fa-check-circle']")))


def test_explict_wait_samsung_syncmaster():
    """В этом тесте всплывающее уведомление о добавлении в корзину принудительно не закрывается, поэтому прописан wait
        на отсутствие уведомления в DOM дереве после 10 секунд (примерно за это время уведомление исчезает)"""
    driver.get(url)
    driver.maximize_window()
    title = driver.title
    assert title == "Your Store"
    wait = WebDriverWait(driver, timeout=3)
    menu_load = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[contains(text(),"Components")]')))
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
    alert_add_to_cart = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//*[@class="fas '
                                                                                                  'fa-check-circle"]'))
    wait = WebDriverWait(driver, timeout=10)  # Ждём в течении 10 секнд закрытия уведомления о добавлении в корзину
    alert_dissapear = wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='fas fa-check-circle']")))
