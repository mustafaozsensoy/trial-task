def check_url(url):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import warnings






    # Kullanıcıdan URL'yi al


    # Chrome ayarlarını tanımla
    options = Options()
    options.add_argument('--headless')

    # Web sürücüsünü başlat
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        driver = webdriver.Chrome(options=options)

    # Web sayfasını yükle
    driver.get(url)

    # Dropdown öğesini bul
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "margin-right-small.large-up-margin-right-medium")))

    # Öğenin içeriğini kaydet
    original_content = dropdown.get_attribute("innerHTML")

    # Mouse imlecini öğenin üzerine getir
    ActionChains(driver).move_to_element(dropdown).perform()

    # Sayfanın hover olup olmadığını kontrol et
    if dropdown.get_attribute("innerHTML") != original_content:
        first_result = "PASS"
    else:
        first_result = "FAIL"

    import requests
    from bs4 import BeautifulSoup
    import re

    response = requests.get(url)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]

    hintce_karakter_toplam = 0
    second_result = "FAIL"
    for link in links[:5]:
        inner_url = url + link
        inner_response = requests.get(inner_url)
        inner_content = inner_response.content
        inner_soup = BeautifulSoup(inner_content, "html.parser")
        inner_text = inner_soup.get_text()
        hintce_karakterler = re.findall(r'[\u0900-\u097F]', inner_text)
        hintce_karakter_sayisi = len(hintce_karakterler)
        hintce_karakter_toplam += hintce_karakter_sayisi
        if inner_text:
            inner_text_len = len(inner_text)
            if hintce_karakter_toplam / inner_text_len > 0.2:
                second_result = "PASS"
            else:
                second_result = "FAIL"

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import cv2
    import numpy as np
    import requests
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # tarayıcı arayüzünü gizle
    chrome_options.add_argument('--disable-gpu')  # GPU kullanımını devre dışı bırak

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    img_tags = driver.find_elements(By.TAG_NAME, 'img')
    img_urls = [img.get_attribute('src') for img in img_tags]

    threshold = 100
    is_blurry = False
    fail_count = 0

    for url in img_urls:
        try:
            img = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@src='" + url + "']")))
            img_arr = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, cv2.IMREAD_GRAYSCALE)
            blur_metric = cv2.Laplacian(img, cv2.CV_64F).var()
            if blur_metric < threshold:
                is_blurry = True
                fail_count += 1
        except:
            continue

    driver.quit()

    if fail_count / len(img_urls) > 0.8:
        third_result = "FAIL"
    else:
        third_result = "PASS"

    if first_result == "PASS" and second_result == "PASS" and third_result == "PASS":
        return "PASS"
    else:
        result = "FAIL, "
        errors = []
        if first_result != "PASS":
            errors.append("Javascript dropdown not working properly")
        if second_result != "PASS":
            errors.append("Inner pages not translated")
        if third_result != "PASS":
            errors.append("Images not high resolution")
        result += ", ".join(errors)
        return result

