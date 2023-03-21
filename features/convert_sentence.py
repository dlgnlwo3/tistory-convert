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
            if word == "":
                print(f"유의어DB에 빈칸이 포함되어있습니다.")
                break
            print(f"'{word}'가 포함되어있습니다.")
            break

    synonym = synonym_random_select(synonym_list, word)
    converted_sentence = sentence.replace(word, synonym)
    is_converted = True

    if sentence == converted_sentence:
        is_converted = False

    # 변환된 문장, 변환에 사용된 단어, 변환 성공 여부
    return converted_sentence, synonym, is_converted


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
def convert_from_db(original_sentence: str, ban_synonym: str, df_two_way: pd.DataFrame, df_one_way: pd.DataFrame):
    if ban_synonym == "":
        ban_synonym_list = []
    else:
        ban_synonym_list = ban_synonym.split("=")
        ban_synonym_list = [x for x in ban_synonym_list if x != ""]
        ban_synonym_list = [x for x in ban_synonym_list if x != " "]

    sentence = original_sentence
    for i, row in df_two_way[:].iterrows():
        try:
            data = str(row["data"])

            if any(s in data for s in ban_synonym_list):
                continue

            synonym_list = data.split("=")

            # 빈 값 제거
            synonym_list = [x for x in synonym_list if x != ""]
            synonym_list = [x for x in synonym_list if x != " "]

            # 구분자만 입력한 배열은 넘김
            if len(synonym_list) <= 0:
                continue

            sentence, synonym, is_converted = convert_sentence(sentence, synonym_list)

            is_converted: bool
            if is_converted:
                # 변환에 사용된 단어를 금지어 리스트에 추가한다.
                synonym: str
                synonym_list = synonym.split(" ")
                for syn in synonym_list:
                    ban_synonym_list.append(syn)
                    print(f"금지어 추가: {syn}")

                print(f"금지어리스트: {ban_synonym_list}")

        except Exception as e:
            print(f"{data}: {e}")
            raise Exception(f"{data}: {e}")
            continue

    for j, row in df_one_way[:].iterrows():
        try:
            before = str(row["before"])
            after = str(row["after"])

            if any(s in before for s in ban_synonym_list):
                continue

            synonym_list = after.split("=")

            # 빈 값 제거
            synonym_list = [x for x in synonym_list if x != ""]
            synonym_list = [x for x in synonym_list if x != " "]

            # 구분자만 입력한 배열은 넘김
            if len(synonym_list) <= 0:
                continue

            sentence = convert_one_way_sentence(sentence, before, synonym_list)

        except Exception as e:
            print(f"{before} -> {after}: {e}")
            raise Exception(f"{before} -> {after}: {e}")
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
