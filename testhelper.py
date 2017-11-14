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