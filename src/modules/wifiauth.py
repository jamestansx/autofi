import urllib.request as request


def is_Connected(url="https://stackoverflow.com/", timeout=3):
    try:
        request.urlopen(url, timeout=timeout)
        return True
    except Exception as e:
        print(e)
        return False
