# from PyQt5.Qt import *
# from PyQt5.QtWidgets import QWidget, QLabel, QApplication
# import sys
#
# #继承QLabel
# class MyLabel(QLabel):
#     def __init__(self,*a,**b):
#         super(MyLabel, self).__init__(*a,**b)
#
#     def setSec(self,sec):
#         ''' 设置标签的文本，用文本来显示剩余时间 '''
#         self.setText(str(sec))
#
#     def myStartTimer(self,sec_ms):
#         ''' 设置定时器每次减少的时间，startTimer()会返回一个值，用来结束定时 '''
#         self.time_id = self.startTimer(sec_ms)
#
#     def timerEvent(self, QTimerEvent):
#         ''' 定时器相对应的方法，定时器减少相应时间都会调用这个函数 '''
#         sec = int(self.text())-1
#         self.setText(str(sec))
#         if(sec==0):
#             print('倒计时结束')
#             self.killTimer(self.time_id)  #结束定时
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = QWidget()
#     window.resize(400,300)
#     label = MyLabel(window)
#     label.move(100,50)
#     label.setSec(10)
#     label.myStartTimer(500)
#     window.show()
#     sys.exit(app.exec_())
#
#


# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore
# # import qdarkstyle
#
# global sec
# sec = 0
#
#
# class WorkThread(QThread):
#     trigger = pyqtSignal()
#
#     def __int__(self):
#         super(WorkThread, self).__init__()
#
#     def run(self):
#         for i in range(2000000000):
#             pass
#
#         # 循环完毕后发出信号
#         self.trigger.emit()
#
#
# def countTime():
#     global sec
#     sec += 1
#     # LED显示数字+1
#     lcdNumber.display(sec)
#
#
# def work():
#     # 计时器计时
#     print("#30")
#     timer.start(1000)  # 将start写成statr居然不报错，但是找bug却找了半天
#     # 计时开始
#     workThread.start()
#     # 当获得循环完毕的信号时，停止计时
#     workThread.trigger.connect(timeStop)
#
#
# def timeStop():
#     print("#38")
#     timer.stop()
#     print("计时结束，共计用时：", lcdNumber.value())
#     global sec
#     sec = 0
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     top = QWidget()
#     top.resize(300, 200)
#     # 影藏边框
#     # top.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#     layout = QVBoxLayout(top)
#     lcdNumber = QLCDNumber()
#     layout.addWidget(lcdNumber)
#     button = QPushButton("开始")
#     layout.addWidget(button)
#
#     timer = QTimer()
#     workThread = WorkThread()
#     button.clicked.connect(work)
#     # 计时结束，触发countime
#     timer.timeout.connect(countTime)
#     # 进行渲染
#     # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#     top.show()
#     sys.exit(app.exec_())



import sys
import GPIO
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLCDNumber, QVBoxLayout, QHBoxLayout, QPushButton

class Timer(QWidget):
    def __init__(self):
        super(Timer, self).__init__()

        self.sec = 0

        self.hourLCDNumber = QLCDNumber()
        self.hourLCDNumber.setDigitCount(2)
        self.hourLCDNumber.display(00)

        self.minLCDNumber = QLCDNumber()
        self.minLCDNumber.setDigitCount(2)
        self.minLCDNumber.display(00)

        self.secLCDNumber = QLCDNumber()
        self.secLCDNumber.setDigitCount(2)
        self.secLCDNumber.display(00)

        self.startSuspendButton = QPushButton('开始')
        self.restartButton = QPushButton('重置')

        self.startSuspendButton.clicked.connect(self.startSuspend)
        self.restartButton.clicked.connect(self.restart)

        hTimerLayout = QHBoxLayout()
        hTimerLayout.addWidget(self.hourLCDNumber)
        hTimerLayout.addWidget(self.minLCDNumber)
        hTimerLayout.addWidget(self.secLCDNumber)

        hButtonLayout = QHBoxLayout()
        hButtonLayout.addWidget(self.startSuspendButton)
        hButtonLayout.addWidget(self.restartButton)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hTimerLayout)
        vLayout.addLayout(hButtonLayout)

        self.setLayout(vLayout)

    def operate(self):
        self.sec += 1
        min, sec = divmod(self.sec, 60)
        hour, min = divmod(min, 60)

        self.hourLCDNumber.display(hour)
        self.minLCDNumber.display(min)
        self.secLCDNumber.display(sec)

    def startSuspend(self):
        bText = self.startSuspendButton.text()
        if bText == '开始' or bText == '继续':
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.operate)
            self.timer.start(1000)
            self.startSuspendButton.setText('暂停')
            
            GPIO.setup()
            GPIO.loop()
        elif bText == '暂停':
            self.timer.deleteLater()
            self.startSuspendButton.setText('继续')
            
            GPIO.destroy()

    def restart(self):
        self.sec = -1
        self.operate()
        if self.startSuspendButton.text() == '暂停':
            self.timer.deleteLater()
            GPIO.destroy()
        self.startSuspendButton.setText('开始')


app = QApplication(sys.argv)
timer = Timer()
timer.show()
sys.exit(app.exec_())
