# tor-driver-python

Demonstration of how to use the Tor Browser and WebDriver in Python.

## Run the demo

The demo is a simple crawler that visits a few sites and then generates a report. The crawler is written in Python and uses Selenium to drive the Tor Browser.

1. Install the Tor Browser.
2. Run the crawler.
3. Run the report.


Use with the container:

```bash
docker run -it --rm -p 5901:5901 -v "${HOME}/src":/src excitingtheory/kalilinux-xvfb:torbrowser
```

Start the VNC server:

```bash
/opt/start-vnc-server-once.sh
```

Go to the correct directory:

```bash
cd /src/tor-driver-python
```


Run the crawler:

```bash
python3 crawler.py
```

Run the report:

```bash
python3 report.py
```

## results

Schema:

```json
{
    "name": "Meow",
    "file": "./results/meow.json",
    "search": "Meow ",
    "orig": "Meow\n",
    "num": "",
    "artifacts": [
        {
            "data": "Jump to content",
            "link": "https://en.wikipedia.org/wiki/Meow#bodyContent",
            "parent": "https://en.wikipedia.org/wiki/Meow"
        },
        {
            "data": "",
            "link": "https://en.wikipedia.org/wiki/Main_Page",
            "parent": "https://en.wikipedia.org/wiki/Meow"
        },
        {
            "data": "",
            "link": "https://en.wikipedia.org/wiki/Wikipedia:Contents",
            "parent": "https://en.wikipedia.org/wiki/Meow"
        }
        ....
    ]
}
```


## References

* [Tor Browser](https://www.torproject.org/)
* [tbselenium](https://github.com/webfp/tor-browser-selenium)
* [Tor Browser User Manual](https://tb-manual.torproject.org/)
* [Tor Browser Design Specification](https://www.torproject.org/projects/torbrowser/design/)
* [Open Tor Browser with Selenium](https://stackoverflow.com/questions/15316304/open-tor-browser-with-selenium)
* [Upgrading to the latest selenium](https://stackoverflow.com/questions/76433782/robotframework-error-typeerror-webdriver-init-got-an-unexpected-keyword)
