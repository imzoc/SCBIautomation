import pyautogui
import time
import glob

""" This is a project that uses pyautogui and opencv to automatically
navigate the Global Trade HQ (GTHQ) in SimCity BuildIt. This includes:
* Pressing the refresh button within the GTHQ,
* Detecting and fetching the screen coordinates of desired items in the
GTHQ and depots.
* Clicking on desired items in the GTHQ (i.e. visiting it's depot) and
in depots (i.e. buying items. buy_all buys all desired items in the
current depot).
* From a depot, navigating to my home city. This predictably angles the
camera towards the GTHQ, so we can automate entering the GTHQ again and
close the loop.

OpenCV uses .png files located in internals/ and items/.

This project takes control of the mouse. Be careful.

This project can sometimes get out of control because I didn't code for
all possibilities, such as being in a depot, trying to buy an item, and
not being able to because storage is full. However, all functions call
wait_until_load() before executing, which will wait to execute the
function until it detects the GTHQ or a depot with items in it, so you
can usually press <ESC> and stop things from going haywire. 

So far, only {steel, lock, burger} have .png files that opencv can use
to detect actual items in the GTHQ or depots. You will need to screen-
capture and add your own .png files for other items.
"""

class SCBI:
    # takes a tuple of (left, top, width, height) and returns middle_x, middle_y
    def unwrap_coordinates(item):
        left, top, width, height = item[0], item[1], item[2], item[3]
        return left + width / 2, top + height / 2

    # If item_names is not a list, it puts item_names into a new list.
    # Then, it ensures that strings are the only items in item_names.
    def validate_item_names(item_names):
        if not type(item_names) is list:
            item_names = [item_names]

        for item_name in item_names:
            if not type(item_name) is str:
                raise TypeError

        return item_names

    # stalls until pyautogui detects a visual cue that indicates that
    # the depot or GTHQ has loaded.
    def wait_until_load():
        loaded = False
        while not loaded:
            for file_path in glob.glob('internals/*_loaded.png'):
                try:
                    pyautogui.locateOnScreen(file_path, confidence=0.95)
                    loaded = True
                    break
                except pyautogui.ImageNotFoundException:
                    pass
    # refreshes the GTHQ, if possible
    def refresh():
        SCBI.wait_until_load()
        try:
            item = pyautogui.locateOnScreen('internals/refresh.png', confidence=0.90)
            x, y = SCBI.unwrap_coordinates(item)
            pyautogui.click(x, y)
            print('refresh: GTHQ has been refreshed.')
        except pyautogui.ImageNotFoundException:
            print('refresh: cannot refresh.')
    
    # detects if any items in item_names is listed in {where}.
    # {where} can be 'depot' or 'GTHQ'
    # Returns None if no such items are found.
    # Returns x, y coordinates of the first found item otherwise. 
    def detect(item_names, where):
        SCBI.wait_until_load()
        item_names = SCBI.validate_item_names(item_names)
        if where not in ['GTHQ', 'depot']:
            print("detect: WARNING: due to 'where' not being 'GTHQ' or 'depot',\
            program may look in wrong filesystem location.")

        for item_name in item_names:
            try:
                item = pyautogui.locateOnScreen(f'items/{where}/{item_name}.png', confidence=0.80)
                print(f"detect: an item has been found in {where}.")
                x, y = SCBI.unwrap_coordinates(item)
                return ((x, y))
            except pyautogui.ImageNotFoundException:
                pass
            except OSError:
                print(f"detect: WARNING: did not find .png file for item in /items/{where}")
        print(f'detect: no items were found in {where}')
        return None

    # clicks on item_coordinates
    def visit(item_coordinates):
        SCBI.wait_until_load()
        if item_coordinates is None:
            print('visit: no item to visit.')
            return
        pyautogui.click(item_coordinates[0], item_coordinates[1])
        print("visit: visiting item's depot")
        return
    
    # determines if any items in item_names are listed in the depot.
    # If not, does nothing.
    # If so, clicks on first found item to buy it.
    def buy(item_names):
        SCBI.wait_until_load()
        item_names = SCBI.validate_item_names(item_names)

        for item_name in item_names:
            pyautogui.moveTo(500, 100)
            try:
                item = pyautogui.locateOnScreen('items/depot/' + item_name + '.png', confidence=0.90)
                x, y = SCBI.unwrap_coordinates(item)
                pyautogui.click(x, y)
                print('buy: item has been bought.')
                return
            except pyautogui.ImageNotFoundException:
                pass
        print('buy: no items found.')
    
    # Uses buy to buy all instances of items in item_names in the current depot.
    def buy_all(item_names):
        item_names = SCBI.validate_item_names(item_names)
            
        while True:
            SCBI.wait_until_load()
            if SCBI.detect(item_names, 'depot'):
                SCBI.buy(item_names)
            else:
                break
        print('buy_all: all items have been bought.')

    # navigates to your home city from another depot. 
    def home():
        try:
            button = pyautogui.locateOnScreen('internals/home_button_1.png', confidence=0.90)
            x, y = SCBI.unwrap_coordinates(button)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            try:
                # untested
                gift = pyautogui.locateOnScreen('internals/gift.png', confidence=0.9)
                x1, y1 = SCBI.unwrap_coordinates(gift)
                pyautogui.click(x1, y1)
                pyautogui.moveTo(x, y)
            except pyautogui.ImageNotFoundException:
                pass
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        except pyautogui.ImageNotFoundException:
            print('home: button not found')
    
    # enters the GTHQ from your home city. This function depends on
    # hard-coded GTHQ coordinates. My monitor is 1920 x 1080 and my
    # BlueStacks window takes up exactly one quarter of the
    # screen on the top left.
    def enter_GTHQ():
        # ensure game enters loading screen before this function executes
        time.sleep(0.5)
        # wait until loading screen finishes
        while True:
            try:
                pyautogui.locateOnScreen('internals/game_loading.png', confidence=0.95)
            except pyautogui.ImageNotFoundException:
                # loading screen has finished.
                time.sleep(2)

                # GTHQ location on screen is somewhat predictable. This
                # provides a margin of error.
            
                pyautogui.moveTo(220, 300)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                
                pyautogui.moveTo(250, 250)
                pyautogui.mouseDown()
                pyautogui.mouseUp()

                pyautogui.moveTo(280, 200)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                
                pyautogui.moveTo(325, 150)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                
                pyautogui.moveTo(325, 100)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                
                
                return
            
    # offsets the item listings in GTHQ and depot so that one extra column is visible
    def offset(x):
        SCBI.wait_until_load()
        pyautogui.moveTo(780, 300)
        pyautogui.drag(x, 0, 0.3, button='left')
        time.sleep(0.5)
        return



            
