import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QProgressBar, QMessageBox
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class DriveApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ZaaraCloud - Desktop App')
        self.setGeometry(100, 100, 400, 300)
        
        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(230, 240, 255))
        self.setPalette(palette)

        # Create a layout for better UI arrangement
        layout = QVBoxLayout()

        # Add label
        self.label = QLabel('Upload a file to Google Drive:', self)
        self.label.setFont(QFont('Arial', 12))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Upload Button
        self.uploadBtn = QPushButton('Upload File', self)
        self.uploadBtn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.uploadBtn.clicked.connect(self.upload_file)
        layout.addWidget(self.uploadBtn)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # About Button
        self.aboutBtn = QPushButton('About ZaaraCloud', self)
        self.aboutBtn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        self.aboutBtn.clicked.connect(self.show_about)
        layout.addWidget(self.aboutBtn)

        self.setLayout(layout)

    def authenticate(self):
        creds = None
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)  
            creds = flow.run_local_server(port=0)
        return creds

    def upload_file(self):
        creds = self.authenticate()

        # File dialog to select a file
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'All files (*)')

        if fname:
            # Show a message box confirming file upload start
            QMessageBox.information(self, 'File Upload', f'Starting upload of {fname.split("/")[-1]} to Google Drive.')

            # Start file upload
            service = build('drive', 'v3', credentials=creds)
            file_metadata = {'name': fname.split('/')[-1]}
            media = MediaFileUpload(fname, resumable=True)

            # Update progress bar (in a simple way)
            self.progressBar.setValue(30)  # Simulate partial progress

            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Complete progress
            self.progressBar.setValue(100)

            # Set label to show successful upload
            self.label.setText(f"File uploaded successfully! ID: {file.get('id')}")

            # Reset progress bar
            self.progressBar.setValue(0)

    def show_about(self):
        QMessageBox.about(self, "About ZaaraCloud", "ZaaraCloud allows you to upload and share files seamlessly with Google Drive. Built for everyone by Zaara.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DriveApp()
    ex.show()
    sys.exit(app.exec_())

