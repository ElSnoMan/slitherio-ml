import time
import random
from pylenium.element import Element
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from pylenium.driver import Pylenium

# auto viewport: {1280, 898}
# custom viewport: {800, 800}

bounding_box_coordinates = {
    'top_left': (0, 0),
    'top_center': (400, 0),
    'top_right': (800, 0),
    'right_center': (800, 400),
    'bottom_right': (800, 800),
    'bottom_center': (400, 800),
    'bottom_left': (0, 800),
    'left_center': (0, 400),
    'center': (400, 400)
}


def stats_container(py) -> Element:
    container = py.wait(timeout=3, ignored_exceptions=[StaleElementReferenceException]
                        ).until(lambda _: py.contains('Your rank:').parent())
    return container


def in_game(py) -> bool:
    if 'opacity: -1;' in stats_container(py).get_attribute('style'):
        return False  # because the stats are hidden so we are not in the game
    else:
        return True


def test_slither_io(py: Pylenium, fake):
    py.visit('https://slither.io')
    py.viewport(800, 800)
    py.get('#nick').type(fake.first_name())
    py.getx("//div[@id='playh']//div[contains(text(), Play)]").click()

    game = True
    first_turn = True
    moves = list()
    center = 400, 400

    while game:
        time.sleep(1)
        if not in_game(py):
            break
        py.screenshot('state.png')
        if first_turn:
            x, y = center
            first_turn = False
        else:
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
        move = x, y
        print(move)
        moves.append(move)
        ActionChains(py.webdriver).move_by_offset(x, y).perform()
