import re

def preprocess_text(text):
    """
    텍스트에 있는 url, email, 전화번호, 특정 문자, 반복되는 문자, 이모지를 제거하는 함수
    """
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Remove Email
    text = re.sub(r'[\w-]+@[\w.]+', '', text)

    # Remove Phone Number
    text = re.sub(r"\d{3}-\d{4}-\d{4}", '', text)

    # 특수문자 제거
    text = re.sub(r'[*!-]', '', text)

    # 반복 문자 제거
    text = re.sub(r'(.)\1+', '', text)
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
                      "]+", re.UNICODE)
    text = re.sub(emoji_pattern, '', text)
    return text