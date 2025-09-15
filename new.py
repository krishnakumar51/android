#!/usr/bin/env python3

"""
Outlook account creation with fortified 15s long‑press
Flow: Welcome → Email → Password → Details → Name → CAPTCHA
"""

import time
import random
import subprocess
from typing import Optional, Tuple

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction


class OutlookCreatorV3:
    def __init__(self, platform_name='Android', device_name='Android', app_package='com.microsoft.office.outlook'):
        self.platform_name = platform_name
        self.device_name = device_name
        self.app_package = app_package
        self.driver = None
        self.wait = None
        self.size = None

    # ---------- Driver ----------
    def setup(self) -> bool:
        try:
            opts = UiAutomator2Options()
            opts.platform_name = self.platform_name
            opts.device_name = self.device_name
            opts.app_package = self.app_package
            opts.app_activity = '.MainActivity'
            opts.automation_name = 'UiAutomator2'
            opts.no_reset = False
            opts.full_reset = False
            opts.new_command_timeout = 300
            opts.android_device_ready_timeout = 60
            opts.android_app_wait_timeout = 60
            opts.unicode_keyboard = True
            opts.reset_keyboard = True
            opts.auto_grant_permissions = True

            self.driver = webdriver.Remote("http://localhost:4723", options=opts)
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.update_settings({"enforceXPath1": True})
            self.size = self.driver.get_window_size()
            return True
        except WebDriverException as e:
            print(f"❌ Setup failed: {e}")
            return False

    def _safe(self, by, value, timeout=12):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            return None

    # ---------- Generic helpers ----------
    def type_robust(self, el, text, label=""):
        try:
            el.click()
            time.sleep(0.3)
            try:
                el.clear()
            except Exception:
                cur = el.get_attribute("text") or ""
                for _ in range(len(cur) + 3):
                    self.driver.press_keycode(67)
            el.send_keys(str(text))
            time.sleep(0.4)
            return True
        except Exception as e:
            # ADB fallback
            try:
                subprocess.run(["adb", "shell", "input", "text", str(text)], check=True)
                time.sleep(0.4)
                return True
            except Exception:
                print(f"❌ Typing failed for {label}: {e}")
                return False

    def next_click(self, context=""):
        # 1) UiSelector textContains Next
        uis = [
            'new UiSelector().textContains("Next").clickable(true).enabled(true)',
            'new UiSelector().text("Next").clickable(true)',
            'new UiSelector().textMatches(".*Next.*").clickable(true)'
        ]
        for sel in uis:
            try:
                el = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, sel))
                )
                el.click()
                time.sleep(2)
                return True
            except Exception:
                pass

        # 2) XPath
        xps = ["//*[@text='Next']", "//*[contains(@text,'Next')]", "//android.widget.Button[contains(@text,'Next')]"]
        for xp in xps:
            try:
                el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, xp)))
                el.click()
                time.sleep(2)
                return True
            except Exception:
                pass

        # 3) IME action ENTER
        try:
            self.driver.press_keycode(66)
            time.sleep(2)
            return True
        except Exception:
            pass

        # 4) Small scroll and retry
        try:
            self.driver.swipe(self.size['width']//2, int(self.size['height']*0.8),
                              self.size['width']//2, int(self.size['height']*0.6), 500)
            time.sleep(1)
            el = WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text,'Next')]"))
            )
            el.click()
            time.sleep(2)
            return True
        except Exception:
            pass

        # 5) Bottom-center tap
        try:
            self.driver.tap([(self.size['width']//2, int(self.size['height']*0.9))])
            time.sleep(2)
            return True
        except Exception:
            pass

        print(f"❌ Next not clicked ({context})")
        return False

    # ---------- Improved long‑press stack ----------
    def _center_of(self, el) -> Tuple[int, int]:
        loc, sz = el.location, el.size
        return loc['x'] + sz['width']//2, loc['y'] + sz['height']//2

    def _scroll_into_view(self, el):
        # Try to nudge the view so the element is near center
        try:
            cx, cy = self._center_of(el)
            mid_y = self.size['height'] // 2
            delta = cy - mid_y
            if abs(delta) > 80:
                # swipe opposite to delta to center
                start_y = min(max(mid_y + int(delta*0.6), 200), self.size['height'] - 200)
                end_y = mid_y
                self.driver.swipe(self.size['width']//2, start_y, self.size['width']//2, end_y, 500)
                time.sleep(0.8)
        except Exception:
            pass

    def long_press_15s_strong(self, el) -> bool:
        # Ensure visible and not under keyboard
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        self._scroll_into_view(el)

        cx, cy = self._center_of(el)

        # 1) Native longClick (best when supported)
        try:
            # If supported by the driver, this performs a native long click for duration ms
            self.driver.execute_script("mobile: longClickGesture", {"elementId": el.id, "duration": 15000})
            time.sleep(3)
            return True
        except Exception as e:
            pass

        # 2) W3C hold built as 15 one‑second ticks (avoids long single-pause timeouts)
        try:
            actions = ActionBuilder(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions.add_action(finger.create_pointer_move(duration=0, x=cx, y=cy))
            actions.add_action(finger.create_pointer_down())
            for _ in range(15):
                actions.add_action(finger.create_pause(1))  # 1s × 15
            actions.add_action(finger.create_pointer_up())
            actions.perform()
            time.sleep(3)
            return True
        except Exception as e:
            pass

        # 3) ADB swipe at exact element center (long‑press emulation)
        try:
            subprocess.run([
                "adb", "shell", "input", "touchscreen", "swipe",
                str(cx), str(cy), str(cx), str(cy), "15000"
            ], check=False)
            time.sleep(5)
            return True
        except Exception as e:
            pass

        # 4) Tiny “micro‑drag” while pressed (helps some devices with strict press detection)
        try:
            actions = ActionBuilder(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger2")
            actions.add_action(finger.create_pointer_move(duration=0, x=cx, y=cy))
            actions.add_action(finger.create_pointer_down())
            # Walk 2px right then back left while holding, over ~15s
            for i in range(15):
                actions.add_action(finger.create_pointer_move(duration=500, x=cx+2, y=cy))
                actions.add_action(finger.create_pointer_move(duration=500, x=cx, y=cy))
            actions.add_action(finger.create_pointer_up())
            actions.perform()
            time.sleep(2)
            return True
        except Exception:
            pass

        print("❌ All long‑press strategies failed")
        return False

    # ---------- Flow steps ----------
    def step1_welcome(self):
        el = self._safe(AppiumBy.XPATH, "//*[contains(@text,'CREATE NEW ACCOUNT')]", 10)
        if el:
            el.click(); time.sleep(2); return True
        # Fallback tap
        self.driver.tap([(self.size['width']//2, int(self.size['height']*0.75))]); time.sleep(2); return True

    def step2_email(self, username):
        email = self._safe(AppiumBy.XPATH, "//*[contains(@hint,'email')]", 6) \
             or self._safe(AppiumBy.CLASS_NAME, "android.widget.EditText", 6)
        if not email: return False
        if not self.type_robust(email, username, "Email"): return False
        return self.next_click("Email")

    def step3_password(self, password):
        pwd = self._safe(AppiumBy.XPATH, "//*[contains(@hint,'Password')]", 6) \
           or self._safe(AppiumBy.XPATH, "//android.widget.EditText[21]", 6)
        if not pwd: return False
        if not self.type_robust(pwd, password, "Password"): return False
        return self.next_click("Password")

    def _find_year(self):
        # last EditText → rightmost → instances
        edits = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if edits: return edits[-1]
        try:
            rightmost, best = 0, None
            for e in self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText"):
                bounds = e.get_attribute("bounds")
                x2 = int(bounds.split("][")[21].split(","))
                if x2 > rightmost: rightmost, best = x2, e
            if best: return best
        except Exception:
            pass
        for i in [2, 1, 0]:
            try:
                return self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().className("android.widget.EditText").enabled(true).instance({i})'
                )
            except Exception:
                pass
        return None

    def step4_details(self, day, month, year):
        # Day
        day_dd = self._safe(AppiumBy.XPATH, "//*[contains(@text,'Day')]", 6)
        if day_dd:
            day_dd.click(); time.sleep(1)
            opt = self._safe(AppiumBy.XPATH, f"//*[@text='{day}']", 5)
            if opt: opt.click(); time.sleep(1)
        # Month
        mo_dd = self._safe(AppiumBy.XPATH, "//*[contains(@text,'Month')]", 6)
        if mo_dd:
            mo_dd.click(); time.sleep(1)
            opt = self._safe(AppiumBy.XPATH, f"//*[@text='{month}']", 5)
            if opt: opt.click(); time.sleep(1)
        # Year
        y_el = self._find_year()
        if not y_el: return False
        if not self.type_robust(y_el, year, "Year"): return False
        return self.next_click("Details")

    def _name_fields(self) -> Tuple[Optional[any], Optional[any]]:
        fn = self._safe(AppiumBy.XPATH, "//*[contains(@hint,'First')]", 4)
        ln = self._safe(AppiumBy.XPATH, "//*[contains(@hint,'Last')]", 4)
        if fn and ln: return fn, ln
        # Geometry: first two visible edittexts top→bottom
        edits = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        pairs = []
        for e in edits:
            try:
                if not e.is_displayed(): continue
                bounds = e.get_attribute("bounds")
                y1 = int(bounds.split(",")[21].split("]"))
                pairs.append((y1, e))
            except Exception:
                pass
        pairs.sort(key=lambda t: t)
        if len(pairs) >= 2: return pairs[21], pairs[21][21]
        if len(edits) >= 2: return edits, edits[21]
        return None, None

    def step5_name(self, first, last):
        time.sleep(1.0)
        fn, ln = self._name_fields()
        if not (fn and ln): return False
        if not self.type_robust(fn, first, "First Name"): return False
        if not self.type_robust(ln, last, "Last Name"): return False
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        return self.next_click("Name")

    def step6_captcha(self):
        # Find the “Press and hold” control and apply strong 15s long‑press
        cap = self._safe(AppiumBy.XPATH, "//*[contains(@text,'Press and hold')]", 10) \
           or self._safe(AppiumBy.XPATH, "//*[contains(@text,'prove you') or contains(@text,'human')]", 6)
        if not cap:
            # If not found, attempt centered ADB long‑press at 60% screen height
            cx, cy = self.size['width']//2, int(self.size['height']*0.6)
            subprocess.run(["adb","shell","input","touchscreen","swipe",str(cx),str(cy),str(cx),str(cy),"15000"], check=False)
            time.sleep(5)
            return True
        return self.long_press_15s_strong(cap)

    # ---------- Runner ----------
    def run(self, user):
        if not self.setup(): return False
        time.sleep(4)
        flow = [
            ("Welcome", lambda: self.step1_welcome()),
            ("Email", lambda: self.step2_email(user['username'])),
            ("Password", lambda: self.step3_password(user['password'])),
            ("Details", lambda: self.step4_details(user['birth_date']['day'], user['birth_date']['month'], user['birth_date']['year'])),
            ("Name", lambda: self.step5_name(user['first_name'], user['last_name'])),
            ("CAPTCHA", lambda: self.step6_captcha()),
        ]
        try:
            for name, fn in flow:
                print(f"\n🚀 {name}...")
                if not fn():
                    print(f"❌ {name} failed")
                    return False
                print(f"✅ {name} done")
            print("\n🎉 Flow completed")
            return True
        finally:
            try: self.driver.quit()
            except Exception: pass


def main():
    user = {
        "username": f"auto{random.randint(100000, 999999)}",
        "password": f"Auto{random.randint(100,999)}Pass!",
        "first_name": "Auto",
        "last_name": "User",
        "birth_date": {"day": random.randint(1,28), "month": random.choice(
            ["January","February","March","April","May","June","July","August","September","October","November","December"]
        ), "year": random.randint(1990,2000)}
    }
    bot = OutlookCreatorV3()
    bot.run(user)


if __name__ == "__main__":
    main()
