import pandas as pd ,re


def propro(lst):
    # Initialize an empty list to store the modified items
    new_lst = []

    # Initialize a variable to store the previous datetime value
    last_dt = None

    # Loop through the list
    for msg in lst:
        # Check if the message starts with a datetime pattern
        if re.match(r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m', msg):
            # If it does, add it to the new list and update the previous datetime value
            new_lst.append(msg)
            last_dt = msg
        else:
            # If it doesn't, concatenate it with the previous item in the new list
            new_lst[-1] = f'{last_dt}#{new_lst[-1]} {msg}'
    return new_lst


def preprocessor(data):
    # f = open("WhatsApp Chat with Reema.txt", encoding="utf-8")
    # data = f.read()
    data = data.split('\n')

    data=propro(data)

    messages = []
    dates = []
    # remove empty messages
    for message in data:
        if len(message) == 0:
            data.remove(message)
    # separate data and messages from data
    for message in data:
        #     remove extra spaces from ends
        message = message.strip()
        #     split dates and messages
        entry = message.split(r" - ")
        if len(entry) < 2:
            #         put dates in those messages which do not have
            if len(entry) == 1:
                dates.append(dates[-1])
                messages.append(entry[0])
        else:
            dates.append(entry[0])
            messages.append(entry[1])


    # make dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert dates from string to dateformat
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p',errors='coerce')
    # convert time in 12 hours format
    df['message_date'] = df['message_date'].dt.strftime('%d-%m-%Y %I:%M %p')
    # Separate users from messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages

    # convert 'message_date' column to datetime format with 'coerce' option
    df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')

    # extract day, month, and year
    df['day'] = df['message_date'].dt.day
    df['month'] = df['message_date'].dt.month
    df['year'] = df['message_date'].dt.year
    df['time'] = df['message_date'].dt.time
    df['hours'] = df['message_date'].dt.hour
    # extract time in 12-hour format
    df['time'] = df['message_date'].dt.strftime('%I:%M %p')

    def month_name(month):
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        return month_dict[month]

    df['month_name'] = df['month'].apply(month_name)
    df['message_date'] = pd.to_datetime(df['message_date'])
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-0' + str(hour + 1))
        elif hour >= 0 and hour <= 8:
            period.append('0' + str(hour) + '-0' + str(hour + 1))
        elif hour == 9:
            period.append('0' + str(hour) + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period
    df.drop(columns=['user_message','user_message'],inplace=True)
    return df

