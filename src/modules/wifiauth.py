import urllib.request as request


def is_Connected(url="http://www.youtube.com", timeout=3):
    try:
        request.urlopen(url, timeout=timeout)
        return True
    except Exception as e:
        print(e)
        return False
