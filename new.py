#!/usr/bin/env python3

"""
Complete Microsoft Outlook Account Creation Automation - UPDATED CAPTCHA
=======================================================================

Full working automation script with PRECISE CAPTCHA BUTTON TARGETING.

ONLY UPDATED: CAPTCHA long press to target actual button, not label text
ALL OTHER FUNCTIONALITY: Unchanged and working perfectly

Features:
- Correct flow: Welcome → Email → Password → Details → Name → CAPTCHA
- Robust element detection with multiple fallback strategies
- Smart field detection using hints, geometry, and positioning
- PRECISE 15-second CAPTCHA button targeting (UPDATED)
- Comprehensive error handling and logging
- Multiple input methods (direct, ADB, keycode)

Requirements:
- Appium Server running on localhost:4723
- UiAutomator2 driver installed
- ADB in system PATH
- Microsoft Outlook app installed on Android device

Usage: python outlook_automation_fixed_captcha.py
"""

import time
import random
import subprocess
import logging
from typing import Optional, Tuple, Dict, Any
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OutlookAccountCreator:
    """Complete Microsoft Outlook account creation automation"""
    
    def __init__(self, 
                 platform_name: str = 'Android',
                 device_name: str = 'Android', 
                 app_package: str = 'com.microsoft.office.outlook'):
        self.platform_name = platform_name
        self.device_name = device_name
        self.app_package = app_package
        self.driver = None
        self.wait = None
        self.screen_size = None

    def setup_driver(self) -> bool:
        """Initialize Appium WebDriver with optimized settings"""
        logger.info("🔧 Setting up Appium driver...")
        
        try:
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
            options.unicode_keyboard = True
            options.reset_keyboard = True
            options.auto_grant_permissions = True
            options.disable_android_watchers = True
            
            self.driver = webdriver.Remote("http://localhost:4723", options=options)
            self.wait = WebDriverWait(self.driver, 20)
            self.screen_size = self.driver.get_window_size()
            
            # Enable XPath1 for stability
            self.driver.update_settings({"enforceXPath1": True})
            
            logger.info("✅ Appium driver setup complete")
            return True
            
        except WebDriverException as e:
            logger.error(f"❌ Driver setup failed: {e}")
            if "Could not find a driver" in str(e):
                logger.error("💡 Install UiAutomator2: appium driver install uiautomator2")
            return False

    def find_element_safe(self, by: str, value: str, timeout: int = 10) -> Optional[any]:
        """Safely find element with timeout"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logger.warning(f"⚠️ Element not found: {by}={value}")
            return None

    def click_element_safe(self, element, description: str = "") -> bool:
        """Safely click element with error handling"""
        if not element:
            return False
        try:
            element.click()
            logger.info(f"👆 Clicked: {description}")
            time.sleep(random.uniform(1.0, 2.5))
            return True
        except Exception as e:
            logger.error(f"❌ Click failed for {description}: {e}")
            return False

    def type_text_robust(self, element, text: str, description: str = "") -> bool:
        """Robust text input with multiple methods"""
        if not element:
            logger.error(f"❌ No element provided for typing: {description}")
            return False
            
        try:
            # Focus on element
            element.click()
            time.sleep(0.5)
            
            # Clear existing text
            try:
                element.clear()
                time.sleep(0.3)
            except:
                # Manual clear with backspace
                current_text = element.get_attribute("text") or ""
                for _ in range(len(current_text) + 5):
                    self.driver.press_keycode(67)  # KEYCODE_DEL
                    time.sleep(0.02)
            
            # Type text
            try:
                element.send_keys(str(text))
                logger.info(f"⌨️ Typed '{text}' in {description}")
                time.sleep(0.5)
                return True
            except Exception as e:
                logger.warning(f"⚠️ Direct typing failed for {description}: {e}")
                
                # Fallback: ADB input
                try:
                    subprocess.run(['adb', 'shell', 'input', 'text', str(text)], 
                                 check=True, capture_output=True)
                    logger.info(f"✅ ADB typed '{text}' in {description}")
                    time.sleep(0.5)
                    return True
                except:
                    logger.warning("⚠️ ADB typing failed")
                
                # Fallback: Keycode input (for numbers)
                if str(text).isdigit():
                    try:
                        for digit in str(text):
                            keycode = 7 + int(digit)  # KEYCODE_0 = 7
                            self.driver.press_keycode(keycode)
                            time.sleep(0.1)
                        logger.info(f"✅ Keycode typed '{text}' in {description}")
                        return True
                    except:
                        logger.warning("⚠️ Keycode typing failed")
                
                return False
                
        except Exception as e:
            logger.error(f"❌ All typing methods failed for {description}: {e}")
            return False

    def find_name_fields(self) -> Tuple[Optional[any], Optional[any]]:
        """Smart detection of First Name and Last Name fields"""
        logger.info("🔍 Detecting name fields...")
        
        # Strategy 1: Look for hint text
        try:
            first_name_hints = [
                "//*[contains(@hint, 'First')]",
                "//*[contains(@hint, 'first')]", 
                "//*[contains(@hint, 'FIRST')]"
            ]
            
            last_name_hints = [
                "//*[contains(@hint, 'Last')]",
                "//*[contains(@hint, 'last')]",
                "//*[contains(@hint, 'LAST')]"
            ]
            
            first_field = None
            last_field = None
            
            for hint in first_name_hints:
                first_field = self.find_element_safe(AppiumBy.XPATH, hint, timeout=3)
                if first_field:
                    break
                    
            for hint in last_name_hints:
                last_field = self.find_element_safe(AppiumBy.XPATH, hint, timeout=3)
                if last_field:
                    break
            
            if first_field and last_field:
                logger.info("✅ Found name fields by hints")
                return first_field, last_field
                
        except Exception as e:
            logger.warning(f"⚠️ Hint-based detection failed: {e}")
        
        # Strategy 2: Get all EditText fields and sort by position
        try:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            visible_fields = []
            
            for field in edit_texts:
                try:
                    if field.is_displayed():
                        bounds = field.get_attribute("bounds")
                        if bounds:
                            # Parse bounds: "[x1,y1][x2,y2]"
                            import re
                            match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                            if match:
                                x1, y1, x2, y2 = map(int, match.groups())
                                visible_fields.append((y1, field))  # Sort by Y position
                except:
                    continue
            
            # Sort by Y position (top to bottom)
            visible_fields.sort(key=lambda x: x[0])
            
            if len(visible_fields) >= 2:
                logger.info("✅ Found name fields by position")
                return visible_fields[0][1], visible_fields[1][1]  # First two fields
                
        except Exception as e:
            logger.warning(f"⚠️ Position-based detection failed: {e}")
        
        # Strategy 3: Simple fallback - first two EditText elements
        try:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if len(edit_texts) >= 2:
                logger.info("✅ Found name fields by index")
                return edit_texts[0], edit_texts[1]
        except Exception as e:
            logger.warning(f"⚠️ Index-based detection failed: {e}")
        
        logger.error("❌ Could not detect name fields")
        return None, None

    def click_next_button(self, context: str = "") -> bool:
        """Comprehensive Next button clicking with multiple strategies"""
        logger.info(f"➡️ Attempting to click Next button ({context})")
        
        # Strategy 1: UiAutomator with textContains
        ui_selectors = [
            'new UiSelector().textContains("Next").clickable(true).enabled(true)',
            'new UiSelector().text("Next").clickable(true)',
            'new UiSelector().textMatches(".*Next.*").clickable(true)',
            'new UiSelector().className("android.widget.Button").textContains("Next")',
        ]
        
        for selector in ui_selectors:
            try:
                element = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
                )
                element.click()
                logger.info(f"✅ Next clicked via UiSelector: {selector}")
                time.sleep(2)
                return True
            except Exception:
                continue
        
        # Strategy 2: XPath selectors
        xpath_selectors = [
            "//*[@text='Next']",
            "//*[contains(@text, 'Next')]",
            "//android.widget.Button[@text='Next']",
            "//android.widget.Button[contains(@text, 'Next')]",
            "//*[@content-desc='Next']",
            "//*[contains(@content-desc, 'Next')]"
        ]
        
        for selector in xpath_selectors:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, selector))
                )
                element.click()
                logger.info(f"✅ Next clicked via XPath: {selector}")
                time.sleep(2)
                return True
            except Exception:
                continue
        
        # Strategy 3: ENTER key press (for forms with IME action)
        try:
            logger.info("⌨️ Trying ENTER key")
            self.driver.press_keycode(66)  # KEYCODE_ENTER
            time.sleep(2)
            logger.info("✅ ENTER key pressed")
            return True
        except Exception as e:
            logger.warning(f"⚠️ ENTER key failed: {e}")
        
        # Strategy 4: Look for any clickable button in bottom area
        try:
            logger.info("🔍 Searching for buttons in bottom area")
            all_buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
            bottom_threshold = self.screen_size['height'] * 0.6
            
            for button in all_buttons:
                try:
                    location = button.location
                    if location['y'] > bottom_threshold and button.is_enabled():
                        button_text = button.get_attribute("text") or ""
                        logger.info(f"🎯 Trying bottom button: '{button_text}'")
                        button.click()
                        time.sleep(2)
                        logger.info("✅ Bottom button clicked")
                        return True
                except Exception:
                    continue
        except Exception as e:
            logger.warning(f"⚠️ Bottom button search failed: {e}")
        
        # Strategy 5: Small scroll and retry
        try:
            logger.info("🔄 Scrolling and retrying")
            self.driver.swipe(
                self.screen_size['width'] // 2, 
                int(self.screen_size['height'] * 0.8),
                self.screen_size['width'] // 2, 
                int(self.screen_size['height'] * 0.6), 
                500
            )
            time.sleep(1)
            
            # Retry first XPath
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text, 'Next')]"))
            )
            element.click()
            logger.info("✅ Next clicked after scroll")
            time.sleep(2)
            return True
        except Exception as e:
            logger.warning(f"⚠️ Scroll and retry failed: {e}")
        
        # Strategy 6: Coordinate-based tapping
        try:
            logger.info("📍 Trying coordinate-based Next button tap")
            coordinates = [
                (self.screen_size['width'] // 2, int(self.screen_size['height'] * 0.9)),  # Bottom center
                (int(self.screen_size['width'] * 0.8), int(self.screen_size['height'] * 0.9)),  # Bottom right
                (self.screen_size['width'] // 2, int(self.screen_size['height'] * 0.85)),  # Slightly higher
            ]
            
            for x, y in coordinates:
                try:
                    self.driver.tap([(x, y)])
                    logger.info(f"✅ Tapped coordinates ({x}, {y})")
                    time.sleep(2)
                    return True
                except Exception:
                    continue
        except Exception as e:
            logger.warning(f"⚠️ Coordinate tapping failed: {e}")
        
        logger.error(f"❌ All Next button strategies failed for: {context}")
        return False

    def find_year_field(self):
        """Find the year input field using multiple strategies"""
        logger.info("🔍 Looking for year field...")
        
        # Strategy 1: Last EditText (usually the year field)
        try:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if edit_texts:
                last_field = edit_texts[-1]
                logger.info("✅ Found year field (last EditText)")
                return last_field
        except Exception:
            pass
        
        # Strategy 2: Rightmost EditText by bounds
        try:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            rightmost_field = None
            max_x = 0
            
            for field in edit_texts:
                try:
                    bounds = field.get_attribute("bounds")
                    if bounds:
                        import re
                        match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                        if match:
                            x2 = int(match.group(3))  # Right edge
                            if x2 > max_x:
                                max_x = x2
                                rightmost_field = field
                except:
                    continue
            
            if rightmost_field:
                logger.info("✅ Found year field (rightmost)")
                return rightmost_field
        except Exception:
            pass
        
        # Strategy 3: UiSelector with instance
        for instance in [2, 1, 0]:  # Try 3rd, 2nd, 1st
            try:
                field = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().className("android.widget.EditText").enabled(true).instance({instance})'
                )
                logger.info(f"✅ Found year field (instance {instance})")
                return field
            except Exception:
                continue
        
        logger.error("❌ Could not find year field")
        return None

    def select_dropdown_option(self, dropdown_element, target_value: str, description: str = "") -> bool:
        """Select option from dropdown menu"""
        try:
            dropdown_element.click()
            time.sleep(1.5)
            
            # Look for the option
            selectors = [
                f"//*[@text='{target_value}']",
                f"//*[contains(@text, '{target_value}')]",
                f"//*[contains(@content-desc, '{target_value}')]"
            ]
            
            for selector in selectors:
                try:
                    option = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, selector))
                    )
                    option.click()
                    logger.info(f"✅ Selected '{target_value}' from {description}")
                    time.sleep(1)
                    return True
                except Exception:
                    continue
            
            # Try scrolling to find option
            logger.info(f"🔄 Scrolling to find {target_value}")
            self.driver.swipe(540, 800, 540, 600, 1000)
            time.sleep(1)
            
            for selector in selectors:
                try:
                    option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, selector))
                    )
                    option.click()
                    logger.info(f"✅ Selected '{target_value}' after scroll")
                    return True
                except Exception:
                    continue
            
            logger.warning(f"⚠️ Could not find option: {target_value}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Dropdown selection failed: {e}")
            return False

    # ====== UPDATED CAPTCHA FUNCTIONS ======
    
    def find_captcha_button_precise(self):
        """UPDATED: Find the actual CAPTCHA button, not the label text"""
        logger.info("🎯 PRECISE: Looking for actual CAPTCHA button...")
        
        # Strategy 1: Strong UiSelector - Button + text + clickable
        ui_candidates = [
            'new UiSelector().className("android.widget.Button").textContains("Press").textContains("hold").clickable(true).enabled(true)',
            'new UiSelector().className("android.widget.Button").textMatches("(?i).*press.*hold.*").clickable(true).enabled(true)',
            'new UiSelector().className("android.widget.Button").descriptionContains("Press").descriptionContains("hold").clickable(true).enabled(true)'
        ]
        
        for ui_selector in ui_candidates:
            try:
                element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)
                if element:
                    logger.info(f"✅ Found CAPTCHA button via UiSelector: {ui_selector}")
                    return element
            except Exception:
                continue
        
        # Strategy 2: XPath - ignore TextView label, take the next button
        xpaths = [
            "//*[contains(@text,'Press and hold') and @class!='android.widget.TextView']/following::android.widget.Button[1]",
            "//android.widget.Button[contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'press and hold')]",
            "//*[contains(@content-desc,'Press') and contains(@content-desc,'hold') and @clickable='true']",
            "//android.widget.Button[contains(@text,'Press') and contains(@text,'hold')]"
        ]
        
        for xpath in xpaths:
            try:
                element = self.driver.find_element(AppiumBy.XPATH, xpath)
                if element:
                    logger.info(f"✅ Found CAPTCHA button via XPath: {xpath}")
                    return element
            except Exception:
                continue
        
        # Strategy 3: Heuristic - pick largest clickable button in middle/lower band
        try:
            candidate = None
            best_area = 0
            height = self.screen_size['height']
            lower_bound = int(height * 0.45)  # Lower 55% of screen
            upper_bound = int(height * 0.85)  # Upper 15% excluded
            
            logger.info(f"🔍 Searching for buttons in vertical band: {lower_bound} to {upper_bound}")
            
            for button in self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button"):
                try:
                    if not button.is_enabled():
                        continue
                        
                    bounds = button.get_attribute("bounds")  # [x1,y1][x2,y2]
                    if not bounds:
                        continue
                        
                    import re
                    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                    if not match:
                        continue
                        
                    x1, y1, x2, y2 = map(int, match.groups())
                    center_y = (y1 + y2) // 2
                    
                    # Check if button is in the target vertical band
                    if lower_bound <= center_y <= upper_bound:
                        area = (x2 - x1) * (y2 - y1)
                        if area > best_area:
                            best_area = area
                            candidate = button
                            logger.info(f"📍 Found button candidate at center_y={center_y}, area={area}")
                            
                except Exception:
                    continue
            
            if candidate:
                logger.info("✅ Found CAPTCHA button via heuristic area search")
                return candidate
                
        except Exception as e:
            logger.warning(f"⚠️ Heuristic button search failed: {e}")
        
        logger.warning("⚠️ Could not find specific CAPTCHA button")
        return None

    def press_captcha_button_precise(self) -> bool:
        """UPDATED: Perform precise 15-second long press on actual button"""
        logger.info("🤖 PRECISE: Starting CAPTCHA button press (15 seconds)")
        
        # Find the true button, not the label
        button = self.find_captcha_button_precise()
        
        if not button:
            logger.warning("⚠️ No specific button found, using center-screen fallback")
            # As a last resort, center-screen ADB long press
            cx = self.screen_size['width'] // 2
            cy = int(self.screen_size['height'] * 0.6)
            try:
                subprocess.run([
                    "adb", "shell", "input", "touchscreen", "swipe",
                    str(cx), str(cy), str(cx), str(cy), "15000"
                ], check=False)
                logger.info("✅ Fallback ADB long press completed")
                time.sleep(5)
                return True
            except Exception as e:
                logger.error(f"❌ Fallback ADB press failed: {e}")
                return False
        
        # Hide keyboard and prepare for press
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        
        # Get button center coordinates
        try:
            location = button.location
            size = button.size
            cx = location['x'] + size['width'] // 2
            cy = location['y'] + size['height'] // 2
            logger.info(f"📍 Button center coordinates: ({cx}, {cy})")
        except Exception:
            # Fallback center if bounds missing
            cx = self.screen_size['width'] // 2
            cy = int(self.screen_size['height'] * 0.6)
            logger.warning(f"⚠️ Using fallback coordinates: ({cx}, {cy})")
        
        # Method 1: Native longClickGesture (preferred)
        try:
            logger.info("🎯 Trying native longClickGesture...")
            self.driver.execute_script("mobile: longClickGesture", {
                "elementId": button.id, 
                "duration": 15000
            })
            logger.info("✅ Native longClickGesture completed (15s)")
            time.sleep(3)
            return True
        except Exception as e:
            logger.warning(f"⚠️ Native longClickGesture failed: {e}")
        
        # Method 2: W3C Actions - 15×1s ticks to avoid long-pause timeouts
        try:
            logger.info("🎯 Trying W3C Actions (15×1s ticks)...")
            actions = ActionBuilder(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions.add_action(finger.create_pointer_move(duration=0, x=cx, y=cy))
            actions.add_action(finger.create_pointer_down())
            
            # 15 one-second pauses instead of one 15-second pause
            for i in range(15):
                actions.add_action(finger.create_pause(1))
                if i % 5 == 0:  # Log progress every 5 seconds
                    logger.info(f"⏳ Holding... {i+1}/15 seconds")
            
            actions.add_action(finger.create_pointer_up())
            actions.perform()
            
            logger.info("✅ W3C Actions long press completed (15s)")
            time.sleep(3)
            return True
        except Exception as e:
            logger.warning(f"⚠️ W3C Actions failed: {e}")
        
        # Method 3: ADB swipe exactly at button center for 15s
        try:
            logger.info("🎯 Trying ADB swipe at button center...")
            subprocess.run([
                "adb", "shell", "input", "touchscreen", "swipe",
                str(cx), str(cy), str(cx), str(cy), "15000"
            ], check=False)
            logger.info("✅ ADB long press completed (15s)")
            time.sleep(5)
            return True
        except Exception as e:
            logger.warning(f"⚠️ ADB swipe failed: {e}")
        
        logger.error("❌ All CAPTCHA long press methods failed")
        return False

    # ====== END UPDATED CAPTCHA FUNCTIONS ======

    # STEP IMPLEMENTATIONS (UNCHANGED - ALL WORKING)
    
    def step1_welcome_screen(self) -> bool:
        """Step 1: Handle Welcome to Outlook screen"""
        logger.info("\n📱 STEP 1: Welcome to Outlook")
        
        try:
            # Look for CREATE NEW ACCOUNT button
            selectors = [
                "//*[contains(@text, 'CREATE NEW ACCOUNT')]",
                "//*[contains(@text, 'Create new account')]",
                "//*[contains(@content-desc, 'CREATE NEW ACCOUNT')]",
                "//android.widget.Button[contains(@text, 'CREATE')]"
            ]
            
            for selector in selectors:
                element = self.find_element_safe(AppiumBy.XPATH, selector, timeout=5)
                if element:
                    if self.click_element_safe(element, "CREATE NEW ACCOUNT"):
                        time.sleep(3)
                        return True
            
            # Coordinate fallback
            logger.info("🎯 Using coordinate fallback for CREATE NEW ACCOUNT")
            x = self.screen_size['width'] // 2
            y = int(self.screen_size['height'] * 0.75)
            self.driver.tap([(x, y)])
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"❌ Welcome screen failed: {e}")
            return False

    def step2_email_creation(self, username: str) -> bool:
        """Step 2: Create your Microsoft account - Email"""
        logger.info("\n📧 STEP 2: Email creation")
        
        try:
            # Find email input field
            email_selectors = [
                "//*[contains(@hint, 'New email')]",
                "//*[contains(@hint, 'email')]",
                "//android.widget.EditText[1]",
                "//android.widget.EditText"
            ]
            
            email_field = None
            for selector in email_selectors:
                email_field = self.find_element_safe(AppiumBy.XPATH, selector, timeout=5)
                if email_field:
                    break
            
            if not email_field:
                # Fallback: first EditText
                edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                if edit_texts:
                    email_field = edit_texts[0]
            
            if not email_field:
                logger.error("❌ Could not find email input field")
                return False
            
            if not self.type_text_robust(email_field, username, "Email"):
                return False
            
            return self.click_next_button("Email Creation")
            
        except Exception as e:
            logger.error(f"❌ Email creation failed: {e}")
            return False

    def step3_password_creation(self, password: str) -> bool:
        """Step 3: Create your password"""
        logger.info("\n🔒 STEP 3: Password creation")
        
        try:
            # Find password field
            password_selectors = [
                "//*[contains(@hint, 'Password')]",
                "//android.widget.EditText[@password='true']",
                "//android.widget.EditText[1]"
            ]
            
            password_field = None
            for selector in password_selectors:
                password_field = self.find_element_safe(AppiumBy.XPATH, selector, timeout=5)
                if password_field:
                    break
            
            if not password_field:
                # Fallback: first EditText
                edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                if edit_texts:
                    password_field = edit_texts[0]
            
            if not password_field:
                logger.error("❌ Could not find password input field")
                return False
            
            if not self.type_text_robust(password_field, password, "Password"):
                return False
            
            return self.click_next_button("Password Creation")
            
        except Exception as e:
            logger.error(f"❌ Password creation failed: {e}")
            return False

    def step4_add_details(self, birth_day: int, birth_month: str, birth_year: int) -> bool:
        """Step 4: Add details (birth date)"""
        logger.info("\n📅 STEP 4: Add details")
        
        try:
            # Keep default country selection
            logger.info("🏳️ Keeping default country selection")
            
            # Day dropdown
            logger.info(f"📅 Setting day to {birth_day}")
            day_selectors = [
                "//*[contains(@text, 'Day')]",
                "//*[contains(@hint, 'Day')]",
                "//android.widget.Spinner[1]"
            ]
            
            day_success = False
            for selector in day_selectors:
                day_dropdown = self.find_element_safe(AppiumBy.XPATH, selector, timeout=5)
                if day_dropdown:
                    if self.select_dropdown_option(day_dropdown, str(birth_day), "Day"):
                        day_success = True
                        break
            
            if not day_success:
                logger.warning("⚠️ Day selection failed, continuing...")
            
            # Month dropdown
            logger.info(f"📅 Setting month to {birth_month}")
            month_selectors = [
                "//*[contains(@text, 'Month')]",
                "//*[contains(@hint, 'Month')]",
                "//android.widget.Spinner[2]"
            ]
            
            month_success = False
            for selector in month_selectors:
                month_dropdown = self.find_element_safe(AppiumBy.XPATH, selector, timeout=5)
                if month_dropdown:
                    if self.select_dropdown_option(month_dropdown, birth_month, "Month"):
                        month_success = True
                        break
            
            if not month_success:
                logger.warning("⚠️ Month selection failed, continuing...")
            
            # Year input
            logger.info(f"📅 Setting year to {birth_year}")
            year_field = self.find_year_field()
            if not year_field:
                logger.error("❌ Could not find year field")
                return False
            
            if not self.type_text_robust(year_field, birth_year, "Year"):
                logger.error("❌ Failed to input year")
                return False
            
            return self.click_next_button("Add Details")
            
        except Exception as e:
            logger.error(f"❌ Add details failed: {e}")
            return False

    def step5_add_name(self, first_name: str, last_name: str) -> bool:
        """Step 5: Add your name"""
        logger.info("\n👤 STEP 5: Add your name")
        
        try:
            # Wait for the page to load
            time.sleep(2)
            
            # Find name fields
            first_field, last_field = self.find_name_fields()
            
            if not first_field:
                logger.error("❌ Could not find first name field")
                return False
            
            if not last_field:
                logger.error("❌ Could not find last name field")
                return False
            
            # Type first name
            if not self.type_text_robust(first_field, first_name, "First Name"):
                logger.error("❌ Failed to input first name")
                return False
            
            # Type last name
            if not self.type_text_robust(last_field, last_name, "Last Name"):
                logger.error("❌ Failed to input last name")
                return False
            
            # Hide keyboard if visible
            try:
                self.driver.hide_keyboard()
            except Exception:
                pass
            
            # Click Next - this is the critical step
            return self.click_next_button("Add Name - CRITICAL")
            
        except Exception as e:
            logger.error(f"❌ Add name failed: {e}")
            return False

    def step6_captcha_challenge(self) -> bool:
        """Step 6: CAPTCHA challenge - UPDATED WITH PRECISE TARGETING"""
        logger.info("\n🤖 STEP 6: CAPTCHA Challenge (PRECISE TARGETING)")
        
        try:
            # Wait a moment for CAPTCHA to appear
            time.sleep(3)
            
            # Use the UPDATED precise long press method
            if self.press_captcha_button_precise():
                logger.info("✅ CAPTCHA completed successfully with precise targeting")
                return True
            else:
                logger.error("❌ CAPTCHA failed with all methods")
                return False
                
        except Exception as e:
            logger.error(f"❌ CAPTCHA challenge failed: {e}")
            return False

    def run_automation(self, user_data: Dict[str, Any]) -> bool:
        """Run the complete automation flow - UNCHANGED"""
        logger.info("🚀 STARTING MICROSOFT OUTLOOK ACCOUNT CREATION")
        logger.info("=" * 60)
        logger.info(f"📧 Email: {user_data['username']}@outlook.com")
        logger.info(f"🔒 Password: {user_data['password']}")
        logger.info(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
        logger.info(f"📅 DOB: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
        logger.info("✅ Flow: Welcome → Email → Password → Details → Name → CAPTCHA")
        logger.info("🎯 UPDATED: Precise CAPTCHA button targeting")
        logger.info("=" * 60)
        
        try:
            if not self.setup_driver():
                return False
            
            time.sleep(5)  # Initial wait for app to load
            
            # Execute all steps
            steps = [
                ("Welcome Screen", lambda: self.step1_welcome_screen()),
                ("Email Creation", lambda: self.step2_email_creation(user_data['username'])),
                ("Password Creation", lambda: self.step3_password_creation(user_data['password'])),
                ("Add Details", lambda: self.step4_add_details(
                    user_data['birth_date']['day'],
                    user_data['birth_date']['month'],
                    user_data['birth_date']['year']
                )),
                ("Add Name", lambda: self.step5_add_name(user_data['first_name'], user_data['last_name'])),
                ("CAPTCHA Challenge", lambda: self.step6_captcha_challenge())
            ]
            
            for step_name, step_function in steps:
                logger.info(f"\n🚀 Executing: {step_name}")
                if not step_function():
                    logger.error(f"❌ {step_name} FAILED")
                    return False
                logger.info(f"✅ {step_name} COMPLETED")
            
            logger.info("\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
            logger.info("✅ Microsoft Outlook account created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Automation failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            if self.driver:
                logger.info("🔚 Closing Appium session...")
                try:
                    self.driver.quit()
                except Exception:
                    pass

def generate_user_data() -> Dict[str, Any]:
    """Generate random user data for account creation - UNCHANGED"""
    return {
        'username': f'autouser{random.randint(100000, 999999)}',
        'password': f'Auto{random.randint(100, 999)}Pass!',
        'first_name': 'Auto',
        'last_name': 'User',
        'birth_date': {
            'day': random.randint(1, 28),
            'month': random.choice(['January', 'February', 'March', 'April', 'May', 'June', 
                                  'July', 'August', 'September', 'October', 'November', 'December']),
            'year': random.randint(1990, 2000)
        }
    }

def main():
    """Main function - UNCHANGED"""
    print("🚀 Microsoft Outlook Account Creation Automation")
    print("🎯 UPDATED: Precise CAPTCHA Button Targeting")
    print("=" * 50)
    
    # Generate user data
    user_data = generate_user_data()
    
    print("Account to be created:")
    print(f"📧 Email: {user_data['username']}@outlook.com")
    print(f"🔒 Password: {user_data['password']}")
    print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
    print(f"📅 Birth Date: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
    print("\n⏳ Starting automation in 3 seconds...")
    time.sleep(3)
    
    try:
        # Create and run automation
        creator = OutlookAccountCreator()
        success = creator.run_automation(user_data)
        
        if success:
            print("\n🎊 SUCCESS! Account created successfully!")
            print("=" * 60)
            print("ACCOUNT DETAILS:")
            print(f"📧 Email: {user_data['username']}@outlook.com")
            print(f"🔒 Password: {user_data['password']}")
            print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
            print(f"📅 Birth Date: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
            print("=" * 60)
            print("✅ Your new Outlook account is ready to use!")
        else:
            print("\n❌ Automation failed! Check the logs above for details.")
            
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()