from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

class PluginWidget(QWidget):
  def __init__(self, name):
    super(PluginWidget, self).__init__()

    self.name = name
    #self.image_path = image_path
    #self.enabled = QLabel("True

    self.lbl = QLabel(self.name)
    #self.img = QPixmap(self.image_path)
    self.hbox = QHBoxLayout()
    self.hbox.addWidget(self.lbl)
    #self.hbox.addWidget(self.img)
    self.setLayout(self.hbox)

  def show(self):
    """
    Show this widget, and all child widgets.
    """
    for w in [self, self.lbl]:
        w.setVisible(True)

  def hide(self):
    """
    Hide this widget, and all child widgets.
    """
    for w in [self, self.lbl]:
        w.setVisible(False)