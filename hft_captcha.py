x = requests.get("https://trading.hft.vn/CaptchaHandler.ashx", verify=False)
with open("/tmp/py.png", 'wb') as f:
    for chunk in x.iter_content(1024):
        f.write(chunk)