import config
import random
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@contextmanager
def managed_browser(headless=True):
    """
    Context manager for Selenium browser instances.

    This function provides a context manager for handling Selenium WebDriver instances.
    It configures the browser with various options for headless operation, performance optimization,
    and automation control mitigations.

    Args:
        headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.

    Yields:
        webdriver.Chrome: A configured Selenium WebDriver instance.

    Example:
        with managed_browser(headless=True) as driver:
            driver.get("https://www.example.com")
            print(driver.title)
    """
    service = Service(config.CHROME_DRIVER_PATH)
    options = Options()

    # Set a random user agent to mimic real user behavior
    if config.USER_AGENTS_LIST:
        user_agent = random.choice(config.USER_AGENTS_LIST)
        options.add_argument(f"--user-agent={user_agent}")

    # Enable headless mode
    if headless:
        options.add_argument("--headless=new")

    # Disable video and media autoplay to reduce resource consumption
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    # Disable video and hardware-accelerated decoding for better performance in headless mode
    options.add_argument("--disable-features=MediaPlayback,HardwareMediaKeyHandling,VideoDecodeAcceleration")

    # Other flags to disable GPU and use SwiftShader for CPU-based rendering
    options.add_argument("--disable-gpu")
    options.add_argument("--use-gl=swiftshader")

    # Disable extensions and other features for better performance
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Create a new Chrome WebDriver instance with the configured options
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Yield the WebDriver instance to the context
        yield driver
    finally:
        # Ensure the browser is closed after the context exits
        driver.quit()
