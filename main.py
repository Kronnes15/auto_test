import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class DemoblazeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Запускається перед початком всіх тестів
        cls.driver = webdriver.Chrome()
        cls.username = 'testUser'
        cls.password = 'testPassword'
    
    def test_registration(self):
        """Тест на реєстрацію нового користувача"""
        driver = self.driver
        driver.get('https://www.demoblaze.com/')
        
        # Натискання кнопки реєстрації
        driver.find_element(By.ID, 'signin2').click()
        time.sleep(1)

        # Перевіряємо, чи з'явилось модальне вікно для реєстрації
        self.assertTrue(driver.find_element(By.ID, 'sign-username').is_displayed(), 
                        "Поле для введення імені користувача не з'явилося")

        # Вводимо ім'я користувача та пароль
        driver.find_element(By.ID, 'sign-username').send_keys(self.username)
        driver.find_element(By.ID, 'sign-password').send_keys(self.password)
        
        # Натискаємо "Sign up"
        driver.find_element(By.XPATH, '//button[contains(text(),"Sign up")]').click()
        time.sleep(2)
        
        # Перевіряємо, чи з'явилося попередження
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Тест реєстрації пройшов успішно.")
        except:
            self.fail("Помилка: Не з'явилося попередження після реєстрації")

    def test_login(self):
        """Тест на вхід під новим користувачем"""
        driver = self.driver
        driver.get('https://www.demoblaze.com/')
        
        # Натискання кнопки логіну
        driver.find_element(By.ID, 'login2').click()
        time.sleep(1)

        # Перевірка на появу форми логіну
        self.assertTrue(driver.find_element(By.ID, 'loginusername').is_displayed(),
                        "Поле для введення імені користувача при логіні не з'явилося")

        # Введення імені користувача та пароля
        driver.find_element(By.ID, 'loginusername').send_keys(self.username)
        driver.find_element(By.ID, 'loginpassword').send_keys(self.password)
        
        # Натискання кнопки "Log in"
        driver.find_element(By.XPATH, '//button[contains(text(),"Log in")]').click()
        time.sleep(2)

        # Перевірка вітального повідомлення
        try:
            welcome_message = driver.find_element(By.ID, 'nameofuser').text
            self.assertIn(f'Welcome {self.username}', welcome_message, "Логін не пройшов")
            print("Тест логіну пройшов успішно.")
        except:
            self.fail("Помилка: Вітальне повідомлення не з'явилось")

    def test_add_to_cart(self):
        """Тест на додавання товару до кошика після логіну"""
        driver = self.driver
        driver.get('https://www.demoblaze.com/')
        
        # Логін перед додаванням до кошика
        self.test_login()
        
        # Перевіряємо, що користувач залогінений перед додаванням до кошика
        welcome_message = driver.find_element(By.ID, 'nameofuser').text
        self.assertIn(f'Welcome {self.username}', welcome_message, "Користувач не залогінений")
        
        # Додаємо товар "Samsung galaxy s6" до кошика
        driver.find_element(By.LINK_TEXT, 'Samsung galaxy s6').click()
        time.sleep(1)
        
        # Перевіряємо наявність кнопки додавання до кошика
        self.assertTrue(driver.find_element(By.CLASS_NAME, 'btn-success').is_displayed(),
                        "Кнопка додавання до кошика не з'явилася")
        
        # Натискаємо "Add to cart"
        driver.find_element(By.CLASS_NAME, 'btn-success').click()
        time.sleep(2)
        
        # Перевіряємо появу попередження
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Тест додавання до кошика пройшов успішно.")
        except:
            self.fail("Помилка: Не з'явилось попередження після додавання товару до кошика")

    @classmethod
    def tearDownClass(cls):
        # Викликається після завершення всіх тестів
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
