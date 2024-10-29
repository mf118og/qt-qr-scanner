import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import ImageGrab
import pyperclip

class QRCodeScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setGeometry(100, 100, 400, 200)

        # Button to capture screenshot
        self.capture_btn = QtWidgets.QPushButton("Capture QR Code", self)
        self.capture_btn.setGeometry(100, 70, 200, 50)
        self.capture_btn.clicked.connect(self.capture_screenshot)

    def capture_screenshot(self):
        # Hide the window temporarily to avoid capturing it in the screenshot
        self.setWindowOpacity(0.0)
        QtCore.QTimer.singleShot(500, self.take_screenshot)  # Delay to ensure window is hidden

    def take_screenshot(self):
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)

        # Convert screenshot to OpenCV format (BGR color space)
        img = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Decode the QR code
        decoded_objects = decode(img)
        
        # Show the window again
        self.setWindowOpacity(1.0)

        # Check if QR code is detected
        if decoded_objects:
            for obj in decoded_objects:
                # Get the QR code data (link)
                qr_data = obj.data.decode("utf-8")
                self.show_link(qr_data)
                return
        else:
            QMessageBox.warning(self, "No QR Code Found", "No QR code detected in the screenshot.")

    def show_link(self, link):
        # Copy the link to the clipboard
        pyperclip.copy(link)
        
        # Display the link in a message box
        QMessageBox.information(self, "QR Code Link", f"Link: {link}\n\n(Link copied to clipboard)")

def main():
    app = QApplication(sys.argv)
    window = QRCodeScannerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

