# load pyqt widgets
from PyQt6.QtWidgets import * 
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from platformdirs import *
from duckduckgo_images_api import search 
from customwidgets import PluginWidget 
import requests
import imghdr
import sys
import os

appname = "Plugin-Explorer"
appauthor = "trustdarkness"

class pluginType(object):
  def __init__(self, plugin_type, fsroot, extension, enabled):
    self.name = plugin_type
    self.plugin_type = plugin_type
    self.fsroot = fsroot
    self.extension = extension
    self.enabled = enabled

class plugin(object):
  def __init__(self, name, plugin_type):
    self.name = name
    self.plugin_type = plugin_type
    # self.img_file = img_file

AU = pluginType("Component", "/Library/Audio/Plug-Ins/Components", "component", True)
VST = pluginType("VST", "/Library/Audio/Plug-Ins/VST", "vst", True)
VST3 = pluginType("VST3", "/Library/Audio/Plug-Ins/VST3", "vst3", True)

plugtypes = {
  AU.plugin_type : AU,
  VST.plugin_type : VST,
  VST3.plugin_type : VST3
}

AUPlugins = []
VSTPlugins = []
VST3Plugins = []

def trackPlugin(plugin):
  if plugin.plugin_type == "Component":
    if plugin not in AUPlugins:
      AUPlugins.append(plugin)
  elif plugin.plugin_type == "VST":
    if plugin not in VSTPlugins:
      VSTPlugins.append(plugin)
  elif plugin.plugin_type == "VST3":
    if plugin not in VST3Plugins:
      VST3Plugins.append(plugin)

class tabs(QTabWidget):
  def __init__(self, parent=None):
    super(tabs, self).__init__(parent)
    self.ComponentTab = QWidget()
    self.ComponentTab.name = "Component"
    self.VSTTab = QWidget()
    self.VSTTab.name = "VST"
    self.VST3Tab = QWidget()
    self.VST3Tab.name = "VST3"
    #self.MASTab = QWidget()
    self.ttabs = [
      self.ComponentTab,
      self.VSTTab,
      self.VST3Tab
    ]
    
    self.addTab(self.ComponentTab, AU.plugin_type)
    self.addTab(self.VSTTab, VST.plugin_type)
    self.addTab(self.VST3Tab, VST3.plugin_type)

    for ptype in plugtypes:
      self.pluginTabUI(ptype)
    # self.tab2UI()
    # self.tab3UI()
    # self.tab4UI()
    self.setWindowTitle("Plugin Explorer")

    # window size
    self.setGeometry(640, 480, 640, 480)

  def update_display(self, text):
    for tab in self.ttabs:
      for widget in tab.widgets:
        if text.lower() in widget.name.lower():
          widget.show()
        else:
          widget.hide()

  def pluginTabUI(self, plugin_type):
    pt = plugtypes[plugin_type]
    # self.model = QFileSystemModel()
    # self.parent_index = self.model.setRootPath(pt.fsroot)  
    # self.root_index = self.model.index(pt.fsroot)
    # track the plugin type with the model for processing
    #self.model.plugin_type = pt
    currentTab = self.getTabByType(pt.plugin_type)
    currentTab.plugs = QWidget()
    currentTab.widgets = []

    #currentTab.model.setNameFilters(["*.%s" % pt.extension])
    # model.setFilter(QtCore.QDir.Files)
    #currentTab.model.setNameFilterDisables(False)

    currentTab.layout = QVBoxLayout()
    currentTab.scroll = QScrollArea()
    currentTab.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    currentTab.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    currentTab.scroll.setWidgetResizable(True)
    # currentTab.scroll.setWidget(currentTab.controls)
    #currentTab.pluginlist = currentTab.layout.addWidget(QScrollArea())

    self.setTabText(self.getIndexByName(pt.plugin_type),pt.plugin_type)
    currentTab.plugin_names = []
    currentTab.plugin_filenames = os.listdir(pt.fsroot)
    for filename in currentTab.plugin_filenames:
      self.fileProcessor(filename, pt)

    currentTab.plugs.setLayout(currentTab.layout)
    currentTab.scroll.setWidget(currentTab.plugs)
    currentTab.searchbar = QLineEdit()
    currentTab.searchbar.textChanged.connect(self.update_display)
    currentTab.completer = QCompleter(currentTab.plugin_names)
    currentTab.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    currentTab.searchbar.setCompleter(currentTab.completer)
    containerLayout = QVBoxLayout()
    containerLayout.addWidget(currentTab.searchbar)
    containerLayout.addWidget(currentTab.scroll)
    #print(currentTab.model.plugin_type)

    currentTab.setLayout(containerLayout)
    currentTab.show()
    #self.model.directoryLoaded.connect(self.onDirectoryLoaded)

  def getTabByType(self, plugin_type):
    if plugin_type == "Component":
      return self.ComponentTab
    elif plugin_type == "VST":
      return self.VSTTab
    elif plugin_type == "VST3":
      return self.VST3Tab

  def getTabByIndex(self, idx):
    return self.ttabs[idx]
  
  def getNameByIndex(self, idx):
    return self.ttabs[idx].plugin_type
  
  def getIndexByName(self, name):
    for idx, tab in enumerate(self.ttabs):
      if tab.name == name:
        return idx
      
  def fileProcessor(self, filename, pt):
    currentTab = self.getTabByType(pt.name)
    plugin_filename = filename
    plugin_name = plugin_filename.removesuffix(".%s" % pt.extension)
    if plugin_name not in currentTab.plugin_names:
      currentTab.plugin_names.append(plugin_name)
    # results = search(plugin_name)
    # # cross our fingers on getting lucky
    # for r in results["results"]:
    #   img_data = requests.get(r["url"]).content
    #   extension = imghdr.what(file=None, h=img_data)
    #   save_filename = f"{plugin_name}.{extension}"
    #   # we'll keep the original and then scale
    #   save_path = os.path.join(user_data_dir(appname, appauthor), save_filename)
    #   with open(save_path, 'wb') as f:
    #     f.write(img_data)
    #   pixmap = QtGui.QPixmap(save_path)
    #   scaled = pixmap.scaled(100,100, QtCore.Qt.KeepAspectRatio)
    #   scaled_path = f"{plugin_name}_scaled.{extension}"
    #   with open(scaled_path, 'wb') as f:
    #     f.write(scaled)
    #   break
    trackPlugin(plugin(plugin_name, pt.plugin_type))
    pwidget = PluginWidget(plugin_name)
    currentTab.layout.addWidget(pwidget)
    currentTab.widgets.append(pwidget)

  def printIndex(self, index):
        print('model printIndex(): {}'.format(self.model.filePath(index)))

  def traverseDirectory(self, parent_index, callback=None):
    callback(parent_index)
    if self.model.hasChildren(parent_index):
      path = self.model.filePath(parent_index)
      filename = self.model.fileName(parent_index)
      print("iterating: pi - {parent_index} p - {path} fn - {filename}")
      it = QtCore.QDirIterator(path, self.model.filter())
      while it.hasNext():
        if callback:
          cb = "callbackTrue"
        else:
          cb = "callbackFalse"
        childIndex = self.model.index(it.next())
        print("ci: {childIndex} - cb: {cb}")
        self.traverseDirectory(childIndex, callback=callback)

  def onDirectoryLoaded(self):
    self.traverseDirectory(self.parent_index, self.printIndex)
    # self.plugs.setLayout(self.layout)
    # self.scroll.setWidget(self.plugs)
    # self.searchbar = QLineEdit()
    # containerLayout = QVBoxLayout()
    # containerLayout.addWidget(self.searchbar)
    # containerLayout.addWidget(self.scroll)
    # print(self.model.plugin_type)
    # currentTab = self.getTabByType(self.model.plugin_type)
    # currentTab.setLayout(containerLayout)
    self.show()

# create the app
App = QApplication(sys.argv)

# create Window
t = tabs()
t.show()

# start
sys.exit(App.exec())
