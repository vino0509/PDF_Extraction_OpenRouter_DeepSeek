import requests
import os
import json
import sys
from LogFile import LogFile
import Config
from Mail import automaticmail

from dotenv import load_dotenv
load_dotenv()


def genai(prompt, filename_new):
    try:
        # Get API key from environment
        api_key = os.getenv("OPENROUTER_API_KEY")
        prompt = "Extract only the following fields from the invoice: Billed To, Date of Issue, Invoice Number, Amount Due, and Due Date. Return the result strictly in JSON format with no explanation or symbols."

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://example.com",
                "X-Title": "My Chat App"
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "user",
                        #"content": "What is the meaning of life?"
                        #"content": prompt + "please print only Billed To, Date of Issue, Invoice Number, Amount Due and Due Date with " + "'" + filename_new + "'" +" with this file name in json format without * sybmbol"
                        "content": prompt + "Extract only the following fields from the invoice: Billed To, Date of Issue, Invoice Number, Amount Due, and Due Date. Return the result strictly in JSON format with no explanation or symbols."
                    }

                ]
            })
        )

        # Extract and print only the AI's answer
        result = response.json()
        answer = result['choices'][0]['message']['content']
        #print(answer)
        return answer
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        LogFile('genai - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        automaticmail(Config.EmailSuject_Error,Config.EmailTo_Error, Config.EmailCC_Error, 'genai - function error -  ' + str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))
        print("genai function Error is : ", str(exc_tb.tb_lineno) +" - " + str(exc_type) + " - " +str(e))