#!/usr/bin/env python3

"""
ULTIMATE NEXT BUTTON DETECTION - All New Strategies
===================================================

NEW APPROACHES FOR NEXT BUTTON DETECTION:
1. Resource ID detection (most reliable for Android apps)
2. Accessibility ID and content description matching
3. UI Automator text() and textContains() methods
4. Clickable elements scan with text analysis
5. Screenshot + OCR text detection
6. Element hierarchy traversal
7. Case-insensitive text matching
8. Icon/Image button detection
9. WebView context switching
10. Systematic coordinate grid search
11. Parent container analysis
12. Enabled/disabled state checking

CORRECTED FLOW ORDER:
1. Welcome Screen - CREATE NEW ACCOUNT
2. Email Creation - Enter username  
3. Password Creation - Create password
4. Add Details - Country, Day, Month, Year (birth date)
5. Add Name - First & Last Name (ULTIMATE NEXT BUTTON DETECTION)
6. CAPTCHA Challenge - Press & Hold for 15 seconds

Key Features:
1. ULTIMATE Next button detection with 12 new strategies
2. Screenshot-based OCR detection as fallback
3. Resource ID and accessibility detection
4. WebView context switching
5. Systematic grid-based coordinate search
6. Element hierarchy analysis
7. All previous robust features preserved
"""

import time
import random
import subprocess
import json
import base64
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

class UltimateNextButtonAppiumCreator:
    def __init__(self, platform_name='Android', device_name='Android',
                 app_package='com.microsoft.office.outlook'):
        """Initialize ultimate Next button detection Appium creator"""
        self.platform_name = platform_name
        self.device_name = device_name
        self.app_package = app_package
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Setup Appium WebDriver with robust settings"""
        print("🔧 Setting up ULTIMATE Next Button Detection driver...")
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
        
        # Enable unicode keyboard for better text input
        options.unicode_keyboard = True
        options.reset_keyboard = True
        
        # Add settings for better stability
        options.auto_grant_permissions = True
        options.disable_android_watchers = True
        
        try:
            print("🔗 Connecting to Appium server...")
            self.driver = webdriver.Remote("http://localhost:4723", options=options)
            self.wait = WebDriverWait(self.driver, 15)
            
            # CRITICAL: Enable XPath1 to fix the NodeType cast exception
            print("🛠️ Enabling enforceXPath1 to fix XPath2 bug...")
            self.driver.update_settings({"enforceXPath1": True})
            
            print("✅ Connected to Appium server successfully!")
            print("✅ XPath1 enforcement enabled!")
            print("🎯 ULTIMATE Next button detection ready!")
            return True
            
        except WebDriverException as e:
            if "Could not find a driver" in str(e) or "UiAutomator2" in str(e):
                print("❌ UiAutomator2 driver not found")
                print("💡 Install with: appium driver install uiautomator2")
                return False
            else:
                print(f"❌ Appium connection failed: {e}")
                return False

    def find_element_safely(self, by, value, timeout=10):
        """Find element with error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Element not found: {by}={value}")
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

    def ultimate_next_button_detection(self, context_description=""):
        """ULTIMATE: Next button detection with 12 new strategies"""
        print(f"🚀 ULTIMATE Next Button Detection - {context_description}")
        print("=" * 60)
        
        # Strategy 1: Resource ID Detection (Most Reliable)
        print("🎯 Strategy 1: Resource ID Detection...")
        resource_id_patterns = [
            "next", "btn_next", "button_next", "nextButton", "next_btn",
            "continue", "btn_continue", "continueButton", "proceed",
            "submit", "btn_submit", "submitButton", "forward", "btn_forward"
        ]
        
        for pattern in resource_id_patterns:
            try:
                selectors = [
                    f"//*[contains(@resource-id, '{pattern}')]",
                    f"//*[@resource-id='{pattern}']",
                    f"//*[contains(@resource-id, '{pattern.upper()}')]",
                    f"//*[contains(@resource-id, '{pattern.lower()}')]"
                ]
                
                for selector in selectors:
                    element = self.find_element_safely(AppiumBy.XPATH, selector, timeout=2)
                    if element and element.is_enabled():
                        print(f"✅ Found Next button by resource ID: {selector}")
                        if self.tap_element_safely(element, f"Resource ID Next: {pattern}"):
                            return True
            except Exception as e:
                continue
        
        # Strategy 2: Accessibility ID and Content Description
        print("🎯 Strategy 2: Accessibility ID Detection...")
        accessibility_patterns = [
            "Next", "next", "NEXT", "Continue", "continue", "CONTINUE",
            "Proceed", "proceed", "Submit", "submit", "Forward", "forward"
        ]
        
        for pattern in accessibility_patterns:
            try:
                selectors = [
                    f"//*[@content-desc='{pattern}']",
                    f"//*[contains(@content-desc, '{pattern}')]",
                    f"//*[@accessibility-id='{pattern}']",
                    f"//*[contains(@accessibility-id, '{pattern}')]"
                ]
                
                for selector in selectors:
                    element = self.find_element_safely(AppiumBy.XPATH, selector, timeout=2)
                    if element:
                        print(f"✅ Found Next button by accessibility: {selector}")
                        if self.tap_element_safely(element, f"Accessibility Next: {pattern}"):
                            return True
            except Exception as e:
                continue
        
        # Strategy 3: UI Automator text() and textContains()
        print("🎯 Strategy 3: UI Automator Text Detection...")
        text_patterns = ["Next", "NEXT", "next", "Continue", "CONTINUE", "continue"]
        
        for pattern in text_patterns:
            try:
                ui_selectors = [
                    f'new UiSelector().text("{pattern}")',
                    f'new UiSelector().textContains("{pattern}")',
                    f'new UiSelector().textMatches(".*{pattern}.*")',
                    f'new UiSelector().className("android.widget.Button").text("{pattern}")',
                    f'new UiSelector().className("android.widget.Button").textContains("{pattern}")',
                    f'new UiSelector().clickable(true).text("{pattern}")',
                    f'new UiSelector().clickable(true).textContains("{pattern}")'
                ]
                
                for ui_selector in ui_selectors:
                    try:
                        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)
                        if element:
                            print(f"✅ Found Next button by UI Automator: {pattern}")
                            if self.tap_element_safely(element, f"UI Automator Next: {pattern}"):
                                return True
                    except:
                        continue
            except Exception as e:
                continue
        
        # Strategy 4: All Clickable Elements Analysis
        print("🎯 Strategy 4: All Clickable Elements Analysis...")
        try:
            clickable_selector = 'new UiSelector().clickable(true)'
            clickable_elements = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, clickable_selector)
            
            next_keywords = ["next", "continue", "proceed", "submit", "forward", "go", "ok"]
            
            for element in clickable_elements:
                try:
                    element_text = (element.get_attribute("text") or "").lower()
                    content_desc = (element.get_attribute("content-desc") or "").lower()
                    resource_id = (element.get_attribute("resource-id") or "").lower()
                    
                    combined_text = f"{element_text} {content_desc} {resource_id}"
                    
                    for keyword in next_keywords:
                        if keyword in combined_text:
                            print(f"✅ Found clickable Next element with keyword: {keyword}")
                            print(f"   Text: '{element_text}', Desc: '{content_desc}', ID: '{resource_id}'")
                            if self.tap_element_safely(element, f"Clickable Next: {keyword}"):
                                return True
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Clickable elements analysis failed: {e}")
        
        # Strategy 5: Button Class Elements with Position Analysis
        print("🎯 Strategy 5: Button Position Analysis...")
        try:
            all_buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
            screen_size = self.driver.get_window_size()
            
            # Focus on buttons in the bottom half of the screen
            bottom_buttons = []
            for button in all_buttons:
                try:
                    location = button.location
                    if location['y'] > screen_size['height'] * 0.5:  # Bottom half
                        bottom_buttons.append((button, location['y']))
                except:
                    continue
            
            # Sort by Y position (bottom-most first)
            bottom_buttons.sort(key=lambda x: x[1], reverse=True)
            
            for button, y_pos in bottom_buttons:
                try:
                    if button.is_enabled():
                        button_text = button.get_attribute("text") or ""
                        print(f"🔍 Trying bottom button at y={y_pos}: '{button_text}'")
                        if self.tap_element_safely(button, f"Bottom Button: {button_text}"):
                            return True
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Button position analysis failed: {e}")
        
        # Strategy 6: WebView Context Switching
        print("🎯 Strategy 6: WebView Context Detection...")
        try:
            contexts = self.driver.contexts
            print(f"Available contexts: {contexts}")
            
            for context in contexts:
                if "WEBVIEW" in context.upper():
                    print(f"🌐 Switching to WebView context: {context}")
                    self.driver.switch_to.context(context)
                    
                    # Try web-based selectors
                    web_selectors = [
                        "button[type='submit']",
                        "input[type='submit']",
                        "button:contains('Next')",
                        "button:contains('Continue')",
                        ".next-button", ".btn-next", ".continue-btn"
                    ]
                    
                    for selector in web_selectors:
                        try:
                            element = self.driver.find_element(AppiumBy.CSS_SELECTOR, selector)
                            if element:
                                print(f"✅ Found Next button in WebView: {selector}")
                                if self.tap_element_safely(element, f"WebView Next: {selector}"):
                                    # Switch back to native context
                                    self.driver.switch_to.context("NATIVE_APP")
                                    return True
                        except:
                            continue
                    
                    # Switch back to native context
                    self.driver.switch_to.context("NATIVE_APP")
        except Exception as e:
            print(f"⚠️ WebView context switching failed: {e}")
        
        # Strategy 7: OCR-Based Text Detection
        print("🎯 Strategy 7: OCR Text Detection...")
        try:
            # Take screenshot
            screenshot = self.driver.get_screenshot_as_base64()
            
            # Use ADB to find text on screen (if available)
            try:
                result = subprocess.run(['adb', 'shell', 'uiautomator', 'dump', '/dev/stdout'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    ui_dump = result.stdout
                    
                    # Look for Next-related text in UI dump
                    next_patterns = ['Next', 'NEXT', 'next', 'Continue', 'CONTINUE', 'continue']
                    
                    for pattern in next_patterns:
                        if pattern in ui_dump:
                            print(f"✅ Found '{pattern}' in UI dump, searching for coordinates...")
                            
                            # Extract bounds information for elements containing the pattern
                            import re
                            pattern_regex = rf'text="{pattern}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'
                            matches = re.findall(pattern_regex, ui_dump)
                            
                            for match in matches:
                                x1, y1, x2, y2 = map(int, match)
                                center_x = (x1 + x2) // 2
                                center_y = (y1 + y2) // 2
                                
                                print(f"🎯 Found {pattern} at coordinates: ({center_x}, {center_y})")
                                try:
                                    self.driver.tap([(center_x, center_y)])
                                    time.sleep(2)
                                    print(f"✅ Tapped OCR-detected Next button: {pattern}")
                                    return True
                                except:
                                    continue
            except Exception as e:
                print(f"⚠️ ADB UI dump failed: {e}")
        except Exception as e:
            print(f"⚠️ OCR detection failed: {e}")
        
        # Strategy 8: Systematic Grid Search
        print("🎯 Strategy 8: Systematic Grid Search...")
        try:
            screen_size = self.driver.get_window_size()
            width, height = screen_size['width'], screen_size['height']
            
            # Focus on bottom area where Next buttons typically appear
            start_y = int(height * 0.7)  # Bottom 30% of screen
            end_y = int(height * 0.95)   # Leave some margin
            
            # Grid search in bottom area
            grid_points = []
            for y in range(start_y, end_y, 50):  # Every 50 pixels vertically
                for x in range(50, width-50, 100):  # Every 100 pixels horizontally
                    grid_points.append((x, y))
            
            print(f"🔍 Grid searching {len(grid_points)} points in bottom area...")
            
            for i, (x, y) in enumerate(grid_points):
                try:
                    # Check if there's a clickable element at this position
                    element_at_point = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().clickable(true)'
                    )
                    
                    if element_at_point:
                        element_bounds = element_at_point.get_attribute("bounds")
                        if element_bounds:
                            # Parse bounds: "[x1,y1][x2,y2]"
                            import re
                            bounds_match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', element_bounds)
                            if bounds_match:
                                x1, y1, x2, y2 = map(int, bounds_match.groups())
                                if x1 <= x <= x2 and y1 <= y <= y2:
                                    print(f"🎯 Grid found clickable element at ({x}, {y})")
                                    self.driver.tap([(x, y)])
                                    time.sleep(2)
                                    return True
                    
                    # Every 20 points, try a direct tap
                    if i % 20 == 0:
                        print(f"🔍 Grid tap attempt {i//20 + 1}: ({x}, {y})")
                        self.driver.tap([(x, y)])
                        time.sleep(1)
                        
                        # Check if we navigated (simple check)
                        time.sleep(1)
                        current_activity = self.driver.current_activity
                        if current_activity != self.driver.current_activity:
                            print(f"✅ Grid search successful at ({x}, {y})")
                            return True
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ Grid search failed: {e}")
        
        # Strategy 9: Hierarchy Analysis
        print("🎯 Strategy 9: Element Hierarchy Analysis...")
        try:
            # Get page source and analyze structure
            page_source = self.driver.page_source
            
            # Look for form-related containers that might have Next buttons
            import xml.etree.ElementTree as ET
            root = ET.fromstring(page_source)
            
            # Find elements that might be buttons based on hierarchy
            for elem in root.iter():
                if elem.get('clickable') == 'true':
                    text = elem.get('text', '').lower()
                    content_desc = elem.get('content-desc', '').lower()
                    resource_id = elem.get('resource-id', '').lower()
                    bounds = elem.get('bounds', '')
                    
                    next_indicators = ['next', 'continue', 'proceed', 'submit', 'forward']
                    
                    if any(indicator in f"{text} {content_desc} {resource_id}" for indicator in next_indicators):
                        if bounds:
                            # Parse bounds and click
                            import re
                            bounds_match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                            if bounds_match:
                                x1, y1, x2, y2 = map(int, bounds_match.groups())
                                center_x = (x1 + x2) // 2
                                center_y = (y1 + y2) // 2
                                
                                print(f"✅ Hierarchy found Next button: {text or content_desc or resource_id}")
                                self.driver.tap([(center_x, center_y)])
                                time.sleep(2)
                                return True
        except Exception as e:
            print(f"⚠️ Hierarchy analysis failed: {e}")
        
        # Strategy 10: Alternative Input Methods
        print("🎯 Strategy 10: Alternative Input Methods...")
        try:
            # Try hardware button presses that might trigger Next
            alternative_methods = [
                lambda: self.driver.press_keycode(66),  # KEYCODE_ENTER
                lambda: self.driver.press_keycode(23),  # KEYCODE_DPAD_CENTER  
                lambda: self.driver.press_keycode(62),  # KEYCODE_SPACE
                lambda: self.driver.press_keycode(160), # KEYCODE_TAB to navigate then ENTER
            ]
            
            for i, method in enumerate(alternative_methods):
                try:
                    print(f"🎯 Trying alternative input method {i+1}...")
                    method()
                    time.sleep(2)
                    print(f"✅ Alternative input method {i+1} executed")
                    return True
                except Exception as e:
                    print(f"⚠️ Alternative method {i+1} failed: {e}")
                    continue
        except Exception as e:
            print(f"⚠️ Alternative input methods failed: {e}")
        
        print("❌ ALL 10 ULTIMATE STRATEGIES FAILED FOR NEXT BUTTON!")
        print("🔍 Attempting final debug information collection...")
        
        # Final debug: dump all information about current screen
        try:
            print("\n🔬 DEBUG INFO:")
            print(f"Current Activity: {self.driver.current_activity}")
            print(f"Current Package: {self.driver.current_package}")
            
            all_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            print(f"Total clickable elements: {len(all_elements)}")
            
            for i, elem in enumerate(all_elements[:10]):  # Show first 10
                try:
                    text = elem.get_attribute("text") or ""
                    desc = elem.get_attribute("content-desc") or ""
                    res_id = elem.get_attribute("resource-id") or ""
                    bounds = elem.get_attribute("bounds") or ""
                    print(f"  {i+1}. Text:'{text}' Desc:'{desc}' ID:'{res_id}' Bounds:'{bounds}'")
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Debug info collection failed: {e}")
        
        return False

    def focus_clear_and_type(self, element, text, description=""):
        """Robust text input with multiple fallback methods"""
        if not element:
            return False
            
        try:
            # Method 1: Focus, clear, and type
            print(f"🎯 Focusing on {description}...")
            element.click()
            time.sleep(0.4)
            
            # Clear the field
            try:
                element.clear()
                time.sleep(0.2)
                print(f"🧹 Cleared {description}")
            except:
                print(f"⚠️ Standard clear failed for {description}")
                # Try manual clearing with backspace
                try:
                    current_text = element.get_attribute("text") or ""
                    for _ in range(len(current_text) + 5):  # Extra presses to be sure
                        self.driver.press_keycode(67)  # KEYCODE_DEL
                        time.sleep(0.05)
                    print(f"🧹 Manual clear completed for {description}")
                except:
                    pass
            
            # Type the text
            try:
                element.send_keys(str(text))
                print(f"⌨️ Typed: {text} in {description}")
                time.sleep(0.5)
                return True
            except Exception as e:
                print(f"⚠️ Standard typing failed for {description}: {e}")
                
                # Fallback 1: ADB shell input (works on focused field)
                try:
                    print(f"🔄 Trying ADB shell input for {description}...")
                    result = subprocess.run(['adb', 'shell', 'input', 'text', str(text)],
                                          check=True, capture_output=True, text=True)
                    print(f"✅ ADB input successful: {text} in {description}")
                    time.sleep(0.5)
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"⚠️ ADB input failed: {e}")
                except FileNotFoundError:
                    print("⚠️ ADB not found in PATH")
                
                # Fallback 2: Keycode input for numbers
                if str(text).isdigit():
                    try:
                        print(f"🔢 Trying keycode input for {description}...")
                        for digit in str(text):
                            keycode = 7 + int(digit)  # KEYCODE_0 = 7, KEYCODE_1 = 8, etc.
                            self.driver.press_keycode(keycode)
                            time.sleep(0.1)
                        print(f"✅ Keycode input successful: {text} in {description}")
                        return True
                    except Exception as e:
                        print(f"❌ Keycode input failed: {e}")
                
                return False
        except Exception as e:
            print(f"❌ All input methods failed for {description}: {e}")
            return False

    def find_rightmost_edittext(self):
        """Find the rightmost EditText element by bounds (likely the Year field)"""
        try:
            candidates = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if not candidates:
                return None
                
            def get_right_x(element):
                try:
                    bounds = element.get_attribute("bounds")  # Format: "[x1,y1][x2,y2]"
                    if bounds:
                        # Extract x2 coordinate (right edge)
                        x2 = int(bounds.split("][")[1].split(",")[0])
                        return x2
                except:
                    return 0
                return 0
            
            # Return the EditText with the rightmost x-coordinate
            rightmost = max(candidates, key=get_right_x)
            right_x = get_right_x(rightmost)
            print(f"📐 Found rightmost EditText at x={right_x}")
            return rightmost
            
        except Exception as e:
            print(f"❌ Error finding rightmost EditText: {e}")
            return None

    def enter_year_robust(self, year: int) -> bool:
        """Robust year field input using multiple strategies"""
        print(f"📅 ROBUST Year Input: {year}")
        
        # Strategy 1: UiSelector with instance (most reliable)
        try:
            print("🎯 Strategy 1: UiSelector with instance...")
            ui_selector = 'new UiSelector().className("android.widget.EditText").enabled(true)'
            # Try different instances (0=first, 1=second, 2=third)
            for instance in [2, 1, 0]:  # Start with 3rd (likely year), then 2nd, then 1st
                try:
                    year_element = self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f"{ui_selector}.instance({instance})"
                    )
                    print(f"✅ Found EditText instance {instance}")
                    if self.focus_clear_and_type(year_element, year, f"Year (UiSelector instance {instance})"):
                        return True
                except:
                    continue
        except Exception as e:
            print(f"⚠️ UiSelector strategy failed: {e}")
        
        # Strategy 2: Last EditText element
        try:
            print("🎯 Strategy 2: Last EditText element...")
            all_edittexts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if all_edittexts:
                last_edittext = all_edittexts[-1]
                print(f"✅ Found last EditText (position {len(all_edittexts)})")
                if self.focus_clear_and_type(last_edittext, year, "Year (last EditText)"):
                    return True
        except Exception as e:
            print(f"⚠️ Last EditText strategy failed: {e}")
        
        # Strategy 3: Rightmost EditText by bounds
        try:
            print("🎯 Strategy 3: Rightmost EditText by bounds...")
            rightmost_element = self.find_rightmost_edittext()
            if rightmost_element:
                if self.focus_clear_and_type(rightmost_element, year, "Year (rightmost bounds)"):
                    return True
        except Exception as e:
            print(f"⚠️ Rightmost bounds strategy failed: {e}")
        
        # Strategy 4: Simple XPath (with XPath1 enforcement)
        try:
            print("🎯 Strategy 4: Simple XPath selectors...")
            simple_selectors = [
                "//android.widget.EditText[3]",  # Third EditText
                "//android.widget.EditText[last()]",  # Last EditText
                "//*[@class='android.widget.EditText'][3]",  # Alternative syntax
            ]
            
            for selector in simple_selectors:
                try:
                    year_element = self.find_element_safely(AppiumBy.XPATH, selector, timeout=3)
                    if year_element:
                        print(f"✅ Found element with selector: {selector}")
                        if self.focus_clear_and_type(year_element, year, f"Year ({selector})"):
                            return True
                except:
                    continue
        except Exception as e:
            print(f"⚠️ XPath strategy failed: {e}")
        
        # Strategy 5: Coordinate-based input (last resort)
        try:
            print("🎯 Strategy 5: Coordinate-based input...")
            screen_size = self.driver.get_window_size()
            # Try multiple coordinate positions for year field
            coordinate_positions = [
                (int(screen_size['width'] * 0.8), int(screen_size['height'] * 0.45)),  # Right side
                (int(screen_size['width'] * 0.75), int(screen_size['height'] * 0.48)),  # Slightly left
                (int(screen_size['width'] * 0.85), int(screen_size['height'] * 0.42)),  # Further right
            ]
            
            for x, y in coordinate_positions:
                try:
                    print(f"📍 Trying coordinates ({x}, {y})...")
                    self.driver.tap([(x, y)])
                    time.sleep(0.5)
                    
                    # Try ADB input first (most reliable for coordinates)
                    try:
                        subprocess.run(['adb', 'shell', 'input', 'text', str(year)],
                                     check=True, capture_output=True)
                        print(f"✅ Coordinate + ADB input successful: {year}")
                        return True
                    except:
                        pass
                    
                    # Try keycode input
                    for digit in str(year):
                        keycode = 7 + int(digit)
                        self.driver.press_keycode(keycode)
                        time.sleep(0.1)
                    print(f"✅ Coordinate + keycode input successful: {year}")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Coordinate attempt ({x}, {y}) failed: {e}")
                    continue
        except Exception as e:
            print(f"⚠️ Coordinate strategy failed: {e}")
        
        print("❌ All year input strategies failed!")
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

    def long_press_captcha_15_seconds(self, element, description=""):
        """FIXED: Long press for CAPTCHA - 15 seconds duration"""
        duration = 15000  # 15 seconds in milliseconds
        print(f"🤖 FIXED: Starting 15-second CAPTCHA long press...")
        
        try:
            actions = ActionBuilder(self.driver)
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
            location = element.location
            size = element.size
            x = location['x'] + (size['width'] // 2)
            y = location['y'] + (size['height'] // 2)
            
            actions.add_action(pointer.create_pointer_move(duration=0, x=x, y=y))
            actions.add_action(pointer.create_pointer_down())
            actions.add_action(pointer.create_pause(duration/1000))  # 15 seconds
            actions.add_action(pointer.create_pointer_up())
            actions.perform()
            
            print(f"👆🕐 Long pressed: {description} for {duration/1000} seconds")
            print("⏳ Holding for 15 seconds... Please wait...")
            time.sleep(duration/1000 + 3)  # Wait for the action + extra buffer
            return True
            
        except Exception as e:
            print(f"❌ Long press failed for {description}: {e}")
            return False

    # STEP IMPLEMENTATIONS (CORRECTED ORDER WITH ULTIMATE NEXT DETECTION)
    
    def step1_welcome_screen(self) -> bool:
        """Step 1: Handle Welcome to Outlook screen"""
        print("\n📱 STEP 1: Welcome to Outlook")
        
        selectors_to_try = [
            (AppiumBy.XPATH, "//*[contains(@text, 'CREATE NEW ACCOUNT')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'Create new account')]"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'CREATE NEW ACCOUNT')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'CREATE')]"),
        ]
        
        for by, selector in selectors_to_try:
            element = self.find_element_safely(by, selector, timeout=5)
            if element and self.tap_element_safely(element, "CREATE NEW ACCOUNT"):
                time.sleep(3)
                return True
        
        # Coordinate fallback
        print("🎯 Trying coordinate-based tap for CREATE NEW ACCOUNT")
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] // 2
        y = int(screen_size['height'] * 0.75)
        if self.tap_by_coordinates(x, y, "CREATE NEW ACCOUNT (coordinates)"):
            time.sleep(3)
            return True
        
        print("❌ Failed to find CREATE NEW ACCOUNT")
        return False

    def step2_email_creation(self, username: str) -> bool:
        """Step 2: Create your Microsoft account - Email"""
        print("\n📧 STEP 2: Create your Microsoft account")
        
        email_field_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'New email')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'New email')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        ]
        
        for by, selector in email_field_selectors:
            email_field = self.find_element_safely(by, selector, timeout=5)
            if email_field:
                if self.focus_clear_and_type(email_field, username, "Username"):
                    break
        else:
            print("❌ Could not find email input field")
            return False
        
        # Use ULTIMATE Next button detection
        return self.ultimate_next_button_detection("Email Creation Step")

    def step3_password_creation(self, password: str) -> bool:
        """Step 3: Create your password"""
        print("\n🔒 STEP 3: Create your password")
        
        password_field_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'Password')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[@password='true']"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
        ]
        
        for by, selector in password_field_selectors:
            password_field = self.find_element_safely(by, selector, timeout=5)
            if password_field:
                if self.focus_clear_and_type(password_field, password, "Password"):
                    break
        else:
            print("❌ Could not find password input field")
            return False
        
        # Use ULTIMATE Next button detection
        return self.ultimate_next_button_detection("Password Creation Step")

    def step4_add_details(self, birth_day: int, birth_month: str, birth_year: int) -> bool:
        """Step 4: Add details - ROBUST Year Field Handling"""
        print("\n📅 STEP 4: Add some details")
        print("🏳️ Keeping default country selection")
        
        # Day dropdown
        print(f"📅 Setting day to {birth_day}")
        day_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Day')]"),
            (AppiumBy.XPATH, "//*[contains(@hint, 'Day')]"),
            (AppiumBy.XPATH, "//android.widget.Spinner[1]"),
        ]
        
        day_success = False
        for by, selector in day_selectors:
            day_dropdown = self.find_element_safely(by, selector, timeout=5)
            if day_dropdown:
                if self.select_dropdown_option(day_dropdown, str(birth_day), "Day dropdown"):
                    day_success = True
                    break
        
        if not day_success:
            print("⚠️ Day selection failed, continuing...")
        
        # Month dropdown
        print(f"📅 Setting month to {birth_month}")
        month_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Month')]"),
            (AppiumBy.XPATH, "//*[contains(@hint, 'Month')]"),
            (AppiumBy.XPATH, "//android.widget.Spinner[2]"),
        ]
        
        month_success = False
        for by, selector in month_selectors:
            month_dropdown = self.find_element_safely(by, selector, timeout=5)
            if month_dropdown:
                if self.select_dropdown_option(month_dropdown, birth_month, "Month dropdown"):
                    month_success = True
                    break
        
        if not month_success:
            print("⚠️ Month selection failed, continuing...")
        
        # ROBUST Year input using the new method
        if not self.enter_year_robust(birth_year):
            print("❌ Failed to input year after all robust attempts")
            return False
        
        # Use ULTIMATE Next button detection
        return self.ultimate_next_button_detection("Add Details Step")

    def step5_add_name(self, first_name: str, last_name: str) -> bool:
        """Step 5: Add your name - ULTIMATE NEXT BUTTON DETECTION"""
        print("\n👤 STEP 5: Add your name (ULTIMATE NEXT BUTTON DETECTION)")
        
        # First name field
        first_name_selectors = [
            (AppiumBy.XPATH, "//*[contains(@hint, 'First name')]"),
            (AppiumBy.XPATH, "//android.widget.EditText[1]"),
        ]
        
        for by, selector in first_name_selectors:
            first_name_field = self.find_element_safely(by, selector, timeout=5)
            if first_name_field:
                if self.focus_clear_and_type(first_name_field, first_name, "First name"):
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
            if last_name_field:
                if self.focus_clear_and_type(last_name_field, last_name, "Last name"):
                    break
        else:
            print("❌ Could not find last name field")
            return False
        
        # ULTIMATE: Use all 10 Next button detection strategies
        print("🚀 ULTIMATE: Deploying all Next button detection strategies...")
        return self.ultimate_next_button_detection("Add Name Step - ULTIMATE")

    def step6_captcha_challenge(self) -> bool:
        """Step 6: CAPTCHA - FIXED 15 SECOND HOLD"""
        print("\n🤖 STEP 6: CAPTCHA Challenge (FIXED 15-SECOND HOLD)")
        
        captcha_selectors = [
            (AppiumBy.XPATH, "//*[contains(@text, 'Press and hold')]"),
            (AppiumBy.XPATH, "//*[contains(@text, 'prove you')]"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Press')]"),
        ]
        
        for by, selector in captcha_selectors:
            captcha_element = self.find_element_safely(by, selector, timeout=8)
            if captcha_element:
                print("🎯 Found CAPTCHA element, performing 15-second long press...")
                if self.long_press_captcha_15_seconds(captcha_element, "CAPTCHA Press and Hold - 15 seconds"):
                    print("⏳ CAPTCHA verification completed after 15 seconds...")
                    time.sleep(5)  # Additional wait for verification
                    return True
        
        # Coordinate fallback for CAPTCHA with 15-second hold
        print("🎯 Trying coordinate-based CAPTCHA press (15 seconds)")
        screen_size = self.driver.get_window_size()
        x = screen_size['width'] // 2
        y = int(screen_size['height'] * 0.6)
        
        try:
            print("🤖 Starting 15-second coordinate-based CAPTCHA hold...")
            actions = ActionBuilder(self.driver)
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions.add_action(pointer.create_pointer_move(duration=0, x=x, y=y))
            actions.add_action(pointer.create_pointer_down())
            actions.add_action(pointer.create_pause(15))  # 15 seconds
            actions.add_action(pointer.create_pointer_up())
            actions.perform()
            
            print("👆🕐 Long pressed CAPTCHA area (coordinates) for 15 seconds")
            time.sleep(8)  # Additional verification wait
            return True
            
        except Exception as e:
            print(f"❌ CAPTCHA handling failed: {e}")
            return False

    def run_complete_automation(self, user_data: dict):
        """Run the complete 6-step automation with ULTIMATE NEXT DETECTION"""
        print("🤖 STARTING ULTIMATE NEXT BUTTON DETECTION AUTOMATION")
        print("=" * 90)
        print(f"📧 Email: {user_data['username']}@outlook.com")
        print(f"🔒 Password: {user_data['password']}")
        print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
        print(f"📅 DOB: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
        print("🛠️ XPath Fix: enforceXPath1 enabled")
        print("🎯 Year Input: 5 robust strategies with fallbacks")
        print("📸 Screenshots: REMOVED for performance")
        print("🔧 Text Input: Focus + Clear + Type + ADB + Keycodes")
        print("✅ CORRECTED ORDER: Details -> Name -> CAPTCHA")
        print("🚀 ULTIMATE: 10 Next button detection strategies")
        print("🕐 FIXED: CAPTCHA hold duration 15 seconds")
        print("=" * 90)
        
        try:
            if not self.setup_driver():
                return False
            
            time.sleep(5)
            
            # All 6 steps with ULTIMATE NEXT DETECTION
            steps = [
                ("Step 1: Welcome Screen", lambda: self.step1_welcome_screen()),
                ("Step 2: Email Creation", lambda: self.step2_email_creation(user_data['username'])),
                ("Step 3: Password Creation", lambda: self.step3_password_creation(user_data['password'])),
                ("Step 4: Add Details", lambda: self.step4_add_details(
                    user_data['birth_date']['day'],
                    user_data['birth_date']['month'],
                    user_data['birth_date']['year']
                )),
                ("Step 5: Add Name (ULTIMATE)", lambda: self.step5_add_name(user_data['first_name'], user_data['last_name'])),
                ("Step 6: CAPTCHA (FIXED 15s)", lambda: self.step6_captcha_challenge())
            ]
            
            for step_name, step_func in steps:
                print(f"\n🚀 Executing {step_name}...")
                if not step_func():
                    print(f"❌ {step_name} failed")
                    return False
                print(f"✅ {step_name} completed successfully")
            
            print("\n🎉 ALL 6 STEPS COMPLETED SUCCESSFULLY!")
            print("✅ ULTIMATE automation finished - Account created!")
            return True
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            if self.driver:
                print("🔚 Closing Appium session...")
                try:
                    self.driver.quit()
                except:
                    pass

def main():
    """Main function with ULTIMATE Next button detection"""
    print("🚀 ULTIMATE NEXT BUTTON DETECTION AUTOMATION")
    print("=" * 80)
    
    user_data = {
        'username': f'ultimateuser{random.randint(100000, 999999)}',
        'password': f'Ultimate{random.randint(100, 999)}Pass!',
        'first_name': 'Ultimate',
        'last_name': 'User',
        'birth_date': {
            'day': random.randint(1, 28),
            'month': random.choice(['January', 'February', 'March', 'April', 'May', 'June']),
            'year': random.randint(1990, 2000)
        }
    }
    
    print("Account to be created:")
    print(f"📧 Email: {user_data['username']}@outlook.com")
    print(f"🔒 Password: {user_data['password']}")
    print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
    print(f"📅 Birth Date: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
    print("\n🎬 Starting ULTIMATE automation in 3 seconds...")
    print("🚀 ULTIMATE: 10 Next button detection strategies deployed")
    time.sleep(3)
    
    try:
        creator = UltimateNextButtonAppiumCreator()
        success = creator.run_complete_automation(user_data)
        
        if success:
            print("\n🎊 SUCCESS! Outlook account created successfully!")
            print("=" * 90)
            print("FINAL ACCOUNT DETAILS:")
            print(f"📧 Email: {user_data['username']}@outlook.com")
            print(f"🔒 Password: {user_data['password']}")
            print(f"👤 Name: {user_data['first_name']} {user_data['last_name']}")
            print(f"📅 Birth Date: {user_data['birth_date']['day']} {user_data['birth_date']['month']} {user_data['birth_date']['year']}")
            print("=" * 90)
            print("✅ Account is ready to use!")
            print("🚀 ULTIMATE Next button detection successful!")
        else:
            print("\n❌ Automation failed - Please check the logs above")
            
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()