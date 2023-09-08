import pyflashGUI as pf
import argparse

if __name__ == '__main__':
    # initiate parser
    parser = argparse.ArgumentParser(description='open flash card GUI')
    parser.add_argument('data',help='Folderpath of your text file where your word list are kept.')
    args = parser.parse_args()   
    # main
    pf.buildGUI(data=args.data)
