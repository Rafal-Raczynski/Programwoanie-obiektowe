from app import *

if __name__ == "__main__":
    app = QApplication([])
    img_browser = Covid(1000, 600)
    sys.exit(app.exec_())
