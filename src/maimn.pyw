from urp_box import *


urp_box_window=Tk()
try:
    b=urp_box(urp_box_window,True)
    urp_box_window.protocol('WM_DELETE_WINDOW', b.close)
    mainloop()
except TclError:
    print("I guess you didn't open S.py")
except AssertionError as e:
    print(e)
    pass
