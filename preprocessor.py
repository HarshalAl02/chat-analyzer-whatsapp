import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern_am_pm = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*'
        r'(\d{1,2}:\d{2})\s*'
        r'([AaPp][Mm])\s*-\s*'
        , re.MULTILINE
    )

    def convert_match(m):
        date_str, time_str, am_pm = m.groups()
        for fmt in ("%d/%m/%y %I:%M %p", "%d/%m/%Y %I:%M %p"):
            try:
                dt_obj = datetime.strptime(f"{date_str} {time_str} {am_pm.upper()}", fmt)
                return dt_obj.strftime("%d/%m/%y, %H:%M - ")
            except ValueError:
                continue
        return m.group(0)

    data = pattern_am_pm.sub(convert_match, data)

    pattern_24hr = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern_24hr, data)[1:]
    dates = re.findall(pattern_24hr, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        split_msg = re.split(r'^([^:]+):\s', message, maxsplit=1)
        if len(split_msg) > 2:
            users.append(split_msg[1])
            messages.append(split_msg[2])
        else:
            users.append('group_notification')
            messages.append(split_msg[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)

    df['date_for_timeline'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
