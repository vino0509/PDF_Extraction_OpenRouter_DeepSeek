import tkinter as tk
import easygui
import sys, os, re, json, xlsxwriter
from datetime import datetime
from PyPDF2 import PdfReader
import pandas as pd
from pathlib import Path
from LogFile import LogFile
from Mail import automaticmail, automaticmail_report
from ScanedPDF2Image import Scaned_PDF_to_Image_Single_file
from Image2Text import Image_to_Text_single_folder
from Image2Text import Image_to_Text_single_file
import Config
from GenAI import genai

format = {"Bank Name": ["No Match", "Invoice"], "Count": [0, 0]}
df_DailyReport = pd.DataFrame(format)



def runfunction():
    try:

        easygui.msgbox("Stat", title= "Test")
        inp = Inputpath.get(1.0, "end-1c")
        out = Outputpath.get(1.0, "end-1c")
        inp = str(inp)
        print(inp)
        print(out)
        OCR_Editable_Scaned(inp, out)
        print("completed")
        easygui.msgbox("Completed", title= "Test")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('runfunction - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error, 'runfunction - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("runfunction function Error is: " , str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))



def OCR_Editable_Scaned(inputPath, outputpath):
    try:
        Invoice_Sucess_Count = 0
        today = datetime.now()
        datestring = today.strftime("%Y%m%d")
        for filename in os.listdir(inputPath):
            if filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.png'):
                #with open(inputPath + "//" + filename, "r") as f:
                print("filename: " + filename)
                LogFile("filename: " + filename + " Start")
                filenamewithoutextension = filename.split(".")[0]

                if filename.endswith('.pdf'):
                    #try  2
                    reader = PdfReader(inputPath + "//" + filename)
                    #print(len(reader.pages))

                    output = []

                    for i in range(len(reader.pages)):
                        page = reader.pages[i]
                        #output += page.extractText()
                        output += page.extract_text()

                    #easygui.msgbox(output[1], title= "Test")

                    #Scaned pdf to textS
                    if len(output) == 0:
                        LogFile("filename: " + filename + " Scanned PDF")
                        Scaned_PDF_to_Image_Single_file(inputPath + "\\" + filename)
                        #for normal
                        output = Image_to_Text_single_folder(filename + "_dir")

                if filename.endswith('.jpg') or filename.endswith('.png'):
                    output = Image_to_Text_single_file(inputPath + "//" + filename)


                if len(output) != 0:
                    Result = ''.join(output)
                    #print(Result)
                    genai_op = genai(Result, filename)
                    #print("answer")`
                    print(genai_op)

                    cleaned_response = re.sub(r"^```json|```$", "", genai_op.strip(), flags=re.IGNORECASE).strip()

                    data = json.loads(cleaned_response)
                    Billed_To = data.get("Billed To") or data.get("BilledTo")
                    #Billed_To = data["Billed To"]
                    Date_of_Issue = data["Date of Issue"]
                    Invoice_Number = data["Invoice Number"]
                    Amount_Due = data["Amount Due"]
                    Due_Date = data["Due Date"]

                    df = pd.DataFrame({
                        'FileName': [filename],
                        'BilledNo': [Billed_To],
                        'Date of Issue': [Date_of_Issue],
                        'Invoice Number' : [Invoice_Number],
                        'Amount Due' : [Amount_Due],
                        'Due Date' : [Due_Date]
                    })
                    print(df)

                    outputfile1 = outputpath
                    #df.to_excel(outputfile1)

                    #print("test output file name 1 "+outputfile1)

                    if not os.path.isfile(outputfile1):
                        workbook = xlsxwriter.Workbook(outputfile1)
                        worksheet = workbook.add_worksheet()
                        worksheet.write('A1', 'FileName')
                        worksheet.write('B1', 'BilledTo')
                        worksheet.write('C1', 'DateOfIssue')
                        worksheet.write('D1', 'InvoiceNumber')
                        worksheet.write('E1', 'AmountDue')
                        worksheet.write('F1', 'DueDate')
                        workbook.close()


                    with pd.ExcelWriter(outputfile1,mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                        df.to_excel(writer, sheet_name="Sheet1",header=None, startrow=writer.sheets["Sheet1"].max_row,index=False)


                    #return (len(df.index))


                src_file = Path(inputPath + "\\" + filename)
                dst_file = Path(inputPath+"//Completed//"+filename)

                if not os.path.exists(inputPath+"//Completed"):
                    os.mkdir(inputPath+"//Completed")
                if not os.path.exists(inputPath+"//Completed//"+filename):
                    src_file.rename(dst_file)
                    print(filename +" - Moved to completed folder")

                    #Extraction_sucess_Count = New_Invoice (Output_filename_full, outputpath)
                    LogFile(filename + " - Extraction Completed")
                    print(filename + " - Extraction Completed")

                #adding File name and Success count for mail-repot
                Invoice_Sucess_Count += 1
                df_DailyReport.at[1,'Count']= Invoice_Sucess_Count

        automaticmail_report(Config.EmailSuject_DailyRepot, Config.EmailTo_DailyRepot, df_DailyReport)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("OCR_Editable_Scaned function the Error is :" , str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        LogFile('OCR_Editable_Scaned - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error + 'OCR_Editable_Scaned - function error -  ', str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("OCR_Editable_Scaned function the Error is :" , str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))





# manual Check
# inputpath = "C\Users\vinos\Desktop\Python\Input"


#interface
# Create a Tkinter window
window = tk.Tk()

# Set the window title
window.title('OCR Tool')

# Set the window size
window.geometry('800x400')

# Create a label for inputfile
label = tk.Label(window, text='Input Path')
label.pack()

# Define the input dialog
Inputpath = tk.Text(window, height=1,width=25)
Inputpath.pack()

# Create a label for outputfile
label = tk.Label(window, text='Output Path')
label.pack()

Outputpath = tk.Text(window, height=1,width=25)
Outputpath.pack()

# Create a button
button = tk.Button(window, text='Run', command= runfunction)
button.pack()

# Start the main event loop
window.mainloop()




