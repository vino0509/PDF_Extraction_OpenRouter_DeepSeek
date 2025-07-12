from datetime import datetime
import os


def LogFile(text):
    try:
        today = datetime.now()
        datestring = today.strftime("%Y-%m-%d %H:%M:%S")
        #folder creation
        if not os.path.exists("LogFile"):
            os.mkdir("LogFile")

        #text write in text file
        Log_File_Path = "LogFile//Logfile.txt"

        file = open(Log_File_Path, 'a')
        file.write(datestring + " - " +text + '\n')
        file.close()
    except Exception as e:
        print(str(e))