from datetime import datetime, date, timedelta


def is_live_test(test):
    now = datetime.now()

    if not test.get('schedule'):
        return False

    test_date = test['schedule']['date']
    test_time = test['schedule']['time']
    test_duration = test['schedule']['duration']

    tdatetime = datetime.strptime(test_date+"-"+test_time, "%d-%m-%Y-%H:%M")

    if tdatetime > now:
        return False

    if tdatetime + timedelta(minutes=int(test_duration)+1) < now:
        return False

    return True

def remaining_time(test):

    test_date_time = test['schedule']['date']+"-"+test['schedule']['time']
    test_date_time = datetime.strptime(test_date_time, "%d-%m-%Y-%H:%M")
    now = datetime.now()

    end_test_date_time = test_date_time + timedelta(minutes=int(test['schedule']['duration'] ) + 1)

    if now > end_test_date_time:
        return 0,0,0

    difference = end_test_date_time - now

    days = difference.days
    hours = difference.seconds//3600 - difference.days*24
    minutes = difference.seconds//60 - hours*60

    return days, hours, minutes

def is_completed_test(test):

    days, hours, minutes = remaining_time(test)
    if days == 0 and hours == 0 and minutes == 0:
        return True

    return False