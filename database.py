import os
class database(object):
    def __init__(self,data=None) -> None:
        super().__init__()
        self.cardlist = []    # All cards
        self.selected_cards = [] # sorted cards for test
        self.temp_cards = []
        self.flashindexes = [] # Shuffled indexess for FLASHMODE
        self.quizindexes = [] # Shuffled indexess for QUIZMODE
        self.flashIndex = 0 # Current index of FLASHMODE
        self.quizIndex = 0 # Current index of QUIZMODE
        self.databasePath = data # File path of the cards info
        self.check_count = 0
        # self.read_scores(self.databasePath[0:-4]+'_score.txt')
        self.init_scores(self.databasePath)
        # self.scorePath = self.databasePath[0:-4]+'_score.txt'
        # if os.path.isfile(self.scorePath):
        #     pass
        # else:
        #     with open(self.scorePath, 'w') as fp:
        #         pass
        
        self.newline = '__n__'
        self.FLAG_FLASH = False # for the first time
        self.FLAG_QUIZ = False # for the first time
    
    def read_scores(self,path):
        lines = []
        with open(path, 'r') as f_in:
            for line in f_in:
                text_data = line.split('\t')[:-1]
                lines.append(text_data)
                # print(text_data)
        
    def init_scores(self,path):
        output_file = path[0:-4]+'_score.txt'
        with open(path, 'r') as f_in, open(output_file, 'w') as f_out:
            # Read each line from the input file
            for line in f_in:
                # Remove any trailing whitespace from the line
                line = line.rstrip()
                if len(line.split('\t')) <= 2 and len(line.split('\t')[0]) > 0:
                    # print(line)
                    # Append a tab space and '[0,0]' to the line
                    modified_line = line + '\t[0,0]'
                    # Write the modified line to the output file
                    f_out.write(modified_line + '\n')
                
    def init_isCardSelectedlist(self,len_cards:int) -> None:
        self.isCardSelectedlist = [False for val in range(len_cards)]
        
        
        