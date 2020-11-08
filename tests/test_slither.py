import time
from selenium.webdriver.common.action_chains import ActionChains
from pylenium.driver import Pylenium


def test_slither_io(py: Pylenium, fake):
    py.visit('https://slither.io')
    py.get('#nick').type(fake.first_name())
    py.getx("//div[@id='playh']//div[contains(text(), Play)]").click()
    in_game = True
    while in_game:
        time.sleep(1)
        container = py.contains('Your rank:').parent()
        if 'opacity: -1;' in container.get_attribute('style'):
            in_game = False  # hidden, which means we are not in the game
            break
        py.screenshot('state.png')
        actions = ActionChains(py.webdriver)
        actions.move_by_offset(200, 200).perform()
        actions.move_by_offset(0, 0).perform()
