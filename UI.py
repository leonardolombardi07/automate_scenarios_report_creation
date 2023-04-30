# External imports
import pyautogui
import time
import pathlib
from typing import Tuple


# Leo: I'm assuming the screen size is constant during program execution
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Screen factor to convert when another screen is used than the standard
# of 1920x1080
RESOLUTION_FACTOR = (SCREEN_WIDTH/1920, SCREEN_HEIGHT/1080)

# Enable experimental code, like trying to detect when an image was saved
# this code can cause bugs or unexpected behaviour, like infinite loops
ENABLE_EXPERIMENTAL_CODE = True


def get_command_window_position():
    # TODO: Leo: make sure this is the correct position in any screen
    # Leo: created a separated function because it seems we'll need to do more
    # calculations to find the right position in any screen
    return (1906, 1003)


def convert_resolution(position: Tuple[int, int]):
    '''Get the right position of a given point considering any screen size'''
    return (position[0]*RESOLUTION_FACTOR[0], position[1]*RESOLUTION_FACTOR[1])


def write_on_command_window(text: str):
    command_window_pos = get_command_window_position()
    pyautogui.click(convert_resolution(command_window_pos))
    pyautogui.write(text)
    pyautogui.press("enter")


def drag_step_cursor_to_final_step():
    step_cursor_pos = (14, 312)
    pyautogui.mouseDown(convert_resolution(
        step_cursor_pos, RESOLUTION_FACTOR), button="left")
    pyautogui.moveTo(SCREEN_WIDTH - 10, 0)
    pyautogui.mouseUp(SCREEN_HEIGHT - 10, 319, button="left")


def copy_current_image_to_clipboard():
    file_button_pos = (21, 40)
    pyautogui.click(convert_resolution(file_button_pos))
    copy_img_button_pos = (59, 440)
    pyautogui.click(convert_resolution(copy_img_button_pos))


def wait_until_image_saved__EXPERIMENTAL(image_path: pathlib.Path, max_wait_time_in_ms: int = 10000):
    # Some other possible solutions:
    # 1) https://stackoverflow.com/questions/70306307/python-how-can-i-asynchronously-save-the-pil-images
    # 2) https://discourse.techart.online/t/pil-wait-for-image-save/3994/5

    if ENABLE_EXPERIMENTAL_CODE == False:
        return

    start_time = end_time = time.time()
    elapsed_time = end_time - start_time
    while elapsed_time < max_wait_time_in_ms:
        if image_path.is_file():
            return

        elapsed_time = time.time() - start_time

    print(
        f"Time of {max_wait_time_in_ms}ms exceeded to check if image with path '{image_path}' was saved. Check if {wait_until_image_saved__EXPERIMENTAL.__name__} is working properly"
    )
