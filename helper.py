from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['users']==selected_user]

    # fetch the number of message
    num_messages = df.shape[0]

    #fetch total number of words
    words =[]
    for message in df['messages']:
        words.extend(message.split())


    # fetch number of media messages
    num_media_messages=df[df['messages'] == "<Media omitted>"].shape[0]

    # fetch number of links

    extractor = URLExtract()
    num_Of_links = []
    for link in df['messages']:
        num_Of_links.extend(extractor.find_urls(link))

    # most busy users
    most_busy = df['users'].value_counts().head()

    return num_messages, len(words) ,num_media_messages,len(num_Of_links) ,

def create_wordcloud(selected_user,df):
    if selected_user !="Overall":
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'sys/shared_message']
    temp = temp[temp['messages'] != '<Media omitted>']

    f=open("stopword.txt",encoding='utf-8')
    stopword=f.read().split()

    def remove_stpwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stopword:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400,height=400,min_font_size=4,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stpwords)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))

    return df_wc
def most_busy_user(df):
    # most busy users
    x = df['users'].value_counts().head()
    df = round((x/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df


def most_used_words(selected_user,df):
    if selected_user !="Overall":
        df = df[df['users']==selected_user]

    temp = df[df['users'] != 'sys/shared_message']
    temp = temp[temp['messages'] != '<Media omitted>']

    f=open("stopword.txt",encoding='utf-8')
    stopword=f.read().split()

    words1 = []
    for message in temp['messages']:
        word_lst = message.lower().split()
        for li in word_lst:
            words1.append(li)
    words = [i for i in words1 if i not in stopword]


    most_comm_df = pd.DataFrame(Counter(words).most_common(30))
    return most_comm_df

def emoji_analyser(selected_user,df):
    if selected_user !="Overall":
        df = df[df['users']==selected_user]

    i=emoji.unicode_codes.get_emoji_unicode_dict
    emoj =i(emoji.LANGUAGES[0])
    emojis=[]
    emojis.extend([c for c in [msg for msg in df['messages']] if c in [val for val in emoj.values()]])

    df_emoji = pd.DataFrame(Counter(emojis).most_common(10))
    return df_emoji


def monthly_timeline(selected_user,df):

    timeline = df.groupby(['year', 'month', 'month_name']).count()['messages'].reset_index()
    t=[str(timeline['month_name'][i])+'-'+str(timeline['year'][i]) for i in range(timeline.shape[0])]

    timeline['time'] = t
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']== selected_user]


    onlydate = df.groupby('only_date').count()['messages'].reset_index()
    return  onlydate


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_acitivity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month_name'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    pivot_table = df.pivot_table(
        index='day_name',
        columns='period',
        values='messages',
        aggfunc='count').fillna(0)
    return pivot_table
