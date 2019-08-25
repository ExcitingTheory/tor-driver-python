
import pprint
import socket
import subprocess

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def isVisible(_driver, locator, timeout=20):
    try:
        WebDriverWait(_driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        return True
    except TimeoutException:
        return False

def isNotVisible(_driver, locator, timeout=20):
    try:
        WebDriverWait(_driver, timeout).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        return True
    except TimeoutException:
        return False

def checkListeningPort(address, port):
    _socket = socket.socket()
    try:
        _socket.connect((address, port))
        return True
    except socket.error:
        return False
    finally:
        _socket.close()

class TorDriver:
    host = 'localhost'
    port = 9150
    _binary = FirefoxBinary(r'/home/username/.local/share/torbrowser/tbb/x86_64/tor-browser_en-US/Browser/firefox')
    _profileTor = '/etc/tor/'
    _defaultProfile = ''
    connected = False


    def setupProfile(self):
        _profile = FirefoxProfile(self._profileTor)
        _profile.set_preference("places.history.enabled", False)
        _profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        _profile.set_preference("privacy.clearOnShutdown.passwords", True)
        _profile.set_preference("privacy.clearOnShutdown.siteSettings", True)   
        _profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        _profile.set_preference("signon.rememberSignons", False)
        _profile.set_preference("network.cookie.lifetimePolicy", 2)
        _profile.set_preference("network.dns.disablePrefetch", True)
        _profile.set_preference("network.http.sendRefererHeader", 0)
        _profile.set_preference("network.proxy.type", 1)
        _profile.set_preference("network.proxy.socks_version", 5)
        _profile.set_preference("network.proxy.socks", '127.0.0.1')
        _profile.set_preference("network.proxy.socks_port", 9150)
        _profile.set_preference("network.proxy.socks_remote_dns", True)
        _profile.set_preference("javascript.enabled", False)
        _profile.set_preference("permissions.default.image", 2)
        _profile.set_preference("http.response.timeout", 120000)
        _profile.set_preference("dom.max_script_run_time", 120000)

        return _profile

    def setupWebdriver(self):
        _binary = self._binary
        _profile = self.setupProfile()
        
        _driver = webdriver.Firefox(firefox_profile=_profile, firefox_binary=_binary)
        return  _driver

    def setupTor(self):
        torProcess = subprocess.run("bash -c torbrowser-launcher", shell=True, check=True)
        pprint.pprint(torProcess)
        while not self.connected:
            try:
                self.connected = checkListeningPort(self.host, self.port)
            except Exception as e:
                print(e)
                pass

    def __init__(self, binaryLocation=None, profileLocation=None):

        if binaryLocation:
            self._binary = FirefoxBinary(binaryLocation)

        
        if profileLocation:
            self._profileTor = profileLocation


