from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

class LoginformTest(LiveServerTestCase):

    def testloginpage(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/login.html')
        time.sleep(8)
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")       
        username_input.send_keys('pavi')
        password_input.send_keys('Pavi@123')
        login_button.send_keys(Keys.RETURN)

        assert 'KSRTC' in driver.page_source





# from django.test import TestCase

# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# class LoginTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://127.0.0.1:8000/login.html")  
#         time.sleep(10)  # Wait for 10 seconds before accessing the URL

#     def test_login_successful(self):
#         username_input = self.driver.find_element(By.ID, "username")
#         password_input = self.driver.find_element(By.ID, "password")
#         login_button = self.driver.find_element(By.XPATH, "//button[text()='Sign In']")       
#         username_input.send_keys("pavi")  
#         password_input.send_keys("Pavi@123")  
#         login_button.click()
#         time.sleep(5)

#         expected_url_after_login = 'http://127.0.0.1:8000/dashboard'  
#         self.assertEqual(self.driver.current_url, expected_url_after_login, "Login failed or unexpected page after login")

#     def tearDown(self):       
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()



#Test1: Login

# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# class searchTest(LiveServerTestCase):

#     def test_search_page(self):
#         driver = webdriver.Chrome()

#         driver.get("http://127.0.0.1:8000/")
#         time.sleep(8)
#         try:
#             # Find and click on the "Bus Details" button from the dashboard
#             bus_details_button = driver.find_element_by_class_name("get-started-btn")
#             bus_details_button.click()
            
#             # Wait for the page to load
#             time.sleep(2)
            
#             # Verify if the page is redirected to the expected URL
#             assert driver.current_url == "http://127.0.0.1:8000/public_bus/"
#             print("Successfully redirected to the Public Bus page.")
            
#             # Find and click on the search icon
#             search_icon = driver.find_element_by_css_selector(".sicon")
#             search_icon.click()
            
#             # Find the source and destination input fields and enter the values
#             source_input = driver.find_element_by_id("sourceInput")
#             source_input.send_keys("champad")
            
#             destination_input = driver.find_element_by_id("destinationInput")
#             destination_input.send_keys("nadannur")
            
#             # Press Enter to perform the search
#             destination_input.send_keys(Keys.ENTER)
            
#             # Wait for the page to load
#             time.sleep(2)
            
#             # Verify if the search results are displayed correctly
#             # (You can add assertions or further validation here)
#             print("Search performed successfully.")
            
#         except Exception as e:
#             print("An error occurred:", str(e))

#         finally:
#             # Close the browser window
#             driver.quit()





import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class PostComplaint(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/login.html")
        self.driver.maximize_window()
        time.sleep(2)

    def test_post_complaint_workflow(self):
        # Login
        self.login()

        # Navigate to the complaint page
        self.driver.get("http://127.0.0.1:8000/complaint/1/")
        time.sleep(2)

        # Wait for the complaint form to be visible
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "staff_allocation"))
            )
        except NoSuchElementException:
            self.fail("Complaint form not found on the page")

        # Click the "Add Complaint" button
        try:
            add_complaint_button = self.driver.find_element(By.XPATH, "//a[contains(@href, '/complaint/1/') and contains(text(), 'Add Complaint')]")
            add_complaint_button.click()
        except NoSuchElementException:
            self.fail("Add Complaint button not found on the page")

        # Verify if redirected to the correct URL after clicking the "Add Complaint" button
        expected_url_after_post_complaint = 'http://127.0.0.1:8000/dashboard'
        self.assertEqual(self.driver.current_url, expected_url_after_post_complaint,
                         "Redirect to post complaint page failed")

        # Add complaint
        self.add_complaint()

        # Wait for the success message or any element on the new page indicating the submission
        success_message_locator = (By.XPATH, "//div[@class='success-message']")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(success_message_locator)
        )

        # Verify if the success message is displayed
        success_message = self.driver.find_element(*success_message_locator)
        self.assertEqual(success_message.text, "Complaint added successfully.",
                         "Failed to display success message after posting complaint")

    def login(self):
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Sign In']")
        username_input.send_keys("pavi")
        password_input.send_keys("Pavi@123")
        login_button.click()
        time.sleep(5)

        # Wait for the login process to complete
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be("http://127.0.0.1:8000/dashboard")
            )
        except:
            self.fail("Login failed or unexpected page after login")

    def add_complaint(self):
        # Fill in complaint details
        terminal_select = self.driver.find_element(By.NAME, 'panoor')
        terminal_select.send_keys("Your Terminal")

        bus_assignment_select = self.driver.find_element(By.NAME, 'KL-2367-MBC-32')
        bus_assignment_select.send_keys("Your Bus Assignment")

        collection_date_input = self.driver.find_element(By.NAME, '2023-12-04')
        collection_date_input.send_keys("2023-12-01")

        collection_description_input = self.driver.find_element(By.NAME, '')
        collection_description_input.send_keys("no tier available")

        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()



from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class searchTest(LiveServerTestCase):

    def test_search_page(self):
        driver = webdriver.Chrome()

        driver.get("http://127.0.0.1:8000/")
        time.sleep(8)
        try:
            # Find and click on the "Bus Details" button from the dashboard
            bus_details_button = driver.find_element_by_xpath("//a[@class='get-started-btn scrollto']")
            bus_details_button.click()
            
            # Wait for the page to load
            time.sleep(2)
            
            # Verify if the page is redirected to the expected URL
            assert driver.current_url == "http://127.0.0.1:8000/public_bus/"
            print("Successfully redirected to the Public Bus page.")
            
            # Find and click on the search icon
            search_icon = driver.find_element_by_css_selector(".sicon")
            search_icon.click()
            
            # Find the source and destination input fields and enter the values
            source_input = driver.find_element_by_id("sourceInput")
            source_input.send_keys("champad")
            
            destination_input = driver.find_element_by_id("destinationInput")
            destination_input.send_keys("nadannur")
            
            # Press Enter to perform the search
            destination_input.send_keys(Keys.ENTER)
            
            # Wait for the page to load
            time.sleep(2)
            
            # Verify if the search results are displayed correctly
            # (You can add assertions or further validation here)
            print("Search performed successfully.")
            
        except Exception as e:
            print("An error occurred:", str(e))

        finally:
            # Close the browser window
            driver.quit()
