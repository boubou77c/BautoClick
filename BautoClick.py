import sys
import threading
import keyboard
import pyautogui
import time

from PyQt5.QtWidgets import QKeySequenceEdit, QDoubleSpinBox,QCheckBox,QSpinBox,QWidget,QApplication,QLabel,QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QKeySequence



class Window(QWidget):
    #Initialize the constructor
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        #Default setting window
        ui = uic.loadUi("bautoclick.ui",self)
        ui.setFixedSize(421,521)
        ui.setWindowTitle("BautoClick")


        #Get the widget
        #spinbox
        self.number_frequency = ui.findChild(QDoubleSpinBox,"nm_fq")
        self.time = ui.findChild(QSpinBox, "nm_time")

        #checkbox
        self.infinite_freq = ui.findChild(QCheckBox,"cb_inf_freq")

        #but / label status
        self.but_start = ui.findChild(QPushButton,"but_start")
        self.status = ui.findChild(QLabel,"status")

        #setting but
        self.set_but = ui.findChild(QPushButton,"setting_but")

        # Initialize state
        self.state: bool = False

        #connect button
        self.get_time:float = self.time.value()
        self.get_freq:float = self.number_frequency.value()
        self.but_start.clicked.connect(lambda :self.start(self.get_time,self.get_freq))

        #Shortcut
        self.shortcut = ui.findChild(QKeySequenceEdit,"key_seq")
        self.save_ct = ui.findChild(QPushButton,"save_sc")

        #Save the ShortCut
        self.save_ct.clicked.connect(self.edit_shortcut)

        #Set the inital shortcut -> M
        self.initial_shortcut()


    def initial_shortcut(self):
        # initial shortcut
        self.hot_key:str = "M"
        self.shortcut.setKeySequence(QKeySequence("M"))
        keyboard.add_hotkey(self.hot_key, lambda: self.start(self.get_time, self.get_freq))

    def edit_shortcut(self) -> bool:
        try:
            # Set the new shortcut
            new_shortcut:str = self.shortcut.keySequence().toString()
            # If the keySequence has more than 1 shortcut -> delete
            if len(new_shortcut) > 1:
                self.shortcut.clear()
            # Remove the old shortcut
            keyboard.remove_hotkey(self.hot_key)
            self.hot_key = new_shortcut
            # Add the new shortcut
            keyboard.add_hotkey(self.hot_key, lambda: self.start(self.get_time, self.get_freq))
            return True
        except Exception:
            self.initial_shortcut()
            print("Shortcut reset 'M' : No shortcut entered.")
            return False


    def start(self,tm,frq):
        #get the time and the frequency
        get_time:float = self.time.value()
        get_freq:float = self.number_frequency.value()

        #if it is checked, time  = 10000 -> infinite time
        if (self.infinite_freq.isChecked()):
            #Create a thread with infinte timemm
            get_time:int = 10000
            self.th_click = threading.Thread(target=self.click, args=(get_time, get_freq,))
            self.th_click.start()

        #else time is what the user want
        else:
            #Create a thread with defined time
            self.th_click = threading.Thread(target=self.click, args=(get_time, get_freq,))
            self.th_click.start()



    def click(self,tm=0,freq=0):

        #Reverse self.state -> To disable or enable
        self.state = not self.state

        #Infinite time == 10000 sec
        if(tm==10000):

            #End chrono -> Current time + infinite time
            end_time = time.time() + 10000

        #Time defined by the user
        else:
            #End chrono -> Current time + defined time
            end_time:float = time.time() + tm

        #Change the status and button text
        self.but_start.setText("Stop")
        self.status.setText("Status : Enabled")

        #Text status force update
        QApplication.processEvents()

        #Loop to do the auto click
        while time.time() < end_time :
            #If it is True -> Click / Else -> Stop
            if (self.state):
                pyautogui.click()
                print("click")
                time.sleep(freq)
            else:
                break

        #It is finished -> Put back the old text
        self.but_start.setText("Start")
        self.status.setText("Status : Disabled")




app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
