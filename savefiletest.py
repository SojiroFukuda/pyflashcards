from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QTextStream, QFile

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a button
        self.button = QPushButton("Create New Text File", self)
        self.button.clicked.connect(self.create_new_text_file)

    def create_new_text_file(self):
        # Open a file dialog to select the file path and name
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Text File", "", "Text Files (*.txt)")
        
        if file_path:
            # Create a QFile object
            file = QFile(file_path)

            # Open the file in write-only mode
            if file.open(QFile.WriteOnly | QFile.Truncate):
                # Create a QTextStream object to write to the file
                out_stream = QTextStream(file)

                # Write some text to the file
                out_stream << "This is a new text file."

                # Close the file
                file.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
