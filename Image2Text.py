from datetime import datetime
import os, sys
from PIL import Image
import pytesseract
from LogFile import LogFile
from Mail import automaticmail
import Config

def Image_to_Text_single_folder(FolderName): # working function for Single folders
    try:
        today = datetime.now()
        datestring = today.strftime("%Y%m%d")
        if os.path.isdir(datestring):
            #print(datestring + "//" + FolderName)
            # Image to Text conversion
            indir = datestring + "//" + "PDFToIMage" + "//" + FolderName
            filecount = (len([name for name in os.listdir(indir) if os.path.isfile(os.path.join(indir, name))]))
            text = []

            for i in range(filecount):
                FolderName_New = FolderName.replace("_dir","")
                #print(indir + "//" + str(i) + "_" + FolderName_New + ".jpg")
                inputfilenme_new = indir + "//" + str(i) + "_" + FolderName_New + ".jpg"
                im = Image.open(inputfilenme_new)
                pytesseract.pytesseract.tesseract_cmd = r'C:\Users\O786423\AppData\Local\Microsoft\AppV\Client\Integration\CFA6629B-C732-49ED-AA3D-B83A9567CD0D\Root\VFS\ProgramFilesX86\Tesseract-OCR\tesseract.exe'
                text.append(pytesseract.image_to_string(im, lang='eng'))
                #print(text)
            return (text)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('Image_to_Text_single_folder - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error, 'Image_to_Text_single_folder - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("Image_to_Text_single_folder function Error is: " , str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))


def Image_to_Text_single_file(FileName): # working function for Single folders
    try:
        text1 = []
        im = Image.open(FileName)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text1.append(pytesseract.image_to_string(im, lang='eng'))
        #print(text)
        return (text1)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('Image_to_Text_single_folder - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error, 'Image_to_Text_single_folder - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("Image_to_Text_single_folder function Error is: " , str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))