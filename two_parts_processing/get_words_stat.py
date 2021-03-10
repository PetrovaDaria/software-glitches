from words_lists import software_words, bug_words


def get_words_stat(dict_words, text_words):
    stat = {}
    for dict_word in dict_words:
        word_count = text_words.count(dict_word)
        if word_count > 0:
            stat[dict_word] = word_count
    return stat


def get_software_news_stat(words):
    return get_words_stat(software_words, words)


def get_bug_words_stat(words):
    return get_words_stat(bug_words, words)


def is_software_bug_news(software_stat, bug_stat):
    return len(software_stat.keys()) > 0 and len(bug_stat.keys()) > 0


def get_collocations(words, dist=2):
    collocations = []
    for i in range(len(words)):
        current_word = words[i]
        is_first_word_is_soft = current_word in software_words
        is_first_word_is_bug = current_word in bug_words
        if is_first_word_is_soft or is_first_word_is_bug:
            for j in range(dist, 0, -1):
                if i + j < len(words):
                    second_current_word = words[i+j]
                    is_second_word_is_soft = second_current_word in software_words
                    is_second_word_is_bug = second_current_word in bug_words
                    if (is_first_word_is_soft and is_second_word_is_bug) or \
                            (is_first_word_is_bug and is_second_word_is_soft):
                        collocations.append(' '.join(words[i:i + j + 1]))
                        break
    return collocations
