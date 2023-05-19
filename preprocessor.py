import pandas as pd
import re
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message':messages , 'time':dates})
    df['time'] = pd.to_datetime(df['time'],format = '%d/%m/%y, %H:%M - ')

    # separate user and message
    user = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('Group notification')
            messages.append(message)
    df['user'] = user
    df['message'] = messages
    df.drop(columns =['user_message'],inplace=True)

    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month_name()
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    df['num_month'] = df['time'].dt.month
    df['day_name'] = df['time'].dt.day_name()
    # df.drop(columns=['time'],inplace=True)
    period = []
    for i in range(df.shape[0]):
        if df['hour'][i]==23:
            period.append(str(df['hour'][i])+'-'+'00')
        else:
            period.append(str(df['hour'][i])+'-'+str(df['hour'][i]+1))
    df['period'] = period

    return df