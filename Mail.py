import win32com.client
import win32com.client as win32
import sys
from LogFile import LogFile


def automaticmail(Subject,TO,CC,EmailBody):
    try:
        ol=win32com.client.Dispatch("outlook.application")
        olmailitem=0x0 #size of the new email
        newmail=ol.CreateItem(olmailitem)
        newmail.Subject= Subject
        newmail.To=TO
        newmail.CC=CC
        newmail.Body= EmailBody


        # attach='C:\\Users\\admin\\Desktop\\Python\\Sample.xlsx'
        # newmail.Attachments.Add(attach)

        # To display the mail before sending it
        # newmail.Display()

        newmail.Send()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('automaticmail - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("automaticmail function Error is: ", e)


def automaticmail_report(Subject, TO, df):
    try:
        outlook = win32.Dispatch('Outlook.Application')  # Capitalize here
        mail = outlook.CreateItem(0)
        mail.To = TO
        mail.Subject = Subject

        html_table = df.to_html(index=False)
        body = f"""
        <p>Hi Team,</p>
        <p>Please find the below report for {Subject}.</p>
        {html_table}
        <p>Regards,<br>Your Automation</p>
        """

        mail.HTMLBody = body
        mail.Send()
        print("Email sent successfully.")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("automaticmail_report function Error:", str(e))