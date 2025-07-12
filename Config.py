from datetime import datetime

today = datetime.now()
datestring = today.strftime("%Y%m%d")

EmailSuject_Error = 'Bot-Error'
# EmailTo_Error = 'vinoshansep@outlook.com'
EmailTo_Error = 'vinothr6@hexaware.com'
EmailCC_Error = ''

EmailSuject_DailyRepot = datestring + ' - Bot-Report'
#EmailTo_DailyRepot = 'vinoshansep@outlook.com'
EmailTo_DailyRepot = 'vinothr6@hexaware.com'
EmailCC_DailyRepot = ''
