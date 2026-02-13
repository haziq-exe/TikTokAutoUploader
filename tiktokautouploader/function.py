from phantomwright.sync_api import sync_playwright
from phantomwright.stealth import Stealth
from phantomwright.user_simulator import SyncUserSimulator
import json
import time
import subprocess
from inference_sdk import InferenceHTTPClient
import pkg_resources
import requests
from PIL import Image
import sys
import os
import warnings
warnings.simplefilter("ignore")


def check_for_updates():
    current_version = pkg_resources.get_distribution("tiktokautouploader").version
    response = requests.get("https://pypi.org/pypi/tiktokautouploader/json")
    
    if response.status_code == 200:
        latest_version = response.json()["info"]["version"]
        if current_version != latest_version:
            print(f"WARNING: You are using version {current_version} of tiktokautouploader, "
                  f"PLEASE UPDATE TO LATEST VERSION {latest_version} FOR BEST EXPERIENCE.")

def login_warning(accountname):
    print(f"NO COOKIES FILE FOUND FOR ACCOUNT {accountname}, PLEASE LOG-IN TO {accountname} WHEN PROMPTED")

def save_cookies(cookies):
    with open('TK_cookies.json', 'w') as file:
        json.dump(cookies, file, indent=4)

def check_expiry(accountname):
    with open(f'TK_cookies_{accountname}.json', 'r') as file:
        cookies = json.load(file)

    current_time = int(time.time())
    cookies_expire = []
    expired = False
    for cookie in cookies:
        if cookie['name'] in ['sessionid', 'sid_tt', 'sessionid_ss', 'passport_auth_status']:
            expiry = cookie.get('expires')
            if not expiry:
                expiry = cookie.get('expirationDate')
            cookies_expire.append(expiry < current_time)

    if all(cookies_expire):
        expired = True

    return expired

def run_javascript(proxy_data=None):
    js_file_path = pkg_resources.resource_filename(__name__, 'Js_assets/login.js')
    proxy_argument = str(proxy_data) if proxy_data is not None else str({})
    try:
        result = subprocess.run(
            ['node', js_file_path, '--proxy', proxy_argument],
            capture_output=True,
            text=True,
        )
    except Exception as e:
        sys.exit(f"Error while running the JavaScript file, when trying to parse cookies: {e}")
    return result

def install_js_dependencies():
    js_dir = pkg_resources.resource_filename(__name__, 'Js_assets')
    node_modules_path = os.path.join(js_dir, 'node_modules')

    if not os.path.exists(node_modules_path):
        print("JavaScript dependencies not found. Installing...")
        try:
            subprocess.run(['npm', 'install', '--silent'], cwd=js_dir, check=True)
        except Exception as e:
            print("An error occurred during npm installation.")
            print(f"Error details: {e}")
            print("Trying to install JavaScript dependencies with shell...")
            try:
                subprocess.run(['npm', 'install', '--silent'], cwd=js_dir, check=True, shell=True)
            except Exception as e:
                print("An error occurred during shell npm installation.")
                print(f"Error details: {e}")
    else:
        time.sleep(0.1)


def read_cookies(cookies_path):
    cookie_read = False
    try:
        with open(cookies_path, 'r') as cookiefile:
            cookies = json.load(cookiefile)

        for cookie in cookies:
            if cookie.get('sameSite') not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'Lax'

        cookie_read = True
    except:
        sys.exit("ERROR: CANT READ COOKIES FILE")
    
    return cookies, cookie_read

def detect_redirect(page):
    redirect_detected = False

    def on_response(response):
        nonlocal redirect_detected
        if response.request.redirected_from:
            redirect_detected = True

    page.on('response', on_response)

    return redirect_detected

def understood_Qs(question):
    understood_terms = {
        'touchdowns': 'football',
        'orange and round': 'basketball',
        'used in hoops': 'basketball',
        'has strings': 'guitar',
        'oval and inflatable': 'football',
        'strumming': 'guitar',
        'bounces': 'basketball',
        'musical instrument': 'guitar',
        'laces': 'football',
        'bands': 'guitar',
        'leather': 'football',
        'leaves': 'tree',
        'pages': 'book',
        'throwing': 'football',
        'tossed in a spiral': 'football',
        'spiky crown': 'pineapple',
        'pigskin': 'football',
        'photography': 'camera',
        'lens': 'camera',
        'grow': 'tree',
        'captures images': 'camera',
        'keeps doctors': 'apple',
        'crown': 'pineapple',
        'driven': 'car',
    }
    
    for key in understood_terms.keys():
        if key in question:
            item = understood_terms.get(key)
            return item
        
    return 'N.A'

def get_image_src(page):
    image_url = page.get_attribute("img#captcha-verify-image", "src")
    return image_url

def download_image(image_url):
    response = requests.get(image_url)
    image_path = "captcha_image.jpg"
    with open(image_path, "wb") as f:
        f.write(response.content)
    return image_path

def run_inference_on_image_tougher(image_path, object):
    rk = 'kyHFbAWkOWfGz8fSEw8O'
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=f"{rk}"
    )
    results = CLIENT.infer(image_path, model_id="captcha-2-6ehbe/2")
    class_names = []
    bounding_boxes = []
    for obj in results['predictions']:
        class_names.append(obj['class'])
        bounding_boxes.append({
            "x": obj['x'],
            "y": obj['y'],
            "width": obj['width'],
            "height": obj['height']
        })
    
    bounding_box = []
    class_to_click = object
    for i, classes in enumerate(class_names):
        if classes == class_to_click:
            bounding_box.append(bounding_boxes[i])

    return bounding_box

def run_inference_on_image(image_path):
    rk = 'kyHFbAWkOWfGz8fSEw8O'
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=f"{rk}"
    )
    results = CLIENT.infer(image_path, model_id="tk-3nwi9/2")
    class_names = []
    bounding_boxes = []
    for obj in results['predictions']:
        class_names.append(obj['class'])
        bounding_boxes.append({
            "x": obj['x'],
            "y": obj['y'],
            "width": obj['width'],
            "height": obj['height']
        })
    
    already_written = []
    bounding_box = []
    class_to_click = []
    for i, detected_class in enumerate(class_names):
        if detected_class in already_written:
            class_to_click.append(detected_class)
            bounding_box.append(bounding_boxes[i])
            index = already_written.index(detected_class)
            bounding_box.append(bounding_boxes[index])
        already_written.append(detected_class)

    found = False
    if len(class_to_click) == 1:
        found = True

    return bounding_box, found

def convert_to_webpage_coordinates(bounding_boxes, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real):
    webpage_coordinates = []
    for box in bounding_boxes:
        x_box = box['x']
        y_box = box['y']
        rel_x = (x_box * image_width_web) / image_width_real
        rel_y = (y_box * image_height_web) / image_height_real
        x_cord = image_x + rel_x
        y_cord = image_y + rel_y
        webpage_coordinates.append((x_cord, y_cord))
    return webpage_coordinates

def click_on_objects(page, object_coords):
    for (x, y) in object_coords:
        page.mouse.click(x, y)
        time.sleep(0.5)

def validate_proxy(proxy):
    if not proxy:
        return

    if not isinstance(proxy, dict):
        raise ValueError("Proxy must be a dictionary.")

    if "server" not in proxy or not isinstance(proxy["server"], str):
        raise ValueError("Proxy must contain a 'server' key with a string value.")

    try:
        proxies = {
            "http": f'http://{proxy["server"]}/',
            "https": f'https://{proxy["server"]}/',
        }
        if proxy.get("username"):
            proxies = {
                "http": f'http://{proxy.get("username")}:{proxy.get("password")}@{proxy["server"]}/',
                "https": f'https://{proxy.get("username")}:{proxy.get("password")}@{proxy["server"]}/',
            }

        response = requests.get("https://www.google.com", proxies=proxies)
        if response.status_code == 200:
            print("Proxy is valid!")
        else:
            raise ValueError(f"Proxy test failed with status code: {response.status_code}")
    except Exception as e:
        raise ValueError(f"Invalid proxy configuration when trying to simple request: {e}")


def _make_stealth_context(p, headless, proxy):

    stealth = Stealth(
        navigator_languages_override=("en-US", "en"),
    )

    browser = p.chromium.launch(
        headless=headless,
        proxy=proxy,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--disable-dev-shm-usage",
        ],
    )
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        locale="en-US",
        timezone_id="America/New_York",
    )
    
    stealth.apply_stealth_sync(context)
    return browser, context


def select_sound_from_favorites(page, sound_name, sim=None, stealth=False, suppressprint=False):
    """
    Selects a sound from the favorites tab by searching through the list.
    Returns True if sound was found and selected, False otherwise.
    """
    try:
        if stealth:
            time.sleep(1)
        try:
            page.click('button:has-text("Favorites")')
        except:
            try:
                page.click('button#favourite')
            except:
                page.click('div.TUXTabBar-item#favourite button')

        time.sleep(1)
        if stealth:
            time.sleep(1)

        page.wait_for_selector('div[class*="MusicPanelMusicItem__content"]', timeout=50000)
        time.sleep(2.5)

        music_cards = page.locator('div[class*="MusicPanelMusicItem__content"]')
        card_count = music_cards.count()

        if not suppressprint:
            print(f"Found {card_count} favorite sounds, searching for '{sound_name}'...")

        keywords = sound_name.split()
        keywords_lower = [kw.lower() for kw in keywords if kw.strip()]

        if not suppressprint and len(keywords_lower) > 1:
            print(f"Searching for sounds containing all keywords: {keywords_lower}")

        found = False
        for i in range(card_count):
            try:
                card = music_cards.nth(i)
                title_element = card.locator('div[class*="MusicPanelMusicItem__infoBasicTitle"]')
                title_text = title_element.inner_text() if title_element.count() > 0 else ""
                other_element = card.locator('div[class*="MusicPanelMusicItem__infoBasicDesc"]')
                other_text = other_element.inner_text() if other_element.count() > 0 else ""

                combined_text = f"{title_text} {other_text}".strip().lower()

                all_keywords_match = all(kw in combined_text for kw in keywords_lower)

                if all_keywords_match and combined_text:
                    display_title = title_text if title_text else "Unknown"
                    if not suppressprint:
                        print(f"Found matching sound: '{display_title} {other_text}'")

                    if stealth:
                        time.sleep(0.5)

                    
                    if sim:
                        sim.prepare_for_interaction(card)
                        time.sleep(0.3)
                        sim.click(card)
                    else:
                        card.hover()
                        time.sleep(0.3)
                        card.click()

                    card.locator("button").last.click()
                    if stealth:
                        time.sleep(1)

                    found = True
                    break
            except:
                continue

        return found

    except Exception as e:
        if not suppressprint:
            print(f"Error in favorites search: {e}")
        return False


def select_sound_from_search(page, sound_name, sim=None, stealth=False):
    """
    Selects a sound using the search functionality (original behavior).
    Uses SyncUserSimulator for human-like typing when available.
    """
    search_box = page.get_by_placeholder("Search sounds")
    if sim:
        sim.click(search_box)
        sim.type(search_box, sound_name)
    else:
        search_box.click()
        page.keyboard.type(sound_name)

    time.sleep(0.2)
    if stealth:
        time.sleep(2)
    page.keyboard.press("Enter")
    try:
        page.wait_for_selector("div[class*='MusicPanelMusicItem__operation']")
        if stealth:
            time.sleep(0.5)
        page.locator("div[class*='MusicPanelMusicItem__operation']").first.click()
        if stealth:
            time.sleep(1)
        return True
    except:
        return False


def upload_tiktok(video, description, accountname, hashtags=None, sound_name=None, sound_aud_vol='mix', schedule=None, day=None, copyrightcheck=False, suppressprint=False, headless=True, stealth=False, proxy=None, search_mode='search'):

    """
    UPLOADS VIDEO TO TIKTOK (powered by Phantomwright for bot-detection evasion)
    --------------------------------------------------------------------------------
    video (str) -> path to video to upload
    description (str) -> description for video
    accountname (str) -> account to upload on
    hashtags (str)(array)(opt) -> hashtags for video
    sound_name (str)(opt) -> name of tik tok sound to use for video
    sound_aud_vol (str)(opt) -> volume of tik tok sound, 'main', 'mix' or 'background'
    schedule (str)(opt) -> format HH:MM, your local time to upload video
    day (int)(opt) -> day to schedule video for
    copyrightcheck (bool)(opt) -> include copyright check or not
    suppressprint (bool)(opt) -> True means function doesnt print anything
    headless (bool)(opt) -> run in headless mode or not
    stealth (bool)(opt) -> will wait second(s) before each operation
    proxy (dict)(opt) -> proxy server to run code on
    search_mode (str)(opt) -> 'search' or 'favorites'
    """
    try:
        check_for_updates()
    except:
        time.sleep(0.1)

    try:
        validate_proxy(proxy)
    except Exception as e:
        sys.exit(f'Error validating proxy: {e}')

    retries = 0
    cookie_read = False
    oldQ = 'N.A'

    if accountname is None:
        sys.exit("PLEASE ENTER NAME OF ACCOUNT TO POST ON, READ DOCUMENTATION FOR MORE INFO")

    if os.path.exists(f'TK_cookies_{accountname}.json'):
        cookies, cookie_read = read_cookies(cookies_path=f'TK_cookies_{accountname}.json')
        expired = check_expiry(accountname=accountname)
        if expired:
            os.remove(f'TK_cookies_{accountname}.json')
            print(f"COOKIES EXPIRED FOR ACCOUNT {accountname}, PLEASE LOG-IN AGAIN")
            cookie_read = False

    if not cookie_read:
        install_js_dependencies()
        login_warning(accountname=accountname)
        run_javascript(proxy_data=proxy)
        os.rename('TK_cookies.json', f'TK_cookies_{accountname}.json')
        cookies, cookie_read = read_cookies(f"TK_cookies_{accountname}.json")
        if not cookie_read:
            sys.exit("ERROR READING COOKIES")

    with sync_playwright() as p:

        browser, context = _make_stealth_context(p, headless=headless, proxy=proxy)
        context.add_cookies(cookies)
        page = context.new_page()

        # Initialise human-behaviour simulator for this page
        sim = SyncUserSimulator(page)

        url = 'https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=en'

        if not suppressprint:
            print(f"Uploading to account '{accountname}'")

        while retries < 2:
            try:
                page.goto(url, timeout=30000)
            except:
                retries += 1
                time.sleep(5)
                if retries == 2:
                    sys.exit("ERROR: TIK TOK PAGE FAILED TO LOAD, try again.")
            else:
                break

        # Brief human-like browsing pause after page load
        sim.simulate_browsing(duration_ms=1500)

        detected = False
        captcha = False
        while not detected:
            if page.locator('.upload-text-container').is_visible():
                detected = True
            else:
                if page.locator('div.VerifyBar___StyledDiv-sc-12zaxoy-0.hRJhHT').is_visible():
                    detected = True
                    captcha = True
                else:
                    time.sleep(0.1)

        if captcha:
            image = get_image_src(page)
            if image:
                if not suppressprint:
                    print("CAPTCHA DETECTED, Attempting to solve")
                solved = False
                attempts = 0
                question = page.locator('div.VerifyBar___StyledDiv-sc-12zaxoy-0.hRJhHT').text_content()
                while not solved:
                    attempts += 1
                    start_time = time.time()
                    while question == oldQ:
                        question = page.locator('div.VerifyBar___StyledDiv-sc-12zaxoy-0.hRJhHT').text_content()
                        if time.time() - start_time > 2:
                            break
                    if 'Select 2 objects that are the same' in question or 'Select two objects that are the same' in question:
                        found = False
                        while not found:
                            page.click('span.secsdk_captcha_refresh--text')
                            image = get_image_src(page)
                            img_path = download_image(image)
                            b_box, found = run_inference_on_image(image_path=img_path)

                        with Image.open(img_path) as img:
                            image_size = img.size

                        imageweb = page.locator('#captcha-verify-image')
                        imageweb.wait_for()
                        box = imageweb.bounding_box()
                        image_x = box['x']
                        image_y = box['y']
                        image_height_web = box['height']
                        image_width_web = box['width']
                        image_width_real, image_height_real = image_size

                        webpage_coords = convert_to_webpage_coordinates(b_box, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real)
                        if not webpage_coords:
                            webpage_coords.append((image_x + 50, image_y + 50))
                        click_on_objects(page, webpage_coords)
                        page.click("div.verify-captcha-submit-button")
                        time.sleep(0.5)
                        if attempts > 5:
                            sys.exit("FAILED TO SOLVE CAPTCHA")
                        showedup = False
                        while not showedup:
                            if page.locator("div.captcha_verify_message.captcha_verify_message-pass").is_visible():
                                solved = True
                                showedup = True
                                os.remove('captcha_image.jpg')
                            if page.locator("div.captcha_verify_message.captcha_verify_message-fail").is_visible():
                                showedup = True
                                oldQ = question
                                page.click('span.secsdk_captcha_refresh--text')
                    else:
                        objectclick = understood_Qs(question)
                        while objectclick == 'N.A':
                            oldQ = question
                            page.click('span.secsdk_captcha_refresh--text')
                            start_time = time.time()
                            runs = 0
                            while question == oldQ:
                                runs += 1
                                question = page.locator('div.VerifyBar___StyledDiv-sc-12zaxoy-0.hRJhHT').text_content()
                                if runs > 1:
                                    time.sleep(1)
                                if time.time() - start_time > 2:
                                    break
                            objectclick = understood_Qs(question)
                        image = get_image_src(page)
                        img_path = download_image(image)
                        b_box = run_inference_on_image_tougher(image_path=img_path, object=objectclick)

                        with Image.open(img_path) as img:
                            image_size = img.size

                        imageweb = page.locator('#captcha-verify-image')
                        imageweb.wait_for()
                        box = imageweb.bounding_box()
                        image_x = box['x']
                        image_y = box['y']
                        image_height_web = box['height']
                        image_width_web = box['width']
                        image_width_real, image_height_real = image_size

                        webpage_coords = convert_to_webpage_coordinates(b_box, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real)
                        if not webpage_coords:
                            webpage_coords.append((image_x + 50, image_y + 50))
                        click_on_objects(page, webpage_coords)
                        page.click("div.verify-captcha-submit-button")
                        time.sleep(1)
                        if attempts > 20:
                            sys.exit("FAILED TO SOLVE CAPTCHA")
                        showedup = False
                        while not showedup:
                            if page.locator("div.captcha_verify_message.captcha_verify_message-pass").is_visible():
                                solved = True
                                showedup = True
                                os.remove('captcha_image.jpg')
                                if not suppressprint:
                                    print("CAPTCHA SOLVED")
                            if page.locator("div.captcha_verify_message.captcha_verify_message-fail").is_visible():
                                showedup = True
                                oldQ = question
                                page.click('span.secsdk_captcha_refresh--text')

        try:
            page.set_input_files('input[type="file"][accept="video/*"]', f'{video}')
        except:
            sys.exit("ERROR: FAILED TO INPUT FILE. Possible Issues: Wifi too slow, file directory wrong, or check documentation to see if captcha is solvable")

        page.wait_for_selector('div[data-contents="true"]')

        time.sleep(0.5)
        if page.locator("button:has-text('Cancel')").is_visible():
            print("Tutorial pop-up detected, dismissing...")
            page.click("button:has-text('Cancel')")
        if page.locator("button:has-text('Got it')").is_visible():
            page.click("button:has-text('Got it')")

        # Human-like click into the description box
        desc_box = page.locator('div[data-contents="true"]')
        sim.click(desc_box)

        if not suppressprint:
            print("Entered File, waiting for tiktok to load onto their server, this may take a couple of minutes, depending on your video length")

        time.sleep(0.5)
        if description is None:
            sys.exit("ERROR: PLEASE INCLUDE A DESCRIPTION")

        for _ in range(len(video) + 2):
            page.keyboard.press("Backspace")
            page.keyboard.press("Delete")

        time.sleep(0.5)

        # Human-like typing for description
        sim.type(desc_box, description)

        if hashtags is not None:
            for hashtag in hashtags:
                if hashtag[0] != '#':
                    hashtag = "#" + hashtag

                page.keyboard.type(hashtag)
                time.sleep(0.5)
                try:
                    if stealth:
                        time.sleep(2)
                    page.click(f'span.hash-tag-topic:has-text("{hashtag}")', timeout=1000)
                except:
                    try:
                        page.click('span.hash-tag-topic', timeout=1000)
                    except:
                        page.keyboard.press("Backspace")
                        try:
                            page.click('span.hash-tag-topic', timeout=1000)
                        except:
                            if not suppressprint:
                                print(f"Tik tok hashtag not working for {hashtag}, moving onto next")
                            page.keyboard.type(f"{hashtag[-1]} ")

        if not suppressprint:
            print("Description and Hashtags added")

        content_check_btn = page.locator("div.common-modal-footer > button[data-type='neutral']", has_text="Cancel")
        if content_check_btn.is_visible():
            content_check_btn.click()

        try:
            page.wait_for_selector('button:has-text("Post")[aria-disabled="false"]', timeout=12000000)
        except:
            sys.exit("ERROR: TIK TOK TOOK TOO LONG TO UPLOAD YOUR FILE (>20min). Try again, if issue persists then try a lower file size or different wifi connection")

        time.sleep(0.2)
        if not suppressprint:
            print("Tik tok done loading file onto servers")

        # Brief browsing simulation before scheduling / posting to look less robotic
        sim.simulate_browsing(duration_ms=1000)

        if (schedule is None) and (day is not None):
            sys.exit("ERROR: CANT SCHEDULE FOR ANOTHER DAY USING 'day' WITHOUT ALSO INCLUDING TIME OF UPLOAD WITH 'schedule'; PLEASE ALSO INCLUDE TIME WITH 'schedule' PARAMETER")

        if schedule is not None:
            try:
                hour = schedule[0:2]
                minute = schedule[3:]
                if (int(minute) % 5) != 0:
                    sys.exit("MINUTE FORMAT ERROR: PLEASE MAKE SURE MINUTE YOU SCHEDULE AT IS A MULTIPLE OF 5 UNTIL 60 (i.e: 40), VIDEO SAVED AS DRAFT")
            except:
                sys.exit("SCHEDULE TIME ERROR: PLEASE MAKE SURE YOUR SCHEDULE TIME IS A STRING THAT FOLLOWS THE 24H FORMAT 'HH:MM', VIDEO SAVED AS DRAFT")

            page.locator('label:has-text("Schedule")').click()
            if stealth:
                time.sleep(2)
            visible = False
            while not visible:
                if page.locator('button:has-text("Allow")').nth(0).is_visible():
                    if stealth:
                        time.sleep(1)
                    page.locator('button:has-text("Allow")').nth(0).click()
                    visible = True
                    time.sleep(0.1)
                else:
                    if page.locator('div.TUXTextInputCore-trailingIconWrapper').nth(1).is_visible():
                        visible = True
                        time.sleep(0.1)
            if day is not None:
                if stealth:
                    time.sleep(1)
                page.locator('div.TUXTextInputCore-leadingIconWrapper:has(svg > path[d="M15 3a1 1 0 0 0-1 1v3h-1.4c-3.36 0-5.04 0-6.32.65a6 6 0 0 0-2.63 2.63C3 11.56 3 13.24 3 16.6v16.8c0 3.36 0 5.04.65 6.32a6 6 0 0 0 2.63 2.63c1.28.65 2.96.65 6.32.65h22.8c3.36 0 5.04 0 6.32-.65a6 6 0 0 0 2.63-2.63c.65-1.28.65-2.96.65-6.32V16.6c0-3.36 0-5.04-.65-6.32a6 6 0 0 0-2.63-2.63C40.44 7 38.76 7 35.4 7H34V4a1 1 0 0 0-1-1h-2a1 1 0 0 0-1 1v3H18V4a1 1 0 0 0-1-1h-2Zm-2.4 8H14v3a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-3h12v3a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-3h1.4c1.75 0 2.82 0 3.62.07a5.11 5.11 0 0 1 .86.14h.03a2 2 0 0 1 .88.91 5.11 5.11 0 0 1 .14.86c.07.8.07 1.87.07 3.62v1.9H7v-1.9c0-1.75 0-2.82.07-3.62a5.12 5.12 0 0 1 .14-.86v-.03a2 2 0 0 1 .88-.87l.03-.01a5.11 5.11 0 0 1 .86-.14c.8-.07 1.87-.07 3.62-.07ZM7 22.5h34v10.9c0 1.75 0 2.82-.07 3.62a5.11 5.11 0 0 1-.14.86v.03a2 2 0 0 1-.88.87l-.03.01a5.11 5.11 0 0 1-.86.14c-.8.07-1.87.07-3.62.07H12.6c-1.75 0-2.82 0-3.62-.07a5.11 5.11 0 0 1-.89-.15 2 2 0 0 1-.87-.87l-.01-.03a5.12 5.12 0 0 1-.14-.86C7 36.22 7 35.15 7 33.4V22.5Z"])').click()
                time.sleep(0.2)
                try:
                    if stealth:
                        time.sleep(1)
                    page.locator(f'span.day.valid:text-is("{day}")').click()
                except:
                    sys.exit("SCHEDULE DAY ERROR: ERROR WITH SCHEDULED DAY, read documentation for more information on format of day")
            try:
                time.sleep(0.2)
                page.locator('div.TUXTextInputCore-leadingIconWrapper:has(svg > path[d="M24 2a22 22 0 1 0 0 44 22 22 0 0 0 0-44ZM6 24a18 18 0 1 1 36 0 18 18 0 0 1-36 0Z"])').click()
                time.sleep(0.2)
                page.locator(f'.tiktok-timepicker-option-text.tiktok-timepicker-right:text-is("{minute}")').scroll_into_view_if_needed()
                time.sleep(0.2)
                if stealth:
                    time.sleep(2)
                page.locator(f'.tiktok-timepicker-option-text.tiktok-timepicker-right:text-is("{minute}")').click()
                time.sleep(0.2)
                if page.locator("div.tiktok-timepicker-time-picker-container").is_visible():
                    time.sleep(0.1)
                else:
                    page.locator('div.TUXTextInputCore-leadingIconWrapper:has(svg > path[d="M24 2a22 22 0 1 0 0 44 22 22 0 0 0 0-44ZM6 24a18 18 0 1 1 36 0 18 18 0 0 1-36 0Z"])').click()
                page.locator(f'.tiktok-timepicker-option-text.tiktok-timepicker-left:text-is("{hour}")').scroll_into_view_if_needed()
                if stealth:
                    time.sleep(2)
                page.locator(f'.tiktok-timepicker-option-text.tiktok-timepicker-left:text-is("{hour}")').click()
                time.sleep(1)
                if not suppressprint:
                    print("Done scheduling video")
            except:
                sys.exit("SCHEDULING ERROR: VIDEO SAVED AS DRAFT")

        sound_fail = False
        if sound_name is not None:
            try:
                if stealth:
                    time.sleep(2)
                sounds_btn = page.locator("button:has-text('Sounds')").last
                sim.click(sounds_btn)
            except:
                sound_fail = True
            if not sound_fail:
                time.sleep(1.5)

                sound_found = False
                if search_mode == 'favorites':
                    sound_found = select_sound_from_favorites(page, sound_name, sim=sim, stealth=stealth, suppressprint=suppressprint)
                else:
                    sound_found = select_sound_from_search(page, sound_name, sim=sim, stealth=stealth)

                if not sound_found:
                    sys.exit(f"ERROR: SOUND '{sound_name}' NOT FOUND")

                if sound_aud_vol != 'mix':
                    try:
                        page.wait_for_selector('img[src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMSAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTAgNy41MDE2QzAgNi42NzMxNyAwLjY3MTU3MyA2LjAwMTYgMS41IDYuMDAxNkgzLjU3NzA5QzMuODY4MDUgNi4wMDE2IDQuMTQ0NTggNS44NzQ4OCA0LjMzNDU1IDUuNjU0NDlMOC43NDI1NSAwLjU0MDUyQzkuMzQ3OCAtMC4xNjE2NjggMTAuNSAwLjI2NjM3NCAxMC41IDEuMTkzNDFWMTguOTY3MkMxMC41IDE5Ljg3NDUgOS4zODg5NCAyMC4zMTI5IDguNzY5NDIgMTkuNjVMNC4zMzE3OSAxNC45MDIxQzQuMTQyNjkgMTQuNjk5OCAzLjg3ODE2IDE0LjU4NDkgMy42MDEyMiAxNC41ODQ5SDEuNUMwLjY3MTU3MyAxNC41ODQ5IDAgMTMuOTEzNCAwIDEzLjA4NDlWNy41MDE2Wk01Ljg0OTQ1IDYuOTYwMjdDNS4yNzk1NiA3LjYyMTQzIDQuNDQ5OTcgOC4wMDE2IDMuNTc3MDkgOC4wMDE2SDJWMTIuNTg0OUgzLjYwMTIyQzQuNDMyMDMgMTIuNTg0OSA1LjIyNTY0IDEyLjkyOTUgNS43OTI5NSAxMy41MzY0TDguNSAxNi40MzI4VjMuODg1MjJMNS44NDk0NSA2Ljk2MDI3WiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPHBhdGggZD0iTTEzLjUxNSA3LjE5MTE5QzEzLjM0MjQgNi45NzU1OSAxMy4zMzk5IDYuNjYwNTYgMTMuNTM1MiA2LjQ2NTNMMTQuMjQyMyA1Ljc1ODE5QzE0LjQzNzYgNS41NjI5MyAxNC43NTU4IDUuNTYxNzUgMTQuOTM1NiA1Ljc3MTM2QzE2Ljk5NTkgOC4xNzM2MiAxNi45OTU5IDExLjgyOCAxNC45MzU2IDE0LjIzMDNDMTQuNzU1OCAxNC40Mzk5IDE0LjQzNzYgMTQuNDM4NyAxNC4yNDIzIDE0LjI0MzVMMTMuNTM1MiAxMy41MzY0QzEzLjMzOTkgMTMuMzQxMSAxMy4zNDI0IDEzLjAyNjEgMTMuNTE1IDEyLjgxMDVDMTQuODEzIDExLjE4ODUgMTQuODEzIDguODEzMTIgMTMuNTE1IDcuMTkxMTlaIiBmaWxsPSIjMTYxODIzIiBmaWxsLW9wYWNpdHk9IjAuNiIvPgo8cGF0aCBkPSJNMTYuNzE3MiAxNi43MTgzQzE2LjUyMTkgMTYuNTIzMSAxNi41MjMxIDE2LjIwNzQgMTYuNzA3MiAxNi4wMDE3QzE5LjcyNTcgMTIuNjMgMTkuNzI1NyA3LjM3MTY4IDE2LjcwNzIgNC4wMDAwMUMxNi41MjMxIDMuNzk0MjcgMTYuNTIxOSAzLjQ3ODU4IDE2LjcxNzIgMy4yODMzMkwxNy40MjQzIDIuNTc2MjFDMTcuNjE5NSAyLjM4MDk1IDE3LjkzNyAyLjM4MDIgMTguMTIzMyAyLjU4NDA4QzIxLjkwOTkgNi43MjkyNiAyMS45MDk5IDEzLjI3MjQgMTguMTIzMyAxNy40MTc2QzE3LjkzNyAxNy42MjE1IDE3LjYxOTUgMTcuNjIwNyAxNy40MjQzIDE3LjQyNTVMMTYuNzE3MiAxNi43MTgzWiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPC9zdmc+Cg=="]')
                        if stealth:
                            time.sleep(1)
                        page.click('img[src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMSAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTAgNy41MDE2QzAgNi42NzMxNyAwLjY3MTU3MyA2LjAwMTYgMS41IDYuMDAxNkgzLjU3NzA5QzMuODY4MDUgNi4wMDE2IDQuMTQ0NTggNS44NzQ4OCA0LjMzNDU1IDUuNjU0NDlMOC43NDI1NSAwLjU0MDUyQzkuMzQ3OCAtMC4xNjE2NjggMTAuNSAwLjI2NjM3NCAxMC41IDEuMTkzNDFWMTguOTY3MkMxMC41IDE5Ljg3NDUgOS4zODg5NCAyMC4zMTI5IDguNzY5NDIgMTkuNjVMNC4zMzE3OSAxNC45MDIxQzQuMTQyNjkgMTQuNjk5OCAzLjg3ODE2IDE0LjU4NDkgMy42MDEyMiAxNC41ODQ5SDEuNUMwLjY3MTU3MyAxNC41ODQ5IDAgMTMuOTEzNCAwIDEzLjA4NDlWNy41MDE2Wk01Ljg0OTQ1IDYuOTYwMjdDNS4yNzk1NiA3LjYyMTQzIDQuNDQ5OTcgOC4wMDE2IDMuNTc3MDkgOC4wMDE2SDJWMTIuNTg0OUgzLjYwMTIyQzQuNDMyMDMgMTIuNTg0OSA1LjIyNTY0IDEyLjkyOTUgNS43OTI5NSAxMy41MzY0TDguNSAxNi4wMDAxIDEzLjI3MjQgMTguMTIzMyAxNy40MTc2QzE3LjkzNyAxNy42MjE1IDE3LjYxOTUgMTcuNjIwNyAxNy40MjQzIDE3LjQyNTVMMTYuNzE3MiAxNi43MTgzWiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPC9zdmc+Cg=="]')
                        time.sleep(0.5)
                        sliders = page.locator("input.scaleInput")

                        if sound_aud_vol == 'background':
                            slider2 = sliders.nth(1)
                            bounding_box2 = slider2.bounding_box()
                            if bounding_box2:
                                x2 = bounding_box2["x"] + (bounding_box2["width"] * 0.07)
                                y2 = bounding_box2["y"] + bounding_box2["height"] / 2
                                if stealth:
                                    time.sleep(1)
                                page.mouse.click(x2, y2)

                        if sound_aud_vol == 'main':
                            slider1 = sliders.nth(0)
                            bounding_box1 = slider1.bounding_box()
                            if bounding_box1:
                                x1 = bounding_box1["x"] + (bounding_box1["width"] * 0.07)
                                y1 = bounding_box1["y"] + bounding_box1["height"] / 2
                                if stealth:
                                    time.sleep(1)
                                page.mouse.click(x1, y1)
                        time.sleep(1)
                    except:
                        sys.exit("ERROR ADJUSTING SOUND VOLUME: please try again or use the default 'mix'.")

                page.wait_for_selector("button:has-text('Save')")
                if stealth:
                    time.sleep(1)
                page.locator("button:has-text('Save')").first.click()
                if not suppressprint:
                    print("Added sound")

        if not sound_fail:
            page.wait_for_selector('div[data-contents="true"]')

            if copyrightcheck:
                copy_check_counter = 0
                if stealth:
                    time.sleep(1)
                page.locator('div[data-e2e="copyright_container"] span[data-part="thumb"]').click()
                while copyrightcheck:
                    time.sleep(2)
                    if page.get_by_text("No issues found.", exact=True).is_visible():
                        if not suppressprint:
                            print("Copyright check complete")
                        break
                    if page.locator("span:has-text('Copyright issues detected')").is_visible():
                        sys.exit("COPYRIGHT CHECK FAILED: VIDEO SAVED AS DRAFT, COPYRIGHT AUDIO DETECTED FROM TIKTOK")
                    copy_check_counter += 1
                    if copy_check_counter > 10:
                        print("COPYRIGHT CHECK TIMEOUT: UNABLE TO CONFIRM IF VIDEO PASSED COPYRIGHT CHECK, CONTINUING TO UPLOAD IN 5 SECONDS.")
                        break

            try:
                if schedule is None:
                    if stealth:
                        time.sleep(1)
                    try:
                        page.click('button:has-text("Post")[data-e2e="post_video_button"]', timeout=2000)
                        page.wait_for_url(url='https://www.tiktok.com/tiktokstudio/content', timeout=2000)
                    except:
                        page.click('button:has-text("Post")[aria-disabled="false"]', timeout=2000)
                        try:
                            page.wait_for_url(url='https://www.tiktok.com/tiktokstudio/content', timeout=2000)
                        except:
                            print("POSSIBLE ERROR: Cannot confirm if uploaded successfully, Please check account in a minute or two to confirm")
                            return "Error"
                    uploaded = False
                    checks = 0
                    while not uploaded:
                        if page.locator(':has-text("Leaving the page does not interrupt")').nth(0).is_visible():
                            time.sleep(0.1)
                            break
                        time.sleep(0.2)
                        checks += 1
                        if checks == 25:
                            break
                else:
                    if stealth:
                        time.sleep(1)
                    page.click('button:has-text("Schedule")', timeout=10000)
                    uploaded = False
                    checks = 0
                    while not uploaded:
                        if page.locator(':has-text("Leaving the page does not interrupt")').nth(0).is_visible():
                            time.sleep(0.2)
                            break
                        time.sleep(0.2)
                        checks += 1
                        if checks == 25:
                            break
                if not suppressprint:
                    print("Done uploading video, NOTE: it may take a minute or two to show on TikTok")
            except:
                time.sleep(2)
                sys.exit("POSSIBLE ERROR UPLOADING: Cannot confirm if uploaded successfully, Please check account in a minute or two to confirm.")
            time.sleep(1)
            page.close()

        else:
            # ----------------------------------------------------------------
            # Sound failed on first attempt – save as draft then re-edit
            # ----------------------------------------------------------------
            try:
                if stealth:
                    time.sleep(1)
                page.click('button:has-text("Save draft")', timeout=10000)
            except:
                sys.exit("SAVE AS DRAFT BUTTON NOT FOUND; Please try account that has ability to save as draft")

            time.sleep(0.5)
            page.close()

            # Open a fresh stealthy browser to edit the draft
            browser2, context2 = _make_stealth_context(p, headless=headless, proxy=proxy)
            context2.add_cookies(cookies)
            page = context2.new_page()
            sim = SyncUserSimulator(page)

            url2 = 'https://www.tiktok.com/tiktokstudio/content?tab=draft'

            retries2 = 0
            while retries2 < 2:
                try:
                    page.goto(url2, timeout=30000)
                except:
                    retries2 += 1
                    time.sleep(5)
                    if retries2 == 2:
                        sys.exit("ERROR: TIK TOK PAGE FAILED TO LOAD, try again.")
                else:
                    break

            sim.simulate_browsing(duration_ms=1000)

            try:
                page.wait_for_selector("path[d='M37.37 4.85a4.01 4.01 0 0 0-.99-.79 3 3 0 0 0-2.72 0c-.45.23-.81.6-1 .79a9 9 0 0 1-.04.05l-19.3 19.3c-1.64 1.63-2.53 2.52-3.35 3.47a36 36 0 0 0-4.32 6.16c-.6 1.1-1.14 2.24-2.11 4.33l-.3.6c-.4.75-.84 1.61-.8 2.43a2.5 2.5 0 0 0 2.37 2.36c.82.05 1.68-.4 2.44-.79l.59-.3c2.09-.97 3.23-1.5 4.33-2.11a36 36 0 0 0 6.16-4.32c.95-.82 1.84-1.71 3.47-3.34l19.3-19.3.05-.06a3 3 0 0 0 .78-3.71c-.22-.45-.6-.81-.78-1l-.02-.02-.03-.03-3.67-3.67a8.7 8.7 0 0 1-.06-.05ZM16.2 26.97 35.02 8.15l2.83 2.83L19.03 29.8c-1.7 1.7-2.5 2.5-3.33 3.21a32 32 0 0 1-7.65 4.93 32 32 0 0 1 4.93-7.65c.73-.82 1.51-1.61 3.22-3.32Z']")
                if stealth:
                    time.sleep(1)
                page.click("path[d='M37.37 4.85a4.01 4.01 0 0 0-.99-.79 3 3 0 0 0-2.72 0c-.45.23-.81.6-1 .79a9 9 0 0 1-.04.05l-19.3 19.3c-1.64 1.63-2.53 2.52-3.35 3.47a36 36 0 0 0-4.32 6.16c-.6 1.1-1.14 2.24-2.11 4.33l-.3.6c-.4.75-.84 1.61-.8 2.43a2.5 2.5 0 0 0 2.37 2.36c.82.05 1.68-.4 2.44-.79l.59-.3c2.09-.97 3.23-1.5 4.33-2.11a36 36 0 0 0 6.16-4.32c.95-.82 1.84-1.71 3.47-3.34l19.3-19.3.05-.06a3 3 0 0 0 .78-3.71c-.22-.45-.6-.81-.78-1l-.02-.02-.03-.03-3.67-3.67a8.7 8.7 0 0 1-.06-.05ZM16.2 26.97 35.02 8.15l2.83 2.83L19.03 29.8c-1.7 1.7-2.5 2.5-3.33 3.21a32 32 0 0 1-7.65 4.93 32 32 0 0 1 4.93-7.65c.73-.82 1.51-1.61 3.22-3.32Z']")
                page.wait_for_selector('div[data-contents="true"]')
                time.sleep(0.2)
            except:
                sys.exit("ERROR ADDING SOUND: Video saved as draft")

            if sound_name is not None:
                if stealth:
                    time.sleep(1)
                page.click("div.TUXButton-label:has-text('Edit video')")
                page.wait_for_selector("div[data-e2e='editor_music_container']", timeout=10000)
                time.sleep(0.5)

                sound_found = False
                if search_mode == 'favorites':
                    sound_found = select_sound_from_favorites(page, sound_name, sim=sim, stealth=stealth, suppressprint=suppressprint)
                else:
                    sound_found = select_sound_from_search(page, sound_name, sim=sim, stealth=stealth)

                if not sound_found:
                    sys.exit(f"ERROR: SOUND '{sound_name}' NOT FOUND")

                try:
                    page.wait_for_selector('img[src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMSAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTAgNy41MDE2QzAgNi42NzMxNyAwLjY3MTU3MyA2LjAwMTYgMS41IDYuMDAxNkgzLjU3NzA5QzMuODY4MDUgNi4wMDE2IDQuMTQ0NTggNS44NzQ4OCA0LjMzNDU1IDUuNjU0NDlMOC43NDI1NSAwLjU0MDUyQzkuMzQ3OCAtMC4xNjE2NjggMTAuNSAwLjI2NjM3NCAxMC41IDEuMTkzNDFWMTguOTY3MkMxMC41IDE5Ljg3NDUgOS4zODg5NCAyMC4zMTI5IDguNzY5NDIgMTkuNjVMNC4zMzE3OSAxNC45MDIxQzQuMTQyNjkgMTQuNjk5OCAzLjg3ODE2IDE0LjU4NDkgMy42MDEyMiAxNC41ODQ5SDEuNUMwLjY3MTU3MyAxNC41ODQ5IDAgMTMuOTEzNCAwIDEzLjA4NDlWNy41MDE2Wk01Ljg0OTQ1IDYuOTYwMjdDNS4yNzk1NiA3LjYyMTQzIDQuNDQ5OTcgOC4wMDE2IDMuNTc3MDkgOC4wMDE2SDJWMTIuNTg0OUgzLjYwMTIyQzQuNDMyMDMgMTIuNTg0OSA1LjIyNTY0IDEyLjkyOTUgNS43OTI5NSAxMy41MzY0TDguNSAxNi40MzI4VjMuODg1MjJMNS44NDk0NSA2Ljk2MDI3WiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPHBhdGggZD0iTTEzLjUxNSA3LjE5MTE5QzEzLjM0MjQgNi45NzU1OSAxMy4zMzk5IDYuNjYwNTYgMTMuNTM1MiA2LjQ2NTNMMTQuMjQyMyA1Ljc1ODE5QzE0LjQzNzYgNS41NjI5MyAxNC43NTU4IDUuNTYxNzUgMTQuOTM1NiA1Ljc3MTM2QzE2Ljk5NTkgOC4xNzM2MiAxNi45OTU5IDExLjgyOCAxNC45MzU2IDE0LjIzMDNDMTQuNzU1OCAxNC40Mzk5IDE0LjQzNzYgMTQuNDM4NyAxNC4yNDIzIDE0LjI0MzVMMTMuNTM1MiAxMy41MzY0QzEzLjMzOTkgMTMuMzQxMSAxMy4zNDI0IDEzLjAyNjEgMTMuNTE1IDEyLjgxMDVDMTQuODEzIDExLjE4ODUgMTQuODEzIDguODEzMTIgMTMuNTE1IDcuMTkxMTlaIiBmaWxsPSIjMTYxODIzIiBmaWxsLW9wYWNpdHk9IjAuNiIvPgo8cGF0aCBkPSJNMTYuNzE3MiAxNi43MTgzQzE2LjUyMTkgMTYuNTIzMSAxNi41MjMxIDE2LjIwNzQgMTYuNzA3MiAxNi4wMDE3QzE5LjcyNTcgMTIuNjMgMTkuNzI1NyA3LjM3MTY4IDE2LjcwNzIgNC4wMDAwMUMxNi41MjMxIDMuNzk0MjcgMTYuNTIxOSAzLjQ3ODU4IDE2LjcxNzIgMy4yODMzMkwxNy40MjQzIDIuNTc2MjFDMTcuNjE5NSAyLjM4MDk1IDE3LjkzNyAyLjM4MDIgMTguMTIzMyAyLjU4NDA4QzIxLjkwOTkgNi43MjkyNiAyMS45MDk5IDEzLjI3MjQgMTguMTIzMyAxNy40MTc2QzE3LjkzNyAxNy42MjE1IDE3LjYxOTUgMTcuNjIwNyAxNy40MjQzIDE3LjQyNTVMMTYuNzE3MiAxNi43MTgzWiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPC9zdmc+Cg=="]')
                    if stealth:
                        time.sleep(1)
                    page.click('img[src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMSAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTAgNy41MDE2QzAgNi42NzMxNyAwLjY3MTU3MyA2LjAwMTYgMS41IDYuMDAxNkgzLjU3NzA5QzMuODY4MDUgNi4wMDE2IDQuMTQ0NTggNS44NzQ4OCA0LjMzNDU1IDUuNjU0NDlMOC43NDI1NSAwLjU0MDUyQzkuMzQ3OCAtMC4xNjE2NjggMTAuNSAwLjI2NjM3NCAxMC41IDEuMTkzNDFWMTguOTY3MkMxMC41IDE5Ljg3NDUgOS4zODg5NCAyMC4zMTI5IDguNzY5NDIgMTkuNjVMNC4zMzE3OSAxNC45MDIxQzQuMTQyNjkgMTQuNjk5OCAzLjg3ODE2IDE0LjU4NDkgMy42MDEyMiAxNC41ODQ5SDEuNUMwLjY3MTU3MyAxNC41ODQ5IDAgMTMuOTEzNCAwIDEzLjA4NDlWNy41MDE2Wk01Ljk0OTQ1IDYuOTYwMjdDNS4yNzk1NiA3LjYyMTQzIDQuNDQ5OTcgOC4wMDE2IDMuNTc3MDkgOC4wMDE2SDJWMTIuNTg0OUgzLjYwMTIyQzQuNDMyMDMgMTIuNTg0OSA1LjIyNTY0IDEyLjkyOTUgNS43OTI5NSAxMy41MzY0TDguNSAxNi40MzI4VjMuODg1MjJMNS44NDk0NSA2Ljk2MDI3WiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPC9zdmc+Cg=="]')
                    time.sleep(0.5)
                    sliders = page.locator("input.scaleInput")

                    if sound_aud_vol == 'background':
                        slider2 = sliders.nth(1)
                        bounding_box2 = slider2.bounding_box()
                        if bounding_box2:
                            x2 = bounding_box2["x"] + (bounding_box2["width"] * 0.07)
                            y2 = bounding_box2["y"] + bounding_box2["height"] / 2
                            if stealth:
                                time.sleep(1)
                            page.mouse.click(x2, y2)

                    if sound_aud_vol == 'main':
                        slider1 = sliders.nth(0)
                        bounding_box1 = slider1.bounding_box()
                        if bounding_box1:
                            x1 = bounding_box1["x"] + (bounding_box1["width"] * 0.07)
                            y1 = bounding_box1["y"] + bounding_box1["height"] / 2
                            if stealth:
                                time.sleep(1)
                            page.mouse.click(x1, y1)
                    time.sleep(1)
                except:
                    sys.exit("ERROR ADJUSTING SOUND VOLUME: please try again.")

                page.wait_for_selector("div.TUXButton-label:has-text('Save edit')")
                if stealth:
                    time.sleep(1)
                page.click("div.TUXButton-label:has-text('Save edit')")
                if not suppressprint:
                    print("Added sound")

            page.wait_for_selector('div[data-contents="true"]')

            if copyrightcheck:
                if stealth:
                    time.sleep(1)
                page.locator('div[data-e2e="copyright_container"] span[data-part="thumb"]').click()
                while copyrightcheck:
                    time.sleep(0.2)
                    if page.locator("span", has_text="No issues detected.").is_visible():
                        if not suppressprint:
                            print("Copyright check complete")
                        break
                    if page.locator('span', has_text="Copyright issues detected.").is_visible():
                        sys.exit("COPYRIGHT CHECK FAILED: VIDEO SAVED AS DRAFT, COPYRIGHT AUDIO DETECTED FROM TIKTOK")

            try:
                if schedule is None:
                    if stealth:
                        time.sleep(1)
                    try:
                        page.click('button:has-text("Post")[data-e2e="post_video_button"]', timeout=2000)
                        page.wait_for_url(url='https://www.tiktok.com/tiktokstudio/content', timeout=2000)
                    except:
                        page.click('button:has-text("Post")[aria-disabled="false"]', timeout=2000)
                        try:
                            page.wait_for_url(url='https://www.tiktok.com/tiktokstudio/content', timeout=2000)
                        except:
                            print("POSSIBLE ERROR: Cannot confirm if uploaded successfully, Please check account in a minute or two to confirm")
                            return "Error"
                    uploaded = False
                    checks = 0
                    while not uploaded:
                        if page.locator(':has-text("Leaving the page does not interrupt")').nth(0).is_visible():
                            time.sleep(0.2)
                            break
                        time.sleep(0.2)
                        checks += 1
                        if checks == 25:
                            break
                else:
                    if stealth:
                        time.sleep(1)
                    page.click('button:has-text("Schedule")', timeout=10000)
                    uploaded = False
                    checks = 0
                    while not uploaded:
                        if page.locator(':has-text("Leaving the page does not interrupt")').nth(0).is_visible():
                            time.sleep(0.1)
                            break
                        time.sleep(0.2)
                        checks += 1
                        if checks == 25:
                            break
                if not suppressprint:
                    print("Done uploading video, NOTE: it may take a minute or two to show on TikTok")
            except:
                time.sleep(2)
                sys.exit("POSSIBLE ERROR UPLOADING: Cannot confirm if uploaded successfully, Please check account in a minute or two to confirm.")
            time.sleep(1)
            page.close()

    return "Completed"