import time
import random
from chromedriver import chromedriver, action
from selenium.common.exceptions import MoveTargetOutOfBoundsException


def wait_randomly(min_delay: float, max_delay: float) -> None:
    """
    Wait for a random period of time in a specified interval.
    :param min_delay: Lower bound of the delay.
    :param max_delay: Upper bound of the delay.
    :return: None
    """
    time.sleep(random.uniform(min_delay, max_delay))


def make_mouse_movements(
        min_steps: int,
        max_steps: int,
        min_count: int,
        max_count: int
) -> None:
    """
    Make random mouse movements for a specified time interval.
    :param min_steps: Lower bound of number of steps per movement.
    :param max_steps: Upper bound of number of steps per movement.
    :param min_count: Minimum number of separate movement-chains.
    :param max_count: Maximum number of separate movement-chains.
    :return: None
    """
    count = random.randint(min_count, max_count)
    window_size = chromedriver.get_window_size()
    width, height = window_size.get('width'), window_size.get('height')
    for _ in range(count):
        steps = random.randint(min_steps, max_steps)
        for _ in range(steps):
            horizontal = random.randint(0, width - 1)
            vertical = random.randint(0, height - 1)
            try:
                action.move_by_offset(horizontal, vertical).perform()
            except MoveTargetOutOfBoundsException:
                pass
            wait_randomly(0.5, 1.5)


def scroll_randomly(max_num_times: int) -> None:
    """
    Scroll randomly for a given number of times.
    :param max_num_times: Maximum number of scrolling movements.
    :return: None
    """
    max_delta_y = chromedriver.get_window_size().get('height')
    num_times = random.randint(0, max_num_times)
    for _ in range(num_times):
        wait_randomly(0.1, 0.8)
        delta_y = random.randint(-max_delta_y, max_delta_y)
        action.scroll_by_amount(0, delta_y).perform()

