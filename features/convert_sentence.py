import random
import pandas as pd


# 단어를 랜덤하게 선택합니다.
def synonym_random_select(synonym_list: list, word: str):
    filtered_list = [synonym for synonym in synonym_list if synonym != word]
    synonym = random.choice(filtered_list)
    return synonym


# 문장을 변환합니다.
def convert_sentence(sentence: str, synonym_list: list):
    include_word = ""
    for word in synonym_list:
        if word in sentence:
            print(f"'{word}'가 포함되어있습니다.")
            include_word = word
            break

    synonym = synonym_random_select(synonym_list, include_word)
    converted_sentence = sentence
    if include_word:
        converted_sentence = sentence.replace(include_word, synonym)
    is_converted = True

    if sentence == converted_sentence:
        is_converted = False

    # 변환된 문장, 변환에 사용된 단어, 변환 성공 여부
    return converted_sentence, synonym, is_converted


# 일방향 문장을 변환합니다.
def convert_one_way_sentence(sentence: str, before_word: str, synonym_list: list, used_synonym_list: list):
    before_word_count = sentence.count(before_word)
    before_synonym = ""

    for i in range(before_word_count):
        synonym = synonym_random_select(synonym_list, before_synonym)
        index = sentence.find(before_word)
        if index >= 0:
            sentence = sentence[:index] + sentence[index:].replace(before_word, synonym, 1)
            used_synonym_list.append(synonym)
        # sentence = sentence.replace(before_word, synonym)
        before_synonym = synonym

    return sentence, used_synonym_list


# 양방향, 일방향 dataframe을 적용합니다.
def convert_from_db(
    original_sentence: str,
    ban_synonym: str,
    df_two_way: pd.DataFrame,
    df_one_way: pd.DataFrame,
):
    if ban_synonym == "":
        ban_synonym_list = []
    else:
        ban_synonym_list = ban_synonym.split("=")
        ban_synonym_list = [x for x in ban_synonym_list if x != ""]
        ban_synonym_list = [x for x in ban_synonym_list if x != " "]

    sentence = original_sentence
    used_synonym_list = []
    two_way_column_list = df_two_way.columns

    for two_way_column in two_way_column_list:
        data_list = df_two_way[str(two_way_column)].to_list()

        for data in data_list:
            try:
                data = str(data)
                synonym_list = data.split("=")

                # 빈 값 제거
                synonym_list = [x for x in synonym_list if x != ""]
                synonym_list = [x for x in synonym_list if x != " "]

                # 금지어 로직
                is_contain_ban_synonym = False
                for ban_synonym in ban_synonym_list:
                    for syn in synonym_list:
                        # 변환할 문장/단어에 금지어가 한글자라도 포함되어있다면 생략함
                        # if ban_synonym.find(syn) > -1:
                        #     is_contain_ban_synonym = True
                        #     break

                        # 변환할 문장/단어가 금지어와 완전히 일치하면 생략함
                        if ban_synonym == syn:
                            is_contain_ban_synonym = True
                            break

                    if is_contain_ban_synonym:
                        break

                if is_contain_ban_synonym:
                    continue

                # 신규 금지어 로직 -> 변환 리스트에서 금지어 리스트를 빼는 차집합 방식
                # 너무 많이 빼다보니 유의어 리스트가 없어서 오류가 발생할 수 있음.
                # Cannot choose from an empty sequence
                synonym_list = list(set(synonym_list) - set(ban_synonym_list))

                # 리스트가 1개 이하라면 넘김 (변환 할 필요가 없음)
                if len(synonym_list) <= 1:
                    continue

                sentence, synonym, is_converted = convert_sentence(sentence, synonym_list)

                is_converted: bool
                if is_converted:
                    # 변환에 사용된 단어를 금지어 리스트에 추가한다.
                    synonym: str
                    used_synonym_list.append(synonym)
                    ban_synonym_list.append(synonym)
                    print(f"금지어리스트: {ban_synonym_list}")

            except Exception as e:
                print(f"{data}: {e}")
                raise Exception(f"{data}: {e}")

    for j, row in df_one_way[:].iterrows():
        try:
            before = str(row["before"])
            after = str(row["after"])

            synonym_list = after.split("=")

            # 빈 값 제거
            synonym_list = [x for x in synonym_list if x != ""]
            synonym_list = [x for x in synonym_list if x != " "]

            # 기존 금지어 로직 -> 문장에 금지어가 한글자라도 포함되어있다면 생략함
            # if any(s in data for s in ban_synonym_list):
            #     continue

            # 신규 금지어 로직 -> 변환 리스트에서 금지어 리스트를 빼는 차집합 방식
            # 너무 많이 빼다보니 유의어 리스트가 없어서 오류가 발생할 수 있음.
            # Cannot choose from an empty sequence
            synonym_list = list(set(synonym_list) - set(ban_synonym_list))

            # 리스트에 아무것도 없다면 생략함
            if len(synonym_list) <= 0:
                continue

            sentence, used_synonym_list = convert_one_way_sentence(sentence, before, synonym_list, used_synonym_list)

        except Exception as e:
            print(f"{before} -> {after}: {e}")
            raise Exception(f"{before} -> {after}: {e}")
            continue

    # 유의어 리스트 중 단어의 길이가 긴 순서부터 차례로 앞쪽에 정렬
    used_synonym_list = sorted(used_synonym_list, key=len, reverse=True)

    return sentence, used_synonym_list


# 문단을 랜덤하게 섞습니다.
def shuffle_sentence(sentence: str):
    sentence_to_list = sentence.split(f"\n\n")
    print(sentence_to_list)

    random.shuffle(sentence_to_list)
    print(sentence_to_list)

    if len(sentence_to_list) > 0:
        sentence = f"\n\n".join(sentence_to_list)

    return sentence


def insert_header_to_sentence(sentence: str, header: str, convert_keyword: str):
    header = header.replace("$키워드$", convert_keyword)
    header += f"\n\n"

    sentence = header + sentence

    return sentence


def insert_footer_to_sentence(sentence: str, footer: str, convert_keyword: str):
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
