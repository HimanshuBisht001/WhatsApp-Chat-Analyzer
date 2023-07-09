import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}[ \u202f]?[APM]{2} - '
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Remove non-breaking space character from the extracted dates
    dates = [re.sub('\u202f', '', date) for date in dates]

    # create pandas dataframe with two columns
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M%p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seprate users and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)


    # Create df of Year, Months, Day, Hour, Minute
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df