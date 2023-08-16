import re
import urllib.parse

import pandas as pd


def remove_non_letters(s):
    return re.sub(r'[^a-zA-Z\s]', '', s)


def normalize_polish_characters(s):
    polish_to_european = {
        'ą': 'a', 'ć': 'c', 'ę': 'e',
        'ł': 'l', 'ó': 'o', 'ś': 's',
        'ź': 'z', 'ż': 'z'
    }
    result = ''.join(polish_to_european.get(c, c) for c in s.lower())
    return remove_non_letters(result)


def extract_title_from_url(url):
    if not isinstance(url, str):
        return ""
    url_unquoted = urllib.parse.unquote(url)
    title = url_unquoted.split('/')[-1]
    title = title.replace('-', ' ')
    return remove_non_letters(title)


def match_reviews(df):
    for index, row in df.iterrows():
        normalized_title = normalize_polish_characters(str(row['tytuł']))
        normalized_title_words = normalized_title.split(' ')
        for url in df['recenzja']:
            url_title = normalize_polish_characters(extract_title_from_url(str(url)))
            url_title_words = url_title.split(' ')

            # Check if the first 2 words of the normalized title match the first 2 words of the URL title
            if normalized_title_words[:2] == url_title_words[:2]:
                print(f"MATCH! {str(row['tytuł'])}: {url_title}")
                df.at[index, 'recenzja_1'] = url
                break
    return df


if __name__ == "__main__":
    file_path = 'data.xlsx'
    df = pd.read_excel(file_path)
    result = match_reviews(df)
    result.to_excel('data_matched_reviews.xlsx')
