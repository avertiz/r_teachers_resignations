import pandas as pd

def clean(teachers_file):
    data = pd.read_csv(teachers_file)
    data = data[data['selftext'] != '[removed]']
    data['link_flair_text'] = data['link_flair_text'].str.replace('&amp;','&')
    data['link_flair_text'] = data['link_flair_text'].fillna('No Flair')
    return(data)

if __name__ == '__main__':
    data_cleaned = clean(teachers_file = 'teachers.csv')
    data_cleaned.to_csv('teachers_cleaned.csv', index=False)
    print('complete')