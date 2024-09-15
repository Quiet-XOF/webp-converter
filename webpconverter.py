import os
import sys
from PIL import Image
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class converterGUI(QWidget):
    def __init__(self):
        super().__init__()
        # Header
        self.setWindowTitle("Convert .WEBP")
        self.setWindowIcon(QIcon("icon.png"))
        self.layout = QGridLayout(self)
        # Save as .png
        self.png_radio = QRadioButton("Save as .png")
        self.layout.addWidget(self.png_radio, 0, 0)
        self.png_radio.setChecked(True)  # Default file type
        # Save as .jpg
        self.jpg_radio = QRadioButton("Save as .jpg")
        self.layout.addWidget(self.jpg_radio, 0, 1)
        # Delete old files
        self.delete_original = QCheckBox("Delete Original .webp Image(s)")
        self.layout.addWidget(self.delete_original, 1, 0, 1, 2)
        # Selected file display
        self.file_display = QListWidget()
        self.layout.addWidget(self.file_display, 2, 0, 1, 2)
        # Process Button
        self.process_button = QPushButton("Process File(s)")
        self.layout.addWidget(self.process_button, 3, 0, 1, 2)
        self.process_button.clicked.connect(self.process_files)
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        # Add selected files
        self.add_file_btn = QPushButton("Select File(s)")
        self.layout.addWidget(self.add_file_btn, 5, 0)
        self.add_file_btn.clicked.connect(self.select_files)
        # Add entire folder
        self.add_folder_btn = QPushButton("Select Folder")
        self.layout.addWidget(self.add_folder_btn, 6, 0)
        self.add_folder_btn.clicked.connect(self.select_folder)
        # Delete selected files
        self.delete_file_btn = QPushButton("Delete File(s)")
        self.layout.addWidget(self.delete_file_btn, 5, 1)
        self.delete_file_btn.clicked.connect(self.delete_file)
        # Delete all files
        self.delete_folder_btn = QPushButton("Delete All")
        self.layout.addWidget(self.delete_folder_btn, 6, 1)
        self.delete_folder_btn.clicked.connect(self.delete_all)

    def select_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilters(["Webp files (*.webp)"])
        files = []
        if file_dialog.exec():
            files += file_dialog.selectedFiles()
        self.update_list(files)

    def select_folder(self):
        file_dialog = QFileDialog.getExistingDirectory(self, "Select Folder")
        files = []
        for file_name in os.listdir(file_dialog):
            if file_name.endswith(".webp"):
                files.append(os.path.abspath(file_name))
        self.update_list(files)

    def delete_file(self):
        if self.file_display.currentRow() != -1:
            self.file_display.takeItem(self.file_display.currentRow())

    def delete_all(self):
        self.file_display.clear()

    def update_list(self, files):
        try:
            for file_name in files:
                if not self.file_display.findItems(file_name, Qt.MatchExactly):
                    item = QListWidgetItem(file_name)
                    self.file_display.addItem(item)
        except Exception as e:
            self.error(e)
            return

    def process_files(self):
        if self.file_display.count() == 0:
            QMessageBox.warning(self, "No Files Selected", "Please use \"Select File(s)\" or \"Select Folder\" to choose files to convert.")
        else:
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(self.file_display.count())
            if self.jpg_radio.isChecked():
                extension = ".jpg"
            else:
                extension = ".png"
            for file in range(self.file_display.count()):
                path = self.file_display.item(file).text()
                try:
                    image = Image.open(path)
                    image.save(path.split(".", 1)[0] + extension)
                    if self.delete_original.isChecked():
                        os.remove(path)
                except Exception as e:
                    self.error(e)
                    return
                self.progress_bar.setValue(file + 1)
            information = f"All files have been converted to {extension}"
            if self.delete_original.isChecked():
                information += "\nThe original .webp file(s) were deleted."
            QMessageBox.information(self, "Task Complete", information)
            self.file_display.clear()
            self.progress_bar.reset()

    def error(self, e):
        QMessageBox.critical(self, "UH OH! UH OH!", f"SOMETHING HAS GONE TERRIBLY WRONG!\nERROR: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = converterGUI()
    #window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
