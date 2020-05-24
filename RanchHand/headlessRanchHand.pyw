# Test headless RanchHand

from RanchHand import *


# Run App if Main
if __name__ == '__main__':
    try:
        app()
    except Exception as e:
        print("Exception Occured:", e)
    
window.close()

# END