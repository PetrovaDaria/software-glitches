from warcio.archiveiterator import ArchiveIterator
from newspaper import Article
import json
import re
from words_lists import software_words, bug_words

# warcio recompress ./CC-NEWS-20161222115112-00000_ENG.warc.gz ./news3.warc.gz

# web_archive_path = 'news.warc.gz'
# possible_json_path = 'possible_news.json'
# news_json_path = 'news.json'

# web_archive_path = 'news2.warc.gz'
# possible_json_path = 'possible_news2.json'
# news_json_path = 'news2.json'

web_archive_path = 'news3.warc.gz'
possible_json_path = 'possible_news3.json'
news_json_path = 'news3.json'


def form_news(
        identifier,
        news,
        url,
        software_words_dict,
        bug_words_dict,
        title_collocations,
        text_collocations,
):
    return {
        'id': identifier,
        'url': url,
        'title': news.title,
        'text': news.text,
        'software_words': software_words_dict,
        'bug_words': bug_words_dict,
        'title_collocations': title_collocations,
        'text_collocations': text_collocations
    }


def is_word_in_words_list(word, words_list):
    if len(word) <= 2:
        return False
    for w in words_list:
        if abs(len(w) - len(word)) <= 3:
            is_substr = w.startswith(word) or word.startswith(w)
            is_substr_with_y_ending = word[-1] == 'y' and w.startswith(word[:-1])
            # является ли полностью слово подстрокой или слово с последней буквой y (technology => technologies)
            if is_substr or is_substr_with_y_ending:
                return True
    return False


def get_collocations(words, dist=2):
    collocations = []
    for i in range(len(words)):
        current_word = words[i]
        # пока что оба слова могут быть из одной категории
        is_first_word_is_soft = is_word_in_words_list(current_word, software_words)
        is_first_word_is_bug = is_word_in_words_list(current_word, bug_words)
        if is_first_word_is_soft or is_first_word_is_bug:
            for j in range(dist, 0, -1):
                if i + j < len(words):
                    second_current_word = words[i+j]
                    is_second_word_is_soft = is_word_in_words_list(second_current_word, software_words)
                    is_second_word_is_bug = is_word_in_words_list(second_current_word, bug_words)
                    if (is_first_word_is_soft and is_second_word_is_bug) or \
                            (is_first_word_is_bug and is_second_word_is_soft):
                        collocations.append(' '.join(words[i:i + j + 1]))
                        break
    return collocations


def get_software_and_bug_words_from_news(title, text):
    punct = '[!@#$%^&*()_+<>?:.,;\n\t]+'
    title_without_punct = re.sub(punct, '', title.lower())
    text_without_punct = re.sub(punct, '', text.lower())
    title_words = title_without_punct.split(' ')
    text_words = text_without_punct.split(' ')
    title_collocations = get_collocations(title_words, dist=3)
    text_collocations = get_collocations(text_words, dist=3)
    all_words = title_words + text_words
    software_words_dict = get_words_dict(software_words, all_words)
    bug_words_dict = get_words_dict(bug_words, all_words)
    return software_words_dict, bug_words_dict, title_collocations, text_collocations


def is_possible_software_and_bug_news(software_words_dict, bug_words_dict):
    return len(software_words_dict.keys()) > 0 and len(bug_words_dict.keys()) > 0


def is_software_and_bug_news(title_collocations, text_collocations):
    return len(title_collocations) > 0 or len(text_collocations) > 0


def count_word_in_text(word, text_words):
    if word == 'blunder':
        s = ''
    count = 0
    for w in text_words:
        if len(w) > 2 and abs(len(w) - len(word)) <= 3:
            is_substr = w.startswith(word) or word.startswith(w)
            is_substr_with_y_ending = w[-1] == 'y' and word.startswith(w[:-1])
            if is_substr or is_substr_with_y_ending:
                count += 1
    return count


def get_words_dict(words_list, text_words):
    words_dict = {}
    for word in words_list:
        word_count = count_word_in_text(word, text_words)
        if word_count > 0:
            words_dict[word] = word_count
    return words_dict


def main():
    possible_software_bug_news = []
    software_bug_news = []
    try:
        with open(web_archive_path, 'rb') as stream:
            i = 0
            for record in ArchiveIterator(stream):
                url = record.rec_headers.get_header('WARC-Target-URI')
                if record.rec_type == 'response':
                    text = record.content_stream().read()
                    article = Article(url='test')
                    article.download(input_html=text)
                    article.parse()
                    software_words_dict, bug_words_dict, title_collocations, text_collocations = \
                        get_software_and_bug_words_from_news(article.title, article.text)
                    is_possible_news = is_possible_software_and_bug_news(software_words_dict, bug_words_dict)
                    if is_possible_news:
                        news = form_news(i, article, url, software_words_dict, bug_words_dict,
                                         title_collocations, text_collocations)
                        possible_software_bug_news.append(news)
                        is_needed_news = is_software_and_bug_news(title_collocations, text_collocations)
                        if is_needed_news:
                            software_bug_news.append(news)
                        print(i)
                        print(url)
                        print('is possible software bug news ', is_possible_news)
                        print('is software bug news ', is_needed_news)
                i += 1
        print('possible news count ', len(possible_software_bug_news))
        print('news count ', len(software_bug_news))
        with open(possible_json_path, 'w') as f:
            json.dump(possible_software_bug_news, f, indent=2)
        with open(news_json_path, 'w') as f:
            json.dump(software_bug_news, f, indent=2)
    except:
        print('possible news count ', len(possible_software_bug_news))
        print('news count ', len(software_bug_news))
        with open(possible_json_path, 'w') as f:
            json.dump(possible_software_bug_news, f, indent=2)
        with open(news_json_path, 'w') as f:
            json.dump(software_bug_news, f, indent=2)


# def main():
#     title = 'Samsung Has Fixed Fingerprint Bug on Galaxy Note 10 & Galaxy S10; Your Bank Data is Safe'
#     # text = 'Samsung Electronics Co Ltd has updated software to fix problems with fingerprint recognition' \
#     #        ' features on its flagship Galaxy S10 and Note 10 smartphones. Samsung issued an apology via' \
#     #        ' its customer support app Samsung Members and told its Galaxy phone users to update their' \
#     #        ' biometric authentication to the latest software version. “Samsung Electronics takes the' \
#     #        ' security of products very seriously and will make sure to strengthen security through' \
#     #        ' continuing improvement and updates to enhance biometric authentication functions,” the' \
#     #        ' company said on its Korean app. A British user told The Sun newspaper that a bug on her' \
#     #        ' Galaxy S10 allowed it to be unlocked regardless of the biometric data registered in the device.' \
#     #        ' Samsung has said the issue can happen when patterns appearing on certain protectors that come with' \
#     #        ' silicon cases are recognised along with fingerprints. Once touted as a revolutionary feature by Samsung,' \
#     #        ' its ultrasonic fingerprint sensors were fooled by tech reviewers. Videos on tech community websites ' \
#     #        'show Galaxy devices can be unlocked through silicon protectors using a persimmon or a small doll. ' \
#     #        'Samsung said it would send notifications for software updates to Galaxy S10 and Note 10 users who ' \
#     #        'have registered their biometric data. The Bank of China has pulled fingerprint payments from certain ' \
#     #        'Samsung devices and Alipay’s fingerprint payment verification function app has been temporarily suspended ' \
#     #        'for some Galaxy devices.'
#     text = 'has updated software to fix problems appropriate to appreciate'
#     software_words_dict, bug_words_dict, title_collocations, text_collocations = get_software_and_bug_words_from_news(title, text)
#     print('software words dict ', software_words_dict)
#     print('bug words dict ', bug_words_dict)
#     print('title collocations ', title_collocations)
#     print('text collocations ', text_collocations)


if __name__ == '__main__':
    main()
