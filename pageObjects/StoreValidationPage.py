import time

from anticaptchaofficial.recaptchav2proxyless import *
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StoreValidationPage:
    previewCode_ID = "guestTkn"
    submitPreview_XPATH = "//input[@value='Submit']"
    recaptchaCompletionMark_ClassName = "recaptcha-checkbox-borderAnimation"
    storyBlock_Css = "div > fw-storyblock"
    nextProduct_Css = "[title='Next Card']"
    previousProduct_Css = "[title='Previous Card']"
    productName_Css = "[data-testid='product-card-item-name']"
    add_toBasket_CSS = "[data-testid='add-to-cart-button']"
    checkout_Css = "[data-testid='checkout-button']"
    continue_to_shopping = "[data-testid='continue-shopping-button']"
    cartEmpty_Css = ".fwn-ntt6st er86ptx5"
    priceDetails_Css = ".fwn-1q0kih1.er86ptx1"
    cartCloseIcon_Css = "[data-testid='close-button']"
    basketIcon_Css = "[data-testid='cart-button']"
    backButton_Css = "[data-testid='back-button']"
    increaseButton_Css = "[data-testid='cart-item-increase-button']"
    decreaseButton_Css = "[data-testid='cart-item-decrease-button']"


    def __init__(self, driver):
        self.driver = driver

    def enterPreviewCode(self, previewCode):
        self.driver.find_element(By.ID, self.previewCode_ID).send_keys(previewCode)
        time.sleep(20)
        self.driver.find_element(By.XPATH, self.submitPreview_XPATH).click()

    def validateStoreTitlePage(self):
        get_title = self.driver.title
        print(get_title)
        assert get_title == "Virtina Dev Store"
        time.sleep(5)

    def nextProductNavigate(self):
        cssSelectorForHost1 = "fw-storyblock[channel='zen_channel']"
        self.driver.execute_script("window.scrollBy(0,200)", "")
        # shadow = self.driver.find_element(By.CSS_SELECTOR, cssSelectorForHost1).shadow_root
        root_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, cssSelectorForHost1)))
        shadow_host = self.driver.execute_script('return arguments[0].shadowRoot', root_element)
        while True:
            try:
                element = shadow_host.find_element(By.CSS_SELECTOR, self.nextProduct_Css)
                # element = WebDriverWait(shadow_host, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.nextProduct_Css)))
                if element.is_displayed():
                    element.click()
                    time.sleep(4)
            except NoSuchElementException:
                print("All Products Navigated")
                # shadow_host.find_element(By.CSS_SELECTOR, self.previousProduct_Css).click()
                break

    def addSingleProduct(self):
        cssSelectorForHost2 = "fw-storyblock[channel='zen_channel']"
        shadow = self.driver.find_element(By.CSS_SELECTOR, cssSelectorForHost2).shadow_root
        product = shadow.find_element(By.CSS_SELECTOR, self.productName_Css)
        self.driver.execute_script("arguments[0].click();", product)
        time.sleep(6)
        addToBasket = shadow.find_element(By.CSS_SELECTOR, self.add_toBasket_CSS)
        addToBasket.click()
        time.sleep(6)
        continueShopping = shadow.find_element(By.CSS_SELECTOR, self.continue_to_shopping)
        continueShopping.click()

    def checkOutValidation(self):
        time.sleep(7)
        cssSelectorForHost2 = "fw-storyblock[channel='zen_channel']"
        shadow = self.driver.find_element(By.CSS_SELECTOR, cssSelectorForHost2).shadow_root
        time.sleep(5)
        basketIcon = shadow.find_element(By.CSS_SELECTOR, self.basketIcon_Css)
        basketIcon.click()
        time.sleep(5)
        closeIcon = shadow.find_element(By.CSS_SELECTOR, self.cartCloseIcon_Css)
        closeIcon.click()
        time.sleep(5)
        backButton = shadow.find_element(By.CSS_SELECTOR, self.backButton_Css)
        backButton.click()
        time.sleep(5)
        product = shadow.find_element(By.CSS_SELECTOR, self.productName_Css)
        self.driver.execute_script("arguments[0].click();", product)
        time.sleep(5)
        basketIcon = shadow.find_element(By.CSS_SELECTOR, self.basketIcon_Css)
        basketIcon.click()
        time.sleep(5)

    def productManageCheckoutPage(self):
        cssSelectorForHost2 = "fw-storyblock[channel='zen_channel']"
        shadow = self.driver.find_element(By.CSS_SELECTOR, cssSelectorForHost2).shadow_root
        try:
            element = shadow.find_element(By.CSS_SELECTOR, self.cartEmpty_Css)
            # element = WebDriverWait(shadow_host, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.nextProduct_Css)))
            if element.is_displayed():
                shadow.find_element(By.CSS_SELECTOR, self.cartCloseIcon_Css).click()
                time.sleep(4)
                addToBasket = shadow.find_element(By.CSS_SELECTOR, self.add_toBasket_CSS)
                addToBasket.click()
            else:
                print("Products are available in basket")
        except NoSuchElementException:
            print("Not able to find the cart message")

        while True:
            try:
                element1 = shadow.find_element(By.CSS_SELECTOR, self.decreaseButton_Css)
                if element1.is_displayed():
                    element1.click()
                    time.sleep(6)
            except NoSuchElementException:
                print("No Negative Buttons Available")
                shadow.find_element(By.CSS_SELECTOR, self.cartCloseIcon_Css).click()
                break
        addToBasket = shadow.find_element(By.CSS_SELECTOR, self.add_toBasket_CSS)
        addToBasket.click()
        time.sleep(6)
        shadow_host = self.driver.find_element(By.CSS_SELECTOR, cssSelectorForHost2)
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', shadow_host)
        shadow_element = shadow_root.find_element(By.CSS_SELECTOR, self.priceDetails_Css)
        shadow_price_text = shadow_element.text
        productPrice = shadow_price_text.replace("$", "")
        print(productPrice)
        converted_totalPrice = float(productPrice)
        shadow.find_element(By.CSS_SELECTOR, self.increaseButton_Css).click()
        time.sleep(6)
        UpdatedPrice = shadow_root.find_element(By.CSS_SELECTOR, self.priceDetails_Css)
        shadow_updatedPrice_text = UpdatedPrice.text
        UpdatedproductPrice = shadow_updatedPrice_text.replace("$", "")
        print(UpdatedproductPrice)
        converted_UpdatedPrice = float(UpdatedproductPrice)
        assert converted_UpdatedPrice == converted_totalPrice + converted_totalPrice
        shadow.find_element(By.CSS_SELECTOR, self.checkout_Css)
        time.sleep(2)

