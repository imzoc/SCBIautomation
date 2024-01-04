from SCBIautomation import SCBI
import time

"""
This macro will scan the global trade center for desired items and buy any
that appear. It requires that the Global Trade HQ be already opened.
"""
desired_items = ['steel']
# In the GTHQ
while True:
    SCBI.refresh()
    SCBI.wait_until_load()
    start = time.time()
    while True:
        item_coordinates = SCBI.detect(desired_items, 'GTHQ')
        if item_coordinates is None:
            SCBI.offset(-500)
            item_coordinates = SCBI.detect(desired_items, 'GTHQ')
        if item_coordinates is None:
            time.sleep(30 + start - time.time())
            break
        SCBI.visit(item_coordinates)
        SCBI.buy_all(desired_items)
        SCBI.home()
        SCBI.enter_GTHQ()