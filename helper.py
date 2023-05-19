from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    # 1. number of message:
    num_message =  df.shape[0]
    # 2.Number of words:
    words =[]
    url = []
    for messages in df['message']:
        words.extend(messages.split())
        # url.extend(URLExtract().find_urls(messages))
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_message,len(words),num_media


def fetch_mostbusyuser(df):
    x = df['user'].value_counts().head()
    percent = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    percent.columns = ['User','Percent']
    return x,percent

def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    f = open('stop_hinglish.txt','r')
    stop_word = f.read()
    temp = df[df['user']!='Group notification']
    temp = temp[temp['message']!= '<Media omitted>\n']
    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)        

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_word = f.read()
    
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    temp = df[df['user']!='Group notification']
    temp = temp[temp['message']!= '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)
    mostcommon_df = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon_df
    
def dailymonthly_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time'] = time

    df['date'] = df['time'].dt.date
    daily_timeline = df.groupby(['date']).count()['message'].reset_index()
    return timeline,daily_timeline

def day_activeness(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    day_activity = df['day_name'].value_counts().reset_index()
    day_activity.columns = ['days','times']
    return day_activity

def month_activeness(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    month_activity = df.groupby(['month']).count()['message'].reset_index()
    month_activity.columns = ['months' , 'message']
    return month_activity

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap