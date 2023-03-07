import random
import pandas as pd


# 단어를 랜덤하게 선택합니다.
def synonym_random_select(synonym_list: list, word: str):
    filtered_list = [synonym for synonym in synonym_list if synonym != word]
    synonym = random.choice(filtered_list)
    return synonym


# 문장을 변환합니다.
def convert_sentence(sentence: str, synonym_list: list):
    for word in synonym_list:
        if word in sentence:
            print(f"'{word}'가 포함되어있습니다.")
            break

    synonym = synonym_random_select(synonym_list, word)
    sentence = sentence.replace(word, synonym)
    return sentence


# 일방향 문장을 변환합니다.
def convert_one_way_sentence(sentence: str, before_word: str, synonym_list: list):
    before_word_count = sentence.count(before_word)
    before_synonym = ""

    for i in range(before_word_count):
        synonym = synonym_random_select(synonym_list, before_synonym)
        index = sentence.find(before_word)
        if index >= 0:
            sentence = sentence[:index] + sentence[index:].replace(before_word, synonym, 1)
        # sentence = sentence.replace(before_word, synonym)
        before_synonym = synonym

    return sentence


# 양방향, 일방향 dataframe을 적용합니다.
def convert_from_db(
    original_sentence: str,
    ban_synonym: str,
    df_two_way: pd.DataFrame,
    df_one_way: pd.DataFrame,
    synonym_convert_limit: int = None,
):
    if ban_synonym == "":
        ban_synonym_list = []
    else:
        ban_synonym_list = ban_synonym.split(",")

    sentence = original_sentence
    for i, row in df_two_way[:synonym_convert_limit].iterrows():
        try:
            data = str(row["data"])

            if any(s in data for s in ban_synonym_list):
                continue

            synonym_list = data.split(",")
            sentence = convert_sentence(sentence, synonym_list)

        except Exception as e:
            print(e)
            continue

    for j, row in df_one_way[:synonym_convert_limit].iterrows():
        try:
            before = str(row["before"])
            after = str(row["after"])

            if any(s in before for s in ban_synonym_list):
                continue

            synonym_list = after.split(",")
            sentence = convert_one_way_sentence(sentence, before, synonym_list)

        except Exception as e:
            print(e)
            continue

    return sentence


# 문단을 랜덤하게 섞습니다.
def shuffle_sentence(sentence: str):
    sentence_to_list = sentence.split(f"\n\n")
    print(sentence_to_list)

    random.shuffle(sentence_to_list)
    print(sentence_to_list)

    if len(sentence_to_list) > 0:
        sentence = f"\n\n".join(sentence_to_list)

    return sentence


def insert_header_to_sentence(sentence: str, header_topic: str, saved_data_header: dict, convert_keyword: str):
    header: str = random.choice(saved_data_header[header_topic])

    header = header.replace("$키워드$", convert_keyword)
    header += f"\n\n"

    sentence = header + sentence

    return sentence


def insert_footer_to_sentence(sentence: str, footer_topic: str, saved_data_footer: dict, convert_keyword: str):
    footer: str = random.choice(saved_data_footer[footer_topic])

    footer = footer.replace("$키워드$", convert_keyword)
    footer = f"\n\n" + footer

    sentence = sentence + footer

    return sentence


# 테스트용 코드

# sentence = "폐어망·폐생수통이 '갤럭시 S23'으로 화려하게 변신"

# ban_synonym = '화려하게'

# synonym_data = "수려하게,유려하게,아름답게,화려하게"

# synonym_list = synonym_data.split(",")

# sentence = convert_sentence(sentence, synonym_list)

# print(sentence)
