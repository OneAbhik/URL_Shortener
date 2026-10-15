import sys
import pyshorteners
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # window
        self.setWindowTitle("URL Shortener")
        self.setGeometry(300, 300, 450, 300)

        # layout
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        # instruction label
        self.instruction_label = QLabel("Enter long URL:")

        # input field
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/very/long/link")

        # shorten button
        self.shorten_button = QPushButton("Shorten URL")
        self.shorten_button.clicked.connect(self.shorten_url)

        # result label, empty at start
        self.result_label = QLabel("")

        # copy button, disabled at start
        self.copy_button = QPushButton("Copy")
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # add to layout, top to bottom
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.shorten_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

        # CSS styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 8px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #74c7ec;
            }
            QPushButton:disabled {
                background-color: #45475a;
                color: #7f849c;
            }
        """)

    def shorten_url(self):
        long_url = self.url_input.text().strip()

        # validation
        if not long_url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return

        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)

            # clickable link
            self.short_url = short_url
            self.result_label.setText(
                f'<a href="{short_url}" style="color:#89b4fa;">{short_url}</a>'
            )
            self.result_label.setOpenExternalLinks(True)

            # enable copy
            self.copy_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to shorten URL:\n{e}")

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.short_url)
        QMessageBox.information(self, "Copied", "Short URL copied to clipboard.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec_())