# A class that provides setup and configuration of a firefox profile, and binary location for firefox, and assists in downloading geckodriver.
import pprint
import socket
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# Checks if an element is visible
def isVisible(_driver, locator, timeout=20):
    try:
        WebDriverWait(_driver, timeout).until(
            expected_conditions.visibility_of_element_located((
                By.CSS_SELECTOR, locator)))

        return True
    except TimeoutException:
        return False

# Checks if a port is listening
def checkListeningPort(address, port):
    _socket = socket.socket()
    try:
        _socket.connect((address, port))
        return True
    except socket.error:
        return False
    finally:
        _socket.close()

# A class to handle the TorBrowser WebDriver.
class TorDriver:
    host = 'localhost'
    port = 9150
    ctrlPort = 9151
    _binary = FirefoxBinary(r'/home/username/.local/share/torbrowser/tbb/x86_64/tor-browser/Browser/firefox')
    _profileTor = '/home/username/.local/share/torbrowser/tbb/x86_64/tor-browser/Browser/TorBrowser/Data/Browser/profile.default'
    _defaultProfile = ''
    connected = False
    geckodriverUrl = "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
    geckodriverPath = "."
    geckodriverExecutable=f"./geckodriver"

    # Allow for overriding the binary and profile locations
    def __init__(self, binaryLocation=None, profileLocation=None):
        if binaryLocation:
            self._binary = FirefoxBinary(binaryLocation)
        if profileLocation:
            self._profileTor = profileLocation

    # Sets up the firefox profile for the webdriver instance. 
    def setupProfile(self):
        _profile = FirefoxProfile(self._profileTor)

        # The following lines 61-96 are from the firefox profile setup of tbselenium http://github.com/webfp/tor-browser-selenium
        _profile.set_preference('browser.startup.page', "0")
        _profile.set_preference('torbrowser.settings.quickstart.enabled', True)
        _profile.set_preference('browser.startup.homepage', 'about:newtab')
        _profile.set_preference('extensions.torlauncher.prompt_at_startup', 0)
        # load strategy normal is equivalent to "onload"
        _profile.set_preference('webdriver.load.strategy', 'normal')
        # disable auto-update
        _profile.set_preference('app.update.enabled', False)
        _profile.set_preference('extensions.torbutton.versioncheck_enabled', False)
        _profile.set_preference('extensions.torbutton.prompted_language', True)
        # https://gitlab.torproject.org/tpo/applications/tor-browser/-/issues/41378
        _profile.set_preference('intl.language_notification.shown', True)
        # Configure Firefox to use Tor SOCKS proxy
        _profile.set_preference('network.proxy.socks_port', self.port)
        _profile.set_preference('extensions.torbutton.socks_port', self.port)
        _profile.set_preference('extensions.torlauncher.control_port', self.ctrlPort)

        _profile.set_preference('extensions.torlauncher.start_tor', False)
        # TODO: investigate whether these prefs are up to date or not
        _profile.set_preference('extensions.torbutton.block_disk', False)
        _profile.set_preference('extensions.torbutton.custom.socks_host', '127.0.0.1')
        _profile.set_preference('extensions.torbutton.custom.socks_port', self.port)
        _profile.set_preference('extensions.torbutton.inserted_button', True)
        _profile.set_preference('extensions.torbutton.launch_warning', False)
        _profile.set_preference('privacy.spoof_english', 2)
        _profile.set_preference('extensions.torbutton.loglevel', 2)
        _profile.set_preference('extensions.torbutton.logmethod', 0)
        _profile.set_preference('extensions.torbutton.settings_method', 'custom')
        _profile.set_preference('extensions.torbutton.use_privoxy', False)
        _profile.set_preference('extensions.torlauncher.control_port', self.port)
        _profile.set_preference('extensions.torlauncher.loglevel', 2)
        _profile.set_preference('extensions.torlauncher.logmethod', 0)
        _profile.set_preference('extensions.torlauncher.prompt_at_startup', False)
        # disable XPI signature checking
        _profile.set_preference('xpinstall.signatures.required', False)
        _profile.set_preference('xpinstall.whitelist.required', False)

        # Disable various features that leak information, see https://www.ghacks.net/overview-firefox-aboutconfig-security-privacy-preferences/
        _profile.set_preference("places.history.enabled", False)
        _profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        _profile.set_preference("privacy.clearOnShutdown.passwords", True)
        _profile.set_preference("privacy.clearOnShutdown.siteSettings", True)   
        _profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        _profile.set_preference("signon.rememberSignons", False)
        _profile.set_preference("network.cookie.lifetimePolicy", 2)
        _profile.set_preference("network.dns.disablePrefetch", True)
        _profile.set_preference("network.http.sendRefererHeader", 0)
        # Disable images
        _profile.set_preference("permissions.default.image", 2)

        # More network related settings
        _profile.set_preference("network.proxy.type", 1)
        _profile.set_preference("network.proxy.socks_version", 5)
        _profile.set_preference("network.proxy.socks", '127.0.0.1')
        _profile.set_preference("network.proxy.socks_remote_dns", True)

        ##############################
        # This disables javascript, which may break some sites.
        # _profile.set_preference("javascript.enabled", False) # !!!!!
        ##############################

        # Set timeouts
        _profile.set_preference("http.response.timeout", 120000)
        _profile.set_preference("dom.max_script_run_time", 120000)

        return _profile

    # Sets up the webdriver and returns the instance
    def setupWebdriver(self):
        service = Service(
            executable_path=self.geckodriverExecutable,
            service_log_path=self.geckodriverPath,
        )

        options = Options()
        options.binary_location = self._binary
        # options.headless = True # uncomment this to run headless
        options.profile = self.setupProfile()

        _driver = webdriver.Firefox(service=service, options=options)

        return  _driver

    # Downloads the geckodriver binary and extracts it here in a sub-shell to avoid having to manipulate the PATH to include the directory.
    def downloadGeckodriver(self):
        geckodriverProcess = subprocess.run(f"curl -SLO {self.geckodriverUrl} && tar -xvf geckodriver*.tar.gz && rm -f geckodriver*.tar.gz", shell=True, check=True)

    # Run torbrowser-launcher and wait for the port to be listening
    def setupTor(self):
        torProcess = subprocess.run("torbrowser-launcher", shell=True, check=True)
        pprint.pprint(torProcess)
        while not self.connected:
            try:
                self.connected = checkListeningPort(self.host, self.port)
            except Exception as e:
                print(e)
                pass

