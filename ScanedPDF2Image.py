from pdf2jpg import pdf2jpg
from datetime import datetime
import os, sys
from LogFile import LogFile
from Mail import automaticmail
import Config

def Scaned_PDF_to_Image_Single_file (Path): # working function for single files
    try:
        today = datetime.now()
        datestring = today.strftime("%Y%m%d")  # Date to the desired string format
        #folder creation
        if not os.path.exists(datestring):
            os.mkdir(datestring)
        if not os.path.exists(datestring+"//PDFToIMage"):
            os.mkdir(datestring+"//PDFToIMage")

        #PDF to Image conversion
        inp = Path
        out = datestring+"\\PDFToIMage"
        result = pdf2jpg.convert_pdf2jpg(inp,out, pages="ALL")
        #pdf2image.convert_from_path()


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('Scaned_PDF_to_Image_Single_file - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error, 'Scaned_PDF_to_Image_Single_file - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("Scaned_PDF_to_Image_Single_file function Error is : ", str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))