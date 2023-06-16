import sys
from PyQt6 import QtGui as Qg, QtWidgets as Qw   
from PyQt6.QtCore import QTextStream, QFile, Qt
import matplotlib
matplotlib.use("Qt5Agg")
import os
import pandas as pd
import numpy as np
import ui_test as ui
import flashcards as fc
import database as db

class Fcviewer(Qw.QMainWindow):
    def __init__(self, parent=None, data=None) -> None:
        super().__init__(parent)
        
        self.database = db.database(data=data)
        self.initUI(data) # initialise UI
        
        #  import assigned words
        if os.path.isfile(self.database.databasePath):
            self.read_words(self.database.databasePath)
        # initialise boolean list 
        self.database.init_isCardSelectedlist(len(self.database.cardlist))
        self.database.default_color = self.ui.label_answer_flash.palette().color(Qg.QPalette.ColorRole.WindowText)
        
    def initUI(self,data):
        # UI setup
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Text edit setting (Add tab)
        self.ui.textEdit_word.setTabChangesFocus(True)
        self.ui.textEdit_desc.setTabChangesFocus(True)
        self.setTabOrder(self.ui.textEdit_word,self.ui.textEdit_desc)
        # Labels and text area setting (Flash tav)
        self.ui.label_test_flash.setWordWrap(True)
        self.ui.label_answer_flash.setWordWrap(True)
        self.ui.label_other.setText('0')
        # Label setting (Quiz tab)
        self.ui.label_test_quiz.setWordWrap(True)
        self.ui.label_A.setWordWrap(True)
        self.ui.label_B.setWordWrap(True)
        self.ui.label_C.setWordWrap(True)
        self.ui.label_D.setWordWrap(True)
        self.choicelist = [
            self.ui.label_A,
            self.ui.label_B,
            self.ui.label_C,
            self.ui.label_D
            ]
        
        self.adjust_fontsize_choicelist()
        
        
        # radio buttons (choices, Quiz tab)
        self.radios = Qw.QButtonGroup()
        self.radios.addButton(self.ui.radioButton_choiceA,0)
        self.radios.addButton(self.ui.radioButton_choiceB,1)
        self.radios.addButton(self.ui.radioButton_choiceC,2)
        self.radios.addButton(self.ui.radioButton_choiceD,3)

        # action listner
        self.ui.pushButton_createNewSet.clicked.connect(self.create_new_text_file) # add tab
        # self.ui.pushButton_selectPath.clicked.connect()
        self.ui.pushButton_add.clicked.connect(self.button_add_clicked)  # add card (Add tab)
        
        self.ui.pushButton_setall_set.clicked.connect(self.button_setall_clicked) # set tab
        self.ui.pushButton_set_set.clicked.connect(self.button_set_clicked) # set tab
        self.ui.pushButton_remove_set.clicked.connect(self.button_remove_clicked) # set tab
        
        self.ui.pushButton_next_flash.clicked.connect(self.button_next_flash_clicked)  # flash tab
        self.ui.pushButton_restart_flash.clicked.connect(self.button_restart_flash_clicked) # flash tab
        self.ui.pushButton_mark.clicked.connect(self.button_mark_clicked)
        self.ui.pushButton_check.clicked.connect(self.button_check_flash_clicked) # flash tab
        self.ui.comboBox_modeFlash.currentIndexChanged.connect(self.mode_changed_flash) # flash tab
        
        self.ui.pushButton_submitQuiz.clicked.connect(self.button_next_quiz_clicked) # quiz tab
        self.ui.tabWidget.currentChanged.connect(self.tab_changed) # quiz tab
        self.ui.comboBox_modeQuiz.currentIndexChanged.connect(self.mode_changed_quiz) # quiz tab
        
        
        # TableView
        self.wordListModel_overview = Qg.QStandardItemModel(0,2)
        self.wordListModel_overview.setHeaderData(0, Qt.Orientation.Horizontal, 'Word')
        self.wordListModel_overview.setHeaderData(1, Qt.Orientation.Horizontal, 'Description')
        self.wordlistModel_sortall = Qg.QStandardItemModel(0,1)
        self.wordlistModel_sorted = Qg.QStandardItemModel(0,1)
        
            
    def create_new_text_file(self):
        # Open a file dialog to select the file path and name
        file_path, _ = Qw.QFileDialog.getSaveFileName(self, "Create New Text File", "", "Text Files (*.txt)")
        
        if file_path:
            if '.txt' in file_path:
                pass
            else:
                file_path = file_path + '.txt'
            # Create a QFile object
            file = QFile(file_path)

            # Open the file in write-only mode
            if file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Truncate):
                # Create a QTextStream object to write to the file
                out_stream = QTextStream(file)
                # Write some text to the file
                out_stream << ""
                # Close the file
                file.close()
                
                self.read_words(file_path)
                self.database.databasePath = file_path
        
        
    def read_words(self,path):
        """import words and descriptions from txt file.

        Args:
            path (_type_): file path.
        """
        text = open(path,'r')
        Lines = text.readlines()
        model = self.ui.tableView_words_overview.model()
        if model is not None:
            model.removeRows(0,model.rowCount())
            self.database.cardlist = []
        
        # assign number to each card
        ID_CARD = 0 # start from 0
        
        for line in Lines:
            if len(line) >= 1 and '\t' in line:
                card = fc.card() # initialise card object
                word = line.split('\t')[0] # '\t' devides the word and the description
                desc = line.split('\t')[1].replace(self.database.newline,'\n') # when description consists of multiple lines
                card.set(word,desc=desc,id=ID_CARD) # assign info
                self.database.cardlist.append(card) # store 
                self.addcard2table_overview(card) # display card in the tableview
                ID_CARD += 1

            
    def addcard2table_overview(self,card):
        item1 = Qg.QStandardItem(card.word)
        item2 = Qg.QStandardItem(card.desc)
        item_sortall =  Qg.QStandardItem(card.word)
        self.wordListModel_overview.appendRow([item1,item2])
        # table setting
        self.ui.tableView_words_overview.setModel(self.wordListModel_overview)
        header = self.ui.tableView_words_overview.horizontalHeader()
        header.setStretchLastSection(True)
        
        self.wordlistModel_sortall.appendRow([item_sortall])
        self.ui.tableView_sortwords_all.setModel(self.wordlistModel_sortall)
        header = self.ui.tableView_sortwords_all.horizontalHeader()
        header.setStretchLastSection(True)
    
    def addcard2table_sorted(self,card):
        item1 = Qg.QStandardItem(card.word)
        self.wordlistModel_sorted.appendRow([item1])
        # table setting
        self.ui.tableView_sortedwords.setModel(self.wordlistModel_sorted)
        header = self.ui.tableView_sortedwords.horizontalHeader()
        header.setStretchLastSection(True)
        
    def button_add_clicked(self):
        word = self.ui.textEdit_word.toPlainText()
        desc = self.ui.textEdit_desc.toPlainText().replace('\n',self.database.newline)
        if len(word) > 1 and len(desc) > 2:
            card = fc.card()
            card.set(word,desc=desc)
            self.database.cardlist.append(card)
            self.addcard2table_overview(card)
            fc.save_cards(self.database.cardlist,self.database.databasePath)
    
    def button_setall_clicked(self):
        pass

    
    def button_remove_clicked(self):
        indexes_selected = self.ui.tableView_sortedwords.selectionModel().selectedIndexes()
        items = [self.ui.tableView_sortedwords.model().data(index) for index in indexes_selected]
        # Unselected_cards = fc.getCardsFromWords(items,self.cardlist)
        self.database.isCardSelectedlist = fc.setFalseforUnselectedCards(items,self.database.cardlist,self.database.isCardSelectedlist)
        self.database.selected_cards = fc.getCardsFromBooleans(self.database.cardlist,self.database.isCardSelectedlist)
        self.update_tableview_sorted()
    
    def button_set_clicked(self):
        
        # extract indexes of the selected rows of table view
        indexes_selected = self.ui.tableView_sortwords_all.selectionModel().selectedIndexes()
        
        # get a list of words (str) from tableview model
        items = [self.ui.tableView_sortwords_all.model().data(index) for index in indexes_selected]
        
        # set a boolean list from the word list
        self.database.isCardSelectedlist = fc.get_CardSelectedIndexesFromWords(items,self.database.cardlist,self.database.isCardSelectedlist)
        
        # set a list of card objects
        self.database.selected_cards = fc.getCardsFromBooleans(self.database.cardlist,self.database.isCardSelectedlist)
        
        # update table view items
        self.update_tableview_sorted()
            
    def update_tableview_sorted(self):
        selected_cards = []
        self.wordlistModel_sorted.removeRows(0,self.wordlistModel_sorted.rowCount())
        for i,isSelected in enumerate(self.database.isCardSelectedlist):
            if isSelected:
                self.addcard2table_sorted(self.database.cardlist[i])
        self.ui.tableView_sortedwords.update()
            
    def button_mark_clicked(self):
        pass
        
    def button_next_flash_clicked(self): 
        # flash
        WORDFIRST = 0
        DESCFIRST = 1 # magic numbers for order of flash
        # first time 
        if self.database.FLAG_FLASH == False:
            self.database.flashindexes = np.arange(len(self.database.selected_cards))
            np.random.shuffle(self.database.flashindexes)
            self.database.FLAG_FLASH = True
        
        ind = int(np.floor(self.database.flashIndex)) % len(self.database.selected_cards) # current index
        acard = self.database.selected_cards[self.database.flashindexes[ind]] # card to display
        self.database.ID_CARD_FLASH = acard.id # set current ID

        # text label
        self.ui.label_index_flash.setText(str(ind+1)+'/'+str(len(self.database.selected_cards))) # display order
        
        MODE = self.ui.comboBox_modeFlash.currentIndex()
        if MODE == WORDFIRST:
            if int(self.database.flashIndex*2) % 2 == 0: # show 
                self.ui.label_test_flash.setText(acard.word)
                self.ui.label_answer_flash.clear()
                self.database.flashIndex += 0.5
            else:
                self.ui.label_answer_flash.setText(acard.desc)
                self.database.flashIndex += 0.5
        elif MODE == DESCFIRST:
            if int(self.database.flashIndex*2) % 2 == 0: # show 
                self.ui.label_test_flash.setText(acard.desc)
                self.ui.label_answer_flash.clear()
                self.database.flashIndex += 0.5
            else:
                self.ui.label_answer_flash.setText(acard.word)
                self.database.flashIndex += 0.5
    
    def button_check_flash_clicked(self):
        if self.database.ID_CARD_FLASH >= 0:
            index = int(self.database.ID_CARD_FLASH)
            # set a boolean list from the word list
            Selected_sum = np.sum(self.database.isCardSelectedlist)
            self.database.isCardSelectedlist = fc.get_CardSelectedIndexesFromWords([self.database.cardlist[index].word],self.database.cardlist,self.database.isCardSelectedlist)
            if Selected_sum != np.sum(self.database.isCardSelectedlist):
                self.database.check_count += 1
                self.ui.label_other.setText(str(self.database.check_count))
            
            
    def button_uncheck_flash_clicked(self):
        pass
    
    def button_restart_flash_clicked(self):
        self.database.flashindexes = np.arange(len(self.database.selected_cards)) 
        np.random.shuffle(self.database.flashindexes)
        
    def button_next_quiz_clicked(self):
        
        # flash
        WORDFIRST = 0
        DESCFIRST = 1 # magic numbers for order of flash
        
        # first time 
        if self.database.FLAG_QUIZ == False:
            self.database.quizindexes = np.arange(len(self.database.selected_cards)) 
            np.random.shuffle(self.database.quizindexes)
            self.database.FLAG_QUIZ = True
        
        # select card
        ind = int(np.floor(self.database.quizIndex)) % len(self.database.selected_cards) # current index
        acard = self.database.selected_cards[self.database.quizindexes[ind]] # card to display
        
        # set text
        self.ui.label_index_quiz.setText(str(ind+1)+'/'+str(len(self.database.selected_cards))) # display order
        MODE = self.ui.comboBox_modeQuiz.currentIndex()
        if MODE == WORDFIRST:
            if int(self.database.quizIndex*2) % 2 == 0: # show quiz
                for label in self.choicelist:
                    label.setStyleSheet("color: {};".format(self.database.default_color.name()))
                    # label.setStyleSheet("QLabel { color : black; }")
                self.ui.label_test_quiz.setText(acard.word) # main text
                # prepare choices
                wrong_choices_indexes = self.prepare_Index_of_wrong_choices(len(self.database.selected_cards),self.database.quizindexes[ind])
                answers = [self.database.selected_cards[i].desc for i in wrong_choices_indexes]
                answers.append(acard.desc)
                np.random.shuffle(answers)
                self.set_choices_quiz(answers)
                # etc
                self.database.quizIndex += 0.5
            else: # check answer
                if self.choicelist[self.radios.checkedId()].text() == acard.desc:
                    self.choicelist[self.radios.checkedId()].setStyleSheet("QLabel { color : lightgreen; }")
                else:
                    self.choicelist[self.radios.checkedId()].setStyleSheet("QLabel { color : red; }")
                    
                self.database.quizIndex += 0.5

        elif MODE == DESCFIRST:
            if int(self.database.quizIndex*2) % 2 == 0: # show quiz
                for label in self.choicelist:
                    label.setStyleSheet("color: {};".format(self.database.default_color.name()))
                    # label.setStyleSheet("QLabel { color : black; }")
                self.ui.label_test_quiz.setText(acard.desc) # main text
                # prepare choices
                wrong_choices_indexes = self.prepare_Index_of_wrong_choices(len(self.database.selected_cards),self.database.quizindexes[ind])
                answers = [self.database.selected_cards[i].word for i in wrong_choices_indexes]
                answers.append(acard.word)
                np.random.shuffle(answers)
                self.set_choices_quiz(answers)
                # etc
                self.database.quizIndex += 0.5
            else: # check answer
                if self.choicelist[self.radios.checkedId()].text() == acard.word:
                    self.choicelist[self.radios.checkedId()].setStyleSheet("QLabel { color : lightgreen; }")
                else:
                    self.choicelist[self.radios.checkedId()].setStyleSheet("QLabel { color : red; }")
                self.database.quizIndex += 0.5
    
    def prepare_Index_of_wrong_choices(self,data_num:int, correct_Index:int):
        available_indexess = np.arange(data_num)
        available_indexess = np.delete(available_indexess,correct_Index)
        np.random.shuffle(available_indexess)
        return available_indexess[0:3]
            
    
    def set_choices_quiz(self,choices:list)->None:
        self.ui.label_A.setText(choices[0])
        self.ui.label_B.setText(choices[1])
        self.ui.label_C.setText(choices[2])
        self.ui.label_D.setText(choices[3])
        self.adjust_fontsize_choicelist()
        
    def mode_changed_flash(self):
        self.reset_progress_flash()
        self.reset_UI_FlashTab()
    
    def mode_changed_quiz(self):
        self.reset_progress_quiz()
        self.reset_UI_QuizTab()
    
    def tab_changed(self,index):
        # set a list of card objects
        self.database.selected_cards = fc.getCardsFromBooleans(self.database.cardlist,self.database.isCardSelectedlist)
        # if none of cards is selected
        if len(self.database.selected_cards) == 0:
            self.database.selected_cards = self.database.cardlist
        # update tableview
        self.update_tableview_sorted()
        
        # reset flashcard progress       
        self.reset_progress_flash()
        self.reset_UI_FlashTab()
        # reset quiz progress
        self.reset_progress_quiz()
        self.reset_UI_QuizTab()
        
    def reset_progress_flash(self):
        self.database.FLAG_FLASH = False
        self.database.flashIndex = 0
        
        
    def reset_progress_quiz(self):
        self.database.FLAG_QUIZ = False
        self.database.quizIndex = 0
        
    def reset_UI_FlashTab(self):
        self.ui.label_test_flash.clear()
        self.ui.label_answer_flash.clear()
        self.ui.label_index_flash.setText(str(self.database.flashIndex+1)+'/'+str(len(self.database.selected_cards)))
    
    def reset_UI_QuizTab(self):
        self.ui.label_test_quiz.clear()
        self.ui.label_index_quiz.setText(str(self.database.quizIndex+1)+'/'+str(len(self.database.selected_cards)))
        for label in self.choicelist:
            label.clear()
    
    def adjust_fontsize_choicelist(self):
        font_sizes = np.ones(4)
        font_list = []
        for i, label in enumerate(self.choicelist):
            label.setWordWrap(False)
            font = label.font()
            font_metrics = Qg.QFontMetrics(font)
            while font_metrics.horizontalAdvance(label.text()) < label.width()/1.5 and font_sizes[i] < 30:
                font_sizes[i] =  font_sizes[i] + 5        
                font.setPointSize(int(font_sizes[i]))
                font_metrics = Qg.QFontMetrics(font)
            font_list.append(font)
        for i,label in enumerate(self.choicelist):
            font = font_list[np.argmin(font_sizes)]
            label.setFont(font)
        self.ui.label_test_quiz.setFont(font_list[np.argmin(font_sizes)])

        
def buildGUI(data = 'None'):
    app = Qw.QApplication(sys.argv)         
    wmain = Fcviewer(data=data)
    wmain.show()
    # if type(data) == pd.core.frame.DataFrame:
    #     wmain.loadData(data)
    # elif isinstance(data,str) and data != 'None':
    #     wmain.loadData(data)
    sys.exit(app.exec())

