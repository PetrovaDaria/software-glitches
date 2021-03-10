import re
import os

text1 = '''
0:30 Trying to get your baby to sleep? Let them cry it out Pause

1:01 Don't let a text wreck your life

2:17 Dance helps D'Iberville boy overcome ADHD

2:12 Watch baby polar bear Nora grow up fast

5:41 Video: Montana dash-cam video shows crashes, dangers of winter driving

0:22 NASA animates the powerful winter storm headed for the Mid-Atlantic

1:01 Video: Mountain lion kittens born in California play for camera

2:32 Vincent the cat gets very rare prosthetic legs

1:03 Video: How to wash your hands

1:08 'Lucky' Turkey to Receive Presidential Pardon
'''

text2 = '''
The British Airways i360 viewing tower has been closed for checks after it suffered technical problems twice in the past week.

About 200 people were trapped at ground level for more than an hour after problems with a door sensor on Sunday.

And a previous problem left 180 passengers stuck in mid-air on Thursday for about two hours.

A spokeswoman for the attraction, which stands at the site of the entrance to the former West Pier in Brighton, said that the i360 had been shut while the checks were carried out.

She said on Monday: “British Airways i360 is closed today while specialist technicians conduct further checks onsite. We apologise for any inconvenience caused. Customers who have booked tickets for flights today will be offered alternative visits or refunds.”

The i360 is the world’s tallest moving observation tower. It is 161 metres tall and allows visitors to travel in a 360-degree curved-glass 
'''


def mark_date_from_archive_name(archive_name):
    result = re.search(r'CC-NEWS-(\d{8}).*', archive_name)
    return result.group(1)


print(mark_date_from_archive_name('CC-NEWS-20160826124520-00000_ENG'))


def is_only_time_paragraphs(text):
    '''
    Проверяет текст на то, состоит ли он только из параграфов, которые начинаются с паттерна \d\d:\d\d
    Обычно такие тексты не имеют смысла, потому что они состоят из коротких сводок очень разных новостей
    :param text: текст
    :return: True - если текст является сводкой новостей, иначе False
    '''
    paragraphs = list(filter(lambda x: x != '', text.split('\n')))
    time_sentences_count = 0
    for paragraph in paragraphs:
        result = re.match(r'\d{1,2}:\d{1,2}', paragraph)
        if result is not None:
            time_sentences_count += 1
    return time_sentences_count == len(paragraphs)
