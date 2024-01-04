This is a project that uses pyautogui and opencv to automatically
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
