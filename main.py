import ui
import sys
import Calculate


if __name__ == '__main__':
    Calculate.test(3, 0, 100, 1, 0.001)
    app = ui.QtWidgets.QApplication(sys.argv)
    mainWindow = ui.QtWidgets.QMainWindow()
    uiWindow = ui.Ui_MainWindow()
    uiWindow.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
    #for i in range(6):
    #    df = Calculate.output(i, 'BPTable', False, False, True)


