#!/usr/bin/env python3
"""
CORRECTED Working Appium Script - Fixed Birth Date Handling
Day & Month = Dropdowns, Year = Text Input Field

Based on actual screenshot showing:
- Day: Dropdown selection
- Month: Dropdown selection  
- Year: Text input (typing required)
"""

import time
import random
import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

class CorrectedAppiumOutlookCreator:
    def __init__(self, platform_name='Android', device_name='Android', 
                 app_package='com.microsoft.office.outlook'):
        """Initialize corrected Appium-based Outlook creator"""
        self.platform_name = platform_name
        self.device_name = device_name
        self.app_package = app_package
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Setup Appium WebDriver"""
        print("🔧 Setting up Appium driver...")

        options = UiAutomator2Options()
        options.platform_name = self.platform_name
        options.device_name = self.device_name
        options.app_package = self.app_package
        options.app_activity = '.MainActivity'
        options.automation_name = 'UiAutomator2'
        options.no_reset = False
        options.full_reset = False
        options.new_command_timeout = 300
        options.android_device_ready_timeout = 60
        options.android_app_wait_timeout = 60

        try:
            print("🔗 Connecting to Appium server...")
            self.driver = webdriver.Remote("http://localhost:4723", options=options)
            self.wait = WebDriverWait(self.driver, 15)
            print("✅ Connected to Appium server successfully!")
            return True
        except WebDriverException as e:
            if "Could not find a driver" in str(e) or "UiAutomator2" in str(e):
                print("❌ UiAutomator2 driver not found")
                print("💡 Install with: appium driver install uiautomator2")
                return False
            else:
                print(f"❌ Appium connection failed: {e}")
                return False

    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot using Appium"""
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"appium_screenshot_{timestamp}.png"

        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

    def find_element_safely(self, by, value, timeout=10):
        """Find element with error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️  Element not found: {by}={value}")
            return None

    def tap_element_safely(self, element, description=""):
        """Tap element with human-like behavior"""
        if element:
            try:
                element.click()
                print(f"👆 Tapped: {description}")
                time.sleep(random.uniform(1.0, 2.0))
                return True
            except Exception as e:
                print(f"❌ Tap failed for {description}: {e}")
                return False
        return False

    def input_text_safely(self, element, text, description=""):
        """Input text with slower typing"""
        if element:
            try:
                element.clear()
                time.sleep(0.3)
                element.send_keys(text)
                print(f"⌨️  Typed: {text} - {description}")
                time.sleep(random.uniform(0.5, 1.0))
                return True
            except Exception as e:
                print(f"❌ Text input failed for {description}: {e}")
                return False
        return False

    def tap_by_coordinates(self, x: int, y: int, description=""):
        """Tap at specific coordinates"""
        try:
            self.driver.tap([(x, y)])
            print(f"👆 Tapped coordinates ({x}, {y}) - {description}")
            time.sleep(random.uniform(1.0, 2.0))
            return True
        except Exception as e:
            print(f"❌ Coordinate tap failed: {e}")
            return False

    def select_dropdown_option(self, dropdown_element, target_value, description=""):
        """Handle dropdown selection (for Day and Month only)"""
        try:
            # Tap the dropdown to open it
            dropdown_element.click()
            time.sleep(1.5)

            # Try multiple approaches to select the value
            selection_methods = [
                (AppiumBy.XPATH, f"//*[@text='{target_value}']"),
                (AppiumBy.XPATH, f"//*[contains(@text, '{target_value}')]"),
                (AppiumBy.XPATH, f"//*[contains(@content-desc, '{target_value}')]"),
            ]

            for by, selector in selection_methods:
                try:
                    option = self.find_element_safely(by, selector, timeout=3)
                    if option:
                        option.click()
                        print(f"✅ Selected '{target_value}' from {description}")
                        time.sleep(1)
                        return True
                except:
                    continue

            # Try scrolling to find the option
            print(f"🔄 Scrolling to find {target_value} in {description}")
            try:
                self.driver.swipe(540, 800, 540, 600, 1000)
                time.sleep(1)

                for by, selector in selection_methods:
                    option = self.find_element_safely(by, selector, timeout=2)
                    if option:
                        option.click()
                        print(f"✅ Selected '{target_value}' from {description} after scroll")
                        return True
            except:
                pass

            print(f"❌ Could not find {target_value} in {description}")
            return False

        except Exception as e:
            print(f"❌ Dropdown selection failed for {description}: {e}")
            return False

    def long_press_captcha(self, element, duration=3000, description=""):
        """Long press for CAPTCHA"""
        try:
            actions = ActionBuilder(self.driver)
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

            location = element.location
            size = element.size
            x = location['x'] + (size['width'] // 2)
            y = location['y'] + (size['height'] // 2)

            actions.add_action(pointer.create_pointer_move(duration=0, x=x, y=y))
            actions.add_action(pointer.create_pointer_down())
            actions.add_action(pointer.create_pause(duration/1000))
            actions.add_action(pointer.create_pointer_up())
            actions.perform()

            print(f"👆🕐 Long pressed: {description} for {duration}ms")
            time.sleep(duration/1000 + 3)
            return True
        except Exception as e:
            print(f"❌ Long press failed for {description}: {e}")
            return False

    def step1_welcome_screen(self) -> bool:
        """Step 1: Handle Welcome to Outlook screen"""
        print("\n📱 STEP 1: Welcome to Outlook")
        self.take_screenshot("appium_01_welcome.png")

        selectors_to_try = [
            (AppiumBy.XPATH, "//*[contains(@text, 'CREATE NEW ACCOUNT')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Create new account')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'CREATE NEW ACCOUNT')]"),
        ]

        for by, selector in selectors_to_try:
            element = self.find_element_safely(by, selector, timeout=5)
            if element and self.tap_element_safely(element, "CREATE NEW ACCOUNT"):
                time.sleep(3)
                self.take_screenshot("appium_01_after_create_new.png")
                return True

        # Coordinate fallback
        print("🎯 Trying coordinate-based tap for CREATE NEW ACCOUNT")
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] // 2
        y = int(screen_size['height'] * 0.75)

        if self.tap_by_coordinates(x, y, "CREATE NEW ACCOUNT (coordinates)"):
            time.sleep(3)
            self.take_screenshot("appium_01_after_coord_tap.png")
            return True

        print("❌ Failed to find CREATE NEW ACCOUNT")
        return False

    def step2_email_creation(self, username: str) -> bool:
        """Step 2: Create your Microsoft account - Email"""
        print("\n📧 STEP 2: Create your Microsoft account")
        self.take_screenshot("appium_02_email_creation.png")

        email_field_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'New email')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'New email')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        ]

        for by, selector in email_field_selectors:
            email_field = self.find_element_safely(by, selector, timeout=5)
            if email_field and self.input_text_safely(email_field, username, "Username"):
                break
        else:
            print("❌ Could not find email input field")
            return False

        next_button_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Next')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next')]"),
        ]

        for by, selector in next_button_selectors:
            next_button = self.find_element_safely(by, selector, timeout=5)
            if next_button and self.tap_element_safely(next_button, "Next button"):
                time.sleep(3)
                self.take_screenshot("appium_02_after_email.png")
                return True

        print("❌ Could not find Next button")
        return False

    def step3_password_creation(self, password: str) -> bool:
        """Step 3: Create your password"""
        print("\n🔒 STEP 3: Create your password")
        self.take_screenshot("appium_03_password_creation.png")

        password_field_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'Password')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[@password='true']"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
        ]

        for by, selector in password_field_selectors:
            password_field = self.find_element_safely(by, selector, timeout=5)
            if password_field and self.input_text_safely(password_field, password, "Password"):
                break
        else:
            print("❌ Could not find password input field")
            return False

        next_button_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Next')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next')]"),
        ]

        for by, selector in next_button_selectors:
            next_button = self.find_element_safely(by, selector, timeout=5)
            if next_button and self.tap_element_safely(next_button, "Next button"):
                time.sleep(3)
                self.take_screenshot("appium_03_after_password.png")
                return True

        print("❌ Could not find Next button")
        return False

    def step4_add_details(self, birth_day: int, birth_month: str, birth_year: int) -> bool:
        """Step 4: Add details - CORRECTED Birth Date Handling"""
        print("\n📅 STEP 4: Add some details")
        self.take_screenshot("appium_04_add_details.png")

        print("🏳️  Keeping default country selection")

        # Day dropdown
        print(f"📅 Setting day to {birth_day}")
        day_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Day')]"),
            (AppiumBy.XPATH, "//*[contains(@hint, 'Day')]"),
            (AppiumBy.XPATH, "//android.widget.Spinner[1]"),
        ]

        for by, selector in day_selectors:
            day_dropdown = self.find_element_safely(by, selector, timeout=5)
            if day_dropdown:
                if self.select_dropdown_option(day_dropdown, birth_day, "Day dropdown"):
                    break

        # Month dropdown
        print(f"📅 Setting month to {birth_month}")
        month_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Month')]"),
            (AppiumBy.XPATH, "//*[contains(@hint, 'Month')]"),
            (AppiumBy.XPATH, "//android.widget.Spinner[2]"),
        ]

        for by, selector in month_selectors:
            month_dropdown = self.find_element_safely(by, selector, timeout=5)
            if month_dropdown:
                if self.select_dropdown_option(month_dropdown, birth_month, "Month dropdown"):
                    break

        # Year text input (NOT dropdown) - CORRECTED
        print(f"📅 Typing year {birth_year} (text input field)")
        year_field_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'Year')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Year') and @class='android.widget.EditText']"),
            (AppiumBy.XPATH, "//android.widget.EditText[contains(@hint, 'Year')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[last()]"),  # Last EditText on screen
        ]

        year_input_success = False
        for by, selector in year_field_selectors:
            year_field = self.find_element_safely(by, selector, timeout=5)
            if year_field:
                if self.input_text_safely(year_field, str(birth_year), "Year field"):
                    year_input_success = True
                    break

        if not year_input_success:
            print("⚠️  Could not find year text field, trying coordinate tap")
            # Fallback: tap at typical year field location and type
            screen_size = self.driver.get_window_size()
            year_x = int(screen_size['width'] * 0.75)  # Right side
            year_y = int(screen_size['height'] * 0.45)  # Middle area

            if self.tap_by_coordinates(year_x, year_y, "Year field (coordinates)"):
                time.sleep(1)
                # Try to type the year
                try:
                    self.driver.set_value(str(birth_year))
                    print(f"⌨️  Typed year {birth_year} via set_value")
                except:
                    # Last resort: use keyevent to type each digit
                    year_str = str(birth_year)
                    for digit in year_str:
                        keycode = 7 + int(digit)  # KEYCODE_0 = 7, KEYCODE_1 = 8, etc.
                        self.driver.press_keycode(keycode)
                        time.sleep(0.1)
                    print(f"⌨️  Typed year {birth_year} via keycodes")

        # Look for Next button
        next_button_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Next')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next')]"),
        ]

        for by, selector in next_button_selectors:
            next_button = self.find_element_safely(by, selector, timeout=5)
            if next_button and self.tap_element_safely(next_button, "Next button"):
                time.sleep(5)
                self.take_screenshot("appium_04_after_details.png")
                return True

        print("❌ Could not find Next button")
        return False

    def step5_captcha_challenge(self) -> bool:
        """Step 5: CAPTCHA - Let's prove you're human"""
        print("\n🤖 STEP 5: CAPTCHA Challenge")
        self.take_screenshot("appium_05_captcha.png")

        captcha_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Press and hold')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'prove you')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Press')]"),
        ]

        for by, selector in captcha_selectors:
            captcha_element = self.find_element_safely(by, selector, timeout=8)
            if captcha_element:
                print("🎯 Found CAPTCHA element, performing long press...")
                if self.long_press_captcha(captcha_element, 3500, "CAPTCHA Press and Hold"):
                    print("⏳ Waiting for CAPTCHA verification...")
                    time.sleep(8)
                    return True

        # Coordinate fallback for CAPTCHA
        print("🎯 Trying coordinate-based CAPTCHA press")
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] // 2
        y = int(screen_size['height'] * 0.6)

        try:
            actions = ActionBuilder(self.driver)
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

            actions.add_action(pointer.create_pointer_move(duration=0, x=x, y=y))
            actions.add_action(pointer.create_pointer_down())
            actions.add_action(pointer.create_pause(3.5))
            actions.add_action(pointer.create_pointer_up())
            actions.perform()

            print("👆🕐 Long pressed CAPTCHA area (coordinates)")
            time.sleep(8)
            return True

        except Exception as e:
            print(f"❌ CAPTCHA handling failed: {e}")
            return False

    def step6_add_name(self, first_name: str, last_name: str) -> bool:
        """Step 6: Add your name"""
        print("\n👤 STEP 6: Add your name")
        self.take_screenshot("appium_06_add_name.png")

        # First name field
        first_name_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'First name')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
        ]

        for by, selector in first_name_selectors:
            first_name_field = self.find_element_safely(by, selector, timeout=5)
            if first_name_field and self.input_text_safely(first_name_field, first_name, "First name"):
                break
        else:
            print("❌ Could not find first name field")
            return False

        # Last name field
        last_name_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'Last name')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[2]"),
        ]

        for by, selector in last_name_selectors:
            last_name_field = self.find_element_safely(by, selector, timeout=5)
            if last_name_field and self.input_text_safely(last_name_field, last_name, "Last name"):
                break
        else:
            print("❌ Could not find last name field")
            return False

        # Final Next button
        next_button_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Next')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Next')]"),
        ]

        for by, selector in next_button_selectors:
            next_button = self.find_element_safely(by, selector, timeout=5)
            if next_button and self.tap_element_safely(next_button, "Final Next button"):
                time.sleep(5)
                self.take_screenshot("appium_06_after_name.png")
                return True

        print("❌ Could not find final Next button")
        return False

    def run_complete_automation(self, user_data: dict):
        """Run the complete 6-step automation"""
        print("🤖 STARTING CORRECTED APPIUM AUTOMATION")
        print("=" * 60)
        print(f"📧 Email: {user_data['username']}@outlook.com")
        print(f"🔒 Password: {user_data['password']}")
        print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
        print(f"📅 DOB: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
        print("🔧 Birth Date: Day=dropdown, Month=dropdown, Year=text input")
        print("=" * 60)

        try:
            if not self.setup_driver():
                return False

            time.sleep(5)

            # All 6 steps
            if not self.step1_welcome_screen():
                print("❌ Step 1 failed")
                return False

            if not self.step2_email_creation(user_data['username']):
                print("❌ Step 2 failed")
                return False

            if not self.step3_password_creation(user_data['password']):
                print("❌ Step 3 failed")
                return False

            birth = user_data['birth_date']
            if not self.step4_add_details(birth['day'], birth['month'], birth['year']):
                print("❌ Step 4 failed")
                return False

            if not self.step5_captcha_challenge():
                print("❌ Step 5 failed")
                return False

            if not self.step6_add_name(user_data['first_name'], user_data['last_name']):
                print("❌ Step 6 failed")
                return False

            print("\n🎉 ALL 6 STEPS COMPLETED SUCCESSFULLY!")
            print("✅ Corrected automation finished")
            self.take_screenshot("appium_07_final_success.png")
            return True

        except Exception as e:
            print(f"❌ Automation error: {e}")
            self.take_screenshot("appium_error.png")
            return False
        finally:
            if self.driver:
                print("🔚 Closing Appium session...")
                self.driver.quit()

def main():
    """Main function"""
    print("🚀 CORRECTED APPIUM OUTLOOK AUTOMATION")
    print("=" * 50)

    user_data = {
        'username': f'correcteduser{random.randint(100000, 999999)}',
        'password': f'Corrected{random.randint(100, 999)}Pass!',
        'first_name': 'Corrected',
        'last_name': 'User',
        'birth_date': {
            'day': random.randint(1, 28),
            'month': 'January',
            'year': random.randint(1990, 2000)
        }
    }

    print("🎬 Starting corrected automation in 3 seconds...")
    time.sleep(3)

    try:
        creator = CorrectedAppiumOutlookCreator()
        success = creator.run_complete_automation(user_data)

        if success:
            print("\n🎊 SUCCESS! Account created with corrected birth date handling!")
            print("=" * 60)
            print("ACCOUNT DETAILS:")
            print(f"📧 Email: {user_data['username']}@outlook.com")
            print(f"🔒 Password: {user_data['password']}")
            print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
            print("=" * 60)
        else:
            print("\n❌ Automation failed")

    except KeyboardInterrupt:
        print("\n🛑 Automation stopped")
    except Exception as e:
        print(f"\n💥 Error: {e}")

if __name__ == "__main__":
    main()
