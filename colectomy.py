import sys, json, shutil
from pathlib import Path

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.setFixedHeight(300)
        self.setFixedWidth(500)

        ###### some shit relates to QMainWindow I can't solve
        # self.mainWidget = QWidget()
        # self.setCentralWidget(self.mainWidget) 
        # self.mainWidget.setLayout(l_main)

        l_main = QVBoxLayout(self)

        #_# add BROWSER LAYOUT to MAIN LAYOUT
        l_browser = QHBoxLayout(self)
        l_main.addLayout(l_browser)

        #_#_# create widgets for BROWSER LAYOUT
        self.w_browser_label = QLabel('Path:', self)
        self.w_browser_address = QLineEdit(self)
        self.w_browser_button = QPushButton('Browse', self)

        #_#_# put widgets to BROWSER LAYOUT
        l_browser.addWidget(self.w_browser_label)
        l_browser.addWidget(self.w_browser_address)
        l_browser.addWidget(self.w_browser_button)

        #_#_# signal for BROWSER BUTTON
        self.w_browser_button.clicked.connect(self.browse_path)

        #_# ANNOUNCER
        #_#_# Anounncer Line
        w_Announcer_HLine1 = QFrame()
        w_Announcer_HLine1.setLineWidth(1)
        w_Announcer_HLine1.setFrameStyle(2)
        w_Announcer_HLine1.setFrameShape(QFrame.HLine)

        w_Announcer_HLine2 = QFrame()
        w_Announcer_HLine2.setLineWidth(1)
        w_Announcer_HLine2.setFrameStyle(2)
        w_Announcer_HLine2.setFrameShape(QFrame.HLine)

        l_main.addWidget(w_Announcer_HLine1)

        #_#_# Announcer Label
        self.w_announcer_label = QLabel('Welcome to Colectomy!', self)
        self.w_announcer_label.setAlignment(Qt.AlignCenter)
        l_main.addWidget(self.w_announcer_label)

        l_main.addWidget(w_Announcer_HLine2)

        #_# add RUN LAYOUT to MAIN LAYOUT
        l_run = QHBoxLayout(self)
        l_main.addLayout(l_run)
        
        #_#_# add HBox to RUN LAYOUT
        l_run_HBOX = QHBoxLayout(self)
        l_run.addLayout(l_run_HBOX)

        #_#_# ITEM LIST LAYOUT #_#_#
        l_run_item_VBOX = QVBoxLayout(self)
        l_run_HBOX.addLayout(l_run_item_VBOX)

        l_run_item_VBOX_AddItem = QHBoxLayout(self)
        l_run_item_VBOX.addLayout(l_run_item_VBOX_AddItem)

        l_run_item_VBOX_HBOX = QHBoxLayout(self)
        l_run_item_VBOX.addLayout(l_run_item_VBOX_HBOX)

        #_#_#_# Add Item - Name Input
        self.w_run_item_AddItem_Label = QLabel('Suffix name:', self)
        self.w_run_item_AddItem_Input = QLineEdit(self)

        l_run_item_VBOX_AddItem.addWidget(self.w_run_item_AddItem_Label)
        l_run_item_VBOX_AddItem.addWidget(self.w_run_item_AddItem_Input)

        #_#_#_# Item List
        self.w_run_item_List = QListWidget(self)
        l_run_item_VBOX_HBOX.addWidget(self.w_run_item_List)

        #_#_#_# Item List Button
        l_run_item_VBOX_HBOX_ButtonLayout = QVBoxLayout(self)
        l_run_item_VBOX_HBOX.addLayout(l_run_item_VBOX_HBOX_ButtonLayout)

        self.w_run_item_button_ADD = QPushButton('ADD', self)
        self.w_run_item_button_REMOVE = QPushButton('REMOVE', self)

        l_run_item_VBOX_HBOX_ButtonLayout.addWidget(self.w_run_item_button_ADD)
        l_run_item_VBOX_HBOX_ButtonLayout.addWidget(self.w_run_item_button_REMOVE)

        #_#_#_# Item List Button - Signal
        self.w_run_item_button_ADD.clicked.connect(self.add_button_clicked)
        self.w_run_item_button_REMOVE.clicked.connect(self.remove_button_clicked)

        #_#_# Separate Line
        w_run_VLine = QFrame()
        w_run_VLine.setLineWidth(1)
        w_run_VLine.setFrameStyle(2)
        w_run_VLine.setFrameShape(QFrame.VLine)

        l_run_HBOX.addWidget(w_run_VLine)

        #_#_# BACK UP and RUN Layout #_#_#
        l_run_BAKRunLayout = QVBoxLayout(self)
        l_run_HBOX.addLayout(l_run_BAKRunLayout)

        self.w_run_BAKChecker = QCheckBox('Back up', self)
        self.w_run_runButton = QPushButton('RUN', self)
        self.w_run_revertButton = QPushButton('REVERT', self)

        self.w_run_revertButton.setEnabled(False)

        self.w_run_BAKChecker.setCheckState(Qt.Checked)

        l_run_BAKRunLayout.addWidget(self.w_run_BAKChecker)
        l_run_BAKRunLayout.addWidget(self.w_run_runButton)
        l_run_BAKRunLayout.addWidget(self.w_run_revertButton)

        self.w_run_runButton.clicked.connect(self.run_button_clicked)
        self.w_run_revertButton.clicked.connect(self.revert_button_clicked)

        #### END OF UI #####

        # AT START OF RUN
        self.load_suffix_list()
        self.fileDict = {}

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Choose path...")
        self.w_browser_address.setText(path)

    def path_JSON(self,file="suffix_list.json"):
        script_dir = Path(".")
        json_dir = script_dir / file
        return json_dir

    def load_JSON(self, path):
        file = open(self.path_JSON())
        data = json.load(file)
        data = data.get("texture_type")
        return data

    def load_suffix_list(self):
        for item in self.load_JSON(self.path_JSON()):
            self.add_item_to_suffix_list(item)
        self.w_announcer_label.setText('Texture type list has been loaded successfully!')

    def read_suffix_list(self):
        inAppList = []
        for i in range(self.w_run_item_List.count()):
            itemToText = self.w_run_item_List.item(i)
            inAppList.append(itemToText.text())
        return inAppList        

    def save_suffix_list(self):
        saveDict = {"texture_type":[]}
        inAppList = self.read_suffix_list()
        saveDict["texture_type"].extend(inAppList)
        with open(self.path_JSON(), 'w') as toSaveFile:
            json.dump(saveDict, toSaveFile)

    def check_existed_suffix(self, itemToCheck):
        checkList = self.w_run_item_List.findItems(itemToCheck, Qt.MatchFixedString)
        if not len(checkList)==0:
            return True
            
    def add_item_to_suffix_list(self, itemToAdd):
        if not self.check_existed_suffix(itemToAdd):
            self.w_run_item_List.addItem(itemToAdd)
            self.w_announcer_label.setText('Suffix has added successfully!')
        else:
            self.w_announcer_label.setText('!!! Suffix already exists in list !!!')

    def remove_suffix_from_list(self, itemToRemove):
        self.w_run_item_List.takeItem(itemToRemove)
        self.w_announcer_label.setText('Suffix has been deleted!')

    def add_button_clicked(self):
        textInInput = self.w_run_item_AddItem_Input.text()
        self.add_item_to_suffix_list(textInInput)
        self.save_suffix_list()

    def remove_button_clicked(self):
        currentRow = self.w_run_item_List.currentRow()
        self.remove_suffix_from_list(currentRow)
        self.save_suffix_list()

    def get_address(self):
        path = Path(self.w_browser_address.text())
        if path.is_dir():
            return path
        else:
            return False

    def list_all_file(self, folderPath):
        fileList = folderPath.glob("*.tga")
        return fileList

    def put_file_to_key(self, fileList):
        fileDict = {}
        for file in fileList:
            fileDict[file] = None
        return fileDict

    def clear_junk_in_name(self, string):
        splitedString = str(string).split("_")
        suffixList = self.read_suffix_list()
        for suffix in suffixList:
            if splitedString[-1]==suffix:
                if self.safe_lock(splitedString[-2]):
                    splitedString.pop(-2)
                    continue
        separator = "_"        
        newString = separator.join(splitedString)
        return newString
 
    def read_suffix_list(self):
        suffixList = []
        for i in range(self.w_run_item_List.count()):
            itemToText = self.w_run_item_List.item(i)
            suffixList.append(itemToText.text())
        return suffixList

    def safe_lock(self, string):
        if len(string)>12:
            return True

    def put_cleared_name_in_value(self, fileDict):
        for k, v in fileDict.items():
            v = self.clear_junk_in_name(k)
            fileDict[k] = v

    def check_value_duplicated(self, fileDict):
        if len(fileDict.values())==len(set(fileDict.values())):
            return False
        else:
            return True
    
    def apply_dict_to_new_name(self, fileDict, folderPath, revert = False):
        self.w_announcer_label.setText('Renaming file... Please wait')
        if revert==False:
            for k, v in fileDict.items():
                oldname = folderPath / k
                oldname.rename(v)
        else:
            for k, v in fileDict.items():
                oldname = folderPath / v
                oldname.rename(k)
            
    def backup_file(self, fileDict, folderPath):
        bakFolder = folderPath / "BAK"
        bakFolder.mkdir(exist_ok = True)
        for file in fileDict.keys():
            sourcePath = folderPath / file
            shutil.copy(sourcePath, bakFolder)

    def run_button_clicked(self):
        #check if browser address is empty
        if self.w_browser_address.text()=="":
            self.w_announcer_label.setText('!!! Please enter location !!!')
        else:
            folderPath = self.get_address()
            if folderPath==False:
                self.w_announcer_label.setText('!!! Location does not exist !!!')
            else:    
                fileList = self.list_all_file(folderPath)
                self.fileDict = self.put_file_to_key(fileList)
                self.put_cleared_name_in_value(self.fileDict)
                if self.check_value_duplicated(self.fileDict)==False:
                    if not self.w_run_BAKChecker.checkState()==0:
                        self.w_announcer_label.setText('Backing up file - Please wait')
                        self.backup_file(self.fileDict, folderPath)
                    self.apply_dict_to_new_name(self.fileDict, folderPath)
                    self.w_announcer_label.setText('Renaming file is successful!')
                    self.w_run_revertButton.setEnabled(True)
                else:
                    self.w_announcer_label.setText('!!! There will be duplicate filename after renaming. Please re-check your files !!!')
    
    def revert_button_clicked(self,fileDict):
        folderPath = self.get_address()
        self.apply_dict_to_new_name(self.fileDict, folderPath, True)
        self.w_announcer_label.setText('Reverting old filename is successful!')
        self.w_run_revertButton.setEnabled(False)

#BEEP BOOP BEEP BOOP        
app = QApplication()
app.setApplicationDisplayName("Colectomy v1.1")
w = main_window()
w.show()
app.exec_()