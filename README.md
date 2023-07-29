# tor-driver-python

Demonstration of how to use the Tor Browser and WebDriver in Python.

## Run the demo

1. Install the Tor Browser.
2. Run the crawler:

```bash
python3 crawler.py
```

Use with the container:

```bash
docker run -it --rm -p 5901:5901 -v "${HOME}/src":/src excitingtheory/kalilinux-xvfb:torbrowser
```

