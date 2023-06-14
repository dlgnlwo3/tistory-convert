from PySide6.QtWidgets import QApplication, QLineEdit

from PySide6.QtCore import Qt

class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            # Perform custom action for Ctrl+V
            clipboard = QApplication.clipboard()
            text = clipboard.text()

            # Strip trailing spaces from the pasted text
            stripped_text = text.strip()
            self.insert(stripped_text)
            return

        super().keyPressEvent(event)