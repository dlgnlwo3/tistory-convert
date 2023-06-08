import random
import pandas as pd
from common.utils import check_common_element
from enums.convert_enum import Words
import re



# 부분적인 $랜덤$ $랜덤/$ 사이의 문장만 섞습니다.
def get_partial_suffle_sentence(text:str, start_word:str, end_word:str):

    sentences = []
    start_index = 0

    while True:
        find_first_index = text.find(start_word, start_index)

        if find_first_index == -1:
            
            # 마지막 문장 넣기
            sentences.append(text[start_index:])
            break
        
        # 첫번째 $random$기호
        before_sentence = text[start_index : find_first_index]
        sentences.append(before_sentence)
        start_index = find_first_index + len(start_word)
        find_end_index = text.find(end_word, find_first_index)
        between_sentence = text[start_index: find_end_index]
        between_sentence = get_shuffle_sentence(between_sentence)
        sentences.append(between_sentence)
        
        start_index = find_end_index + len(end_word) + 1

    return "".join(sentences)

def get_shuffle_sentence(sentence: str):
    sentence_to_list = sentence.split(Words.SENTENCE_SPLIT.value)

    random.shuffle(sentence_to_list)

    if len(sentence_to_list) > 0:
        sentence = Words.SENTENCE_SPLIT.value.join(sentence_to_list)

    return sentence


# 단어를 랜덤하게 선택합니다.
def synonym_random_select(synonym_list: list, word: str):
    filtered_list = [synonym for synonym in synonym_list if synonym != word]
    synonym = random.choice(filtered_list)
    return synonym


def append_no_changed_idx_list(
    ban_synonym_list: list,
    origin_sentence: str,
):
    no_change_idx_list = []
    for word in ban_synonym_list:
        # 1. word가 포함된 문장 위치를 가져옴
        start_idx_list = [
            i
            for i in range(len(origin_sentence))
            if origin_sentence.startswith(word, i)
        ]

        len_word = len(word)  # 변환대상 단어 길이
        for start_i in start_idx_list:
            # 단어 숫자만큼 입력
            for include_i in range(0, len_word):
                key = start_i + include_i  # sentence에 들어가야할 위치

                # 기존에 건드렸던 영역이면 더 이상 건들지 않는다.
                if not key in no_change_idx_list:
                    no_change_idx_list.append(key)

    return no_change_idx_list


def update_dict_sentence(
    before_word: str,
    after_word: str,
    dict_sentence: dict,
    used_idx_list: list,
    ban_idx_list: list,
    origin_sentence: str,
    is_convert_once: bool,  # 한번만 변환
):
    # 1. before_word가 포함된 문장 위치를 가져옴
    start_idx_list = [
        i
        for i in range(len(origin_sentence))
        if origin_sentence.startswith(before_word, i)
    ]

    len_before_word = len(before_word)  # 변환대상 단어 길이
    len_after_word = len(after_word)  # 변환할 유의어 길이

    # 발견된 단어수 만큼 반복
    for start_i in start_idx_list:
        # 단어 전체중 밴 리스트와 겹치는게 하나라도 있으면 continue 해야함
        before_word_idx_list = list(range(start_i, start_i + len_before_word))
        if check_common_element(before_word_idx_list, ban_idx_list):
            continue

        before_count = len(used_idx_list)

        for include_i in range(0, len_before_word):
            key = start_i + include_i  # sentence에 들어가야할 위치

            try:
                value = after_word[include_i]
                if (
                    include_i == (len_before_word - 1)
                    and len_before_word < len_after_word
                ):
                    # after_word가 더 긴 경우
                    value = after_word[include_i:len_after_word]
            except:
                if len_before_word < len_after_word:
                    # after_word가 더 긴 경우
                    value = after_word[include_i:len_after_word]
                else:
                    value = ""

            # 기존에 건드렸던 영역이면 이거나 금지 영역이면 건드리지 않는다.
            if not key in used_idx_list:
                dict_sentence.update({key: value})
                used_idx_list.append(key)

        after_count = len(used_idx_list)
        if is_convert_once and before_count != after_count:
            break

    if len(used_idx_list) > 0:
        used_idx_list = sorted(list(set(used_idx_list)))

    return dict_sentence, used_idx_list


def get_split_and_remove_empty_list(text: str) -> list:
    split_and_remove_empty_list = text.split("=")
    split_and_remove_empty_list = [x for x in split_and_remove_empty_list if x != ""]
    split_and_remove_empty_list = [x for x in split_and_remove_empty_list if x != " "]
    return split_and_remove_empty_list


# 양방향, 일방향 dataframe을 적용합니다.
def convert_from_db_two_way(
    sentence: str,
    ban_synonym: str,
    df_two_way: pd.DataFrame,
    df_one_way: pd.DataFrame,
):
    if ban_synonym == "":
        ban_synonym_list = []
    else:
        ban_synonym_list = get_split_and_remove_empty_list(ban_synonym)

    sentence_list = list(sentence)
    dict_sentence = {i: word for i, word in enumerate(sentence_list)}

    used_idx_list = []
    ban_idx_list = append_no_changed_idx_list(ban_synonym_list, sentence)

    # 1. 양방향 변환 시작
    two_way_column_list = df_two_way.columns.to_list()
    for two_way_column in two_way_column_list:
        synonym_dbs = df_two_way[str(two_way_column)].to_list()

        for synonym_db in synonym_dbs:
            try:
                synonym_db = str(synonym_db)
                synonym_list = get_split_and_remove_empty_list(synonym_db)

                to_change_list = []
                for synonym in synonym_list:

                    finded_count = sentence.count(synonym)
                    if finded_count > 0:
                        for word_idx in range(finded_count + 1):
                            after_word = synonym_random_select(synonym_list, synonym)
                            if after_word:
                                to_change_list.append(
                                    {"Before": synonym, "After": after_word}
                                )

                # 유의어 대상에 하나도 포함되어 있지 않다면?
                if len(to_change_list) == 0:
                    continue

                for dict_change in to_change_list:
                    dict_sentence, used_idx_list = update_dict_sentence(
                        dict_change["Before"],
                        dict_change["After"],
                        dict_sentence,
                        used_idx_list,
                        ban_idx_list,
                        sentence,
                        is_convert_once=True,
                    )

            except Exception as e:
                raise Exception(f"{to_change_list} -> {after_word}: {e}")

    # 2. 일방향 변환 시작
    for j, row in df_one_way[:].iterrows():
        try:
            before_word = str(row["before"])
            str_after = str(row["after"])

            synonym_list = get_split_and_remove_empty_list(str_after)

            # Before 워드에 해당하는게 없으면 넘긴다.
            if sentence.find(before_word) == -1:
                continue

            # 리스트에 아무것도 없다면 생략함
            if len(synonym_list) <= 0:
                continue

            # 리스트에 1개만 있다면 그 단어로 치환함
            elif len(synonym_list) == 1:
                after_word = synonym_list[0]
            else:
                after_word = synonym_random_select(synonym_list, before_word)
            if not after_word:
                continue

            dict_sentence, used_idx_list = update_dict_sentence(
                before_word,
                after_word,
                dict_sentence,
                used_idx_list,
                ban_idx_list,
                sentence,
                is_convert_once=False,
            )

        except Exception as e:
            raise Exception(f"{before_word} -> {after_word}: {e}")

    return dict_sentence, used_idx_list


# 일방향, 양방향 dataframe을 적용합니다.
def convert_from_db(
    sentence: str,
    ban_synonym: str,
    df_two_way: pd.DataFrame,
    df_one_way: pd.DataFrame,
):
    if ban_synonym == "":
        ban_synonym_list = []
    else:
        ban_synonym_list = get_split_and_remove_empty_list(ban_synonym)

    sentence_list = list(sentence)
    dict_sentence = {i: word for i, word in enumerate(sentence_list)}

    used_idx_list = []
    ban_idx_list = append_no_changed_idx_list(ban_synonym_list, sentence)

    # 2. 일방향 변환 시작
    for j, row in df_one_way[:].iterrows():
        try:
            before_word = str(row["before"])
            str_after = str(row["after"])

            synonym_list = get_split_and_remove_empty_list(str_after)

            # Before 워드에 해당하는게 없으면 넘긴다.
            if sentence.find(before_word) == -1:
                continue

            # 리스트에 아무것도 없다면 생략함
            if len(synonym_list) <= 0:
                continue

            # 리스트에 1개만 있다면 그 단어로 치환함
            elif len(synonym_list) == 1:
                after_word = synonym_list[0]
            else:
                after_word = synonym_random_select(synonym_list, before_word)
            if not after_word:
                continue

            dict_sentence, used_idx_list = update_dict_sentence(
                before_word,
                after_word,
                dict_sentence,
                used_idx_list,
                ban_idx_list,
                sentence,
                is_convert_once=False,
            )

        except Exception as e:
            print(f"{before_word} -> {after_word}: {e}")
            raise Exception(f"{before_word} -> {after_word}: {e}")

    # 1. 양방향 변환 시작
    two_way_column_list = df_two_way.columns.to_list()
    for two_way_column in two_way_column_list:
        synonym_dbs = df_two_way[str(two_way_column)].to_list()

        for synonym_db in synonym_dbs:
            try:
                synonym_db = str(synonym_db)
                synonym_list = get_split_and_remove_empty_list(synonym_db)

                to_change_list = []
                for synonym in synonym_list:
                    if synonym == "을 만큼":
                        print("")
                    finded_count = sentence.count(synonym)
                    if finded_count > 0:
                        for word_idx in range(finded_count + 1):
                            after_word = synonym_random_select(synonym_list, synonym)
                            if after_word:
                                to_change_list.append(
                                    {"Before": synonym, "After": after_word}
                                )

                # 유의어 대상에 하나도 포함되어 있지 않다면?
                if len(to_change_list) == 0:
                    continue

                for dict_change in to_change_list:
                    dict_sentence, used_idx_list = update_dict_sentence(
                        dict_change["Before"],
                        dict_change["After"],
                        dict_sentence,
                        used_idx_list,
                        ban_idx_list,
                        sentence,
                        is_convert_once=True,
                    )

            except Exception as e:
                print(f"{to_change_list} -> {after_word}: {e}")
                raise Exception(f"{to_change_list} -> {after_word}: {e}")

    return dict_sentence, used_idx_list

# 문단을 랜덤하게 섞습니다.
def shuffle_sentence(sentence: str):

    if sentence.find(Words.RANDOM_START_WORD.value) > -1 and sentence.find(Words.RANDOM_END_WORD.value) > 1:
        return get_partial_suffle_sentence(sentence, Words.RANDOM_START_WORD.value, Words.RANDOM_END_WORD.value)

    return get_shuffle_sentence(sentence)



def insert_header_to_sentence(sentence: str, header: str, convert_keyword: str):
    header = header.replace(Words.REPLACE_KEYWORD.value, convert_keyword)
    header += Words.SENTENCE_SPLIT.value

    sentence = header + sentence

    return sentence


def insert_footer_to_sentence(sentence: str, footer: str, convert_keyword: str):
    footer = footer.replace(Words.REPLACE_KEYWORD.value, convert_keyword)
    footer = Words.SENTENCE_SPLIT.value + footer

    sentence = sentence + footer

    return sentence


def replace_keyword(text: str, convert_keyword: str):
    text = text.replace(Words.REPLACE_KEYWORD.value, convert_keyword)
    return text


# 테스트용 코드

origin_sentence = "예시문장"

origin_sentence_list = list(origin_sentence)

origin_sentence_dict = {i + 1: word for i, word in enumerate(origin_sentence_list)}

