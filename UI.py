from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QCheckBox, QLabel
from PyQt5.QtGui import QFont
import qtawesome as qta

class SnipesterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Snipester')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("QWidget { background-color: #1C2833; }")  # Set the global background color

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_button.setObjectName("refresh-button")
        self.refresh_button.setFixedWidth(100)

        self.refresh_button.setToolTip('Click to refresh the content')  # Add tooltip for refresh button

        button_layout.addWidget(self.refresh_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.setIcon(qta.icon('fa5s.stop', color='white'))
        self.stop_button.setObjectName("stop-button")
        self.stop_button.setFixedWidth(100)

        self.stop_button.setToolTip('Click to stop the current operation')  # Add tooltip for stop button

        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        link_layout = QVBoxLayout()
        self.link_label = QLabel('Enter link here:', self)
        self.link_label.setObjectName("link-label")
        link_layout.addWidget(self.link_label)

        self.link_input = QTextEdit(self)
        self.link_input.setStyleSheet("background-color: #2C3E50; color: #ECF0F1;")
        self.link_input.setFixedHeight(75)
        self.link_input.setAcceptRichText(False)
        link_layout.addWidget(self.link_input)

        self.modified_link_label = QLabel('Altered HTML link:', self)
        self.modified_link_label.setObjectName("modified-link-label")
        link_layout.addWidget(self.modified_link_label)

        self.modified_link_pane = QTextEdit(self)
        self.modified_link_pane.setReadOnly(True)
        self.modified_link_pane.setObjectName("modified-link-pane")
        self.modified_link_pane.setFixedHeight(75)
        self.modified_link_pane.setFont(QFont("Arial", 12))
        link_layout.addWidget(self.modified_link_pane)

        main_layout.addLayout(link_layout)

        checkbox_layout = QHBoxLayout()
        self.debug_checkbox = QCheckBox('Debug', self)
        self.debug_checkbox.setStyleSheet("color: #ECF0F1;")

        self.debug_checkbox.setToolTip('Enable or disable debug mode')  # Add tooltip for debug checkbox

        checkbox_layout.addWidget(self.debug_checkbox)

        self.fallback_checkbox = QCheckBox('Use Web Scraping Fallback', self)
        self.fallback_checkbox.setStyleSheet("color: #ECF0F1;")
        self.fallback_checkbox.setChecked(False)

        self.fallback_checkbox.setToolTip('Use web scraping fallback if enabled')  # Add tooltip for fallback checkbox

        checkbox_layout.addWidget(self.fallback_checkbox)

        self.scrape_link_checkbox = QCheckBox('Scrape Link', self)
        self.scrape_link_checkbox.setStyleSheet("color: #ECF0F1;")
        self.scrape_link_checkbox.setChecked(False)
        checkbox_layout.addWidget(self.scrape_link_checkbox)

        main_layout.addLayout(checkbox_layout)

        self.info_label = QLabel('Information:', self)
        self.info_label.setObjectName("info-label")
        main_layout.addWidget(self.info_label)

        self.info_pane = QTextEdit(self)
        self.info_pane.setReadOnly(True)
        self.info_pane.setObjectName("info-pane")
        self.info_pane.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.info_pane)

        self.debug_label = QLabel('Debug:', self)
        self.debug_label.setObjectName("debug-label")
        main_layout.addWidget(self.debug_label)

        self.debug_pane = QTextEdit(self)
        self.debug_pane.setReadOnly(True)
        self.debug_pane.setObjectName("debug-pane")
        self.debug_pane.show()  # Ensure debug pane is visible

        main_layout.addWidget(self.debug_pane)

        self.end_date_label = QLabel(self)
        self.end_date_label.setObjectName("end-date-label")
        main_layout.addWidget(self.end_date_label)

        self.setLayout(main_layout)

    def get_link_input(self):
        return self.link_input.toPlainText()

    def display_info_data(self, data):
        if data:
            self.info_pane.setHtml(f"<span style='color: green;'>{data}</span>")  # Display data in green
        else:
            self.info_pane.setPlainText("No data available.")  # Inform the user if no data is available
