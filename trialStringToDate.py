from datetime import datetime
dateTimeStr = '2020-09-07T08:30:00'
dateTime = datetime.strptime(dateTimeStr, '%Y-%m-%dT%H:%M:%S')
print(dateTime)