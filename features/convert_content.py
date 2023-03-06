import random


content = "폐어망·폐생수통이 '갤럭시 S23'으로 화려하게 변신"


synonym_db = ["수려하게", "유려하게", "아름답게", "화려하게"]


def synonym_random_select(synonym_db: list, word: str):
    filtered_list = [synonym for synonym in synonym_db if synonym != word]
    synonym = random.choice(filtered_list)
    return synonym


def convert_content(content: str, synonym_db: list):

    for word in synonym_db:
        if word in content:
            print(f"'{word}'가 포함되어있습니다.")
            break

    synonym = synonym_random_select(synonym_db, word)

    content = content.replace(word, synonym)

    return content


content = convert_content(content, synonym_db)

print(content)
