import random


sentence = "폐어망·폐생수통이 '갤럭시 S23'으로 화려하게 변신"

synonym_data = "수려하게,유려하게,아름답게,화려하게"

synonym_list = synonym_data.split(",")


def synonym_random_select(synonym_list: list, word: str):
    filtered_list = [synonym for synonym in synonym_list if synonym != word]
    synonym = random.choice(filtered_list)
    return synonym


def convert_sentence(sentence: str, synonym_list: list):

    for word in synonym_list:
        if word in sentence:
            print(f"'{word}'가 포함되어있습니다.")
            break

    synonym = synonym_random_select(synonym_list, word)
    sentence = sentence.replace(word, synonym)
    return sentence


def convert_one_way_sentence(sentence: str, before: str, synonym_list: list):

    synonym = synonym_random_select(synonym_list, before)
    sentence = sentence.replace(before, synonym)
    return sentence




sentence = convert_sentence(sentence, synonym_list)

print(sentence)
