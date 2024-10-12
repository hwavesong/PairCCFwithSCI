# -*- coding: utf-8 -*-
import re

import fitz


def is_only_digits(line):
    if re.fullmatch(r'\d+', line) is not None:
        return True
    return False


def find_category_title(text):
    chinese_pattern = r'（(.*?)）'  # todo::中英文括号混用
    english_pattern = r'\((.*?)\)'
    if re.search(chinese_pattern, text) is not None:
        return re.search(chinese_pattern, text).group(1)
    else:
        return re.search(english_pattern, text).group(1)

def get_entries(text_block):
    entries=[]

    for line in text_block.split():
        if is_only_digits(line):
            entries.append([])

        if len(entries)>0:
            entries[-1].append(line)

    formatted_entries = list()
    for each in entries:
        formatted_entries.append([each[0], each[1], ' '.join(each[2:-2]), each[-2], each[-1]])

    return formatted_entries


def extract_basic_info():
    doc = fitz.open('./CCF-中国计算机学会推荐国际学术会议和期刊目录-2022更名版.pdf')

    # 提取journal页面
    categories = [[]]
    journal_flag = True
    for idx, page in enumerate(doc):
        if idx == 0:
            continue

        raw_text = page.get_text('text')

        if '中国计算机学会推荐国际学术' in raw_text:
            if '期刊' in raw_text or '学术刊物' in raw_text: #todo::命名不一致
                journal_flag = True
            else:
                journal_flag = False
                categories.append([])

        if journal_flag:
            categories[-1].append(raw_text)

        # print(idx, ' '.join(raw_text.split()))

    # 分割不同的级别：A, B, C
    detailed_categories = []
    for category in categories[:-1]:
        title = find_category_title(''.join(category))

        concatenated_text = ''.join(category)

        A_start_idx = concatenated_text.index('一')
        B_start_idx = concatenated_text.index('二')
        C_start_idx = concatenated_text.index('三')

        level_A = concatenated_text[A_start_idx:B_start_idx]
        level_B = concatenated_text[B_start_idx:C_start_idx]
        level_C = concatenated_text[B_start_idx:]

        A_entries = get_entries(level_A)
        B_entries = get_entries(level_B)
        C_entries = get_entries(level_C)

        detailed_categories.append([title, A_entries, B_entries, C_entries])

    return detailed_categories

def write_markdown(detailed_categories):
    content = list()
    for category in detailed_categories:
        box = '## {}\n'.format(category[0])

        box += '### {}\n'.format('A类')
        box += "| 序号        | 刊物简称  |  刊物全称     | 出版社 | 网址      | 中科院分区 |\n| :----------- | :------- | :------- | :----------- | :----------- | :----------- |\n"
        for each in category[1]:
            box += '|{}|{}|{}|{}|{}|{} \n'.format(each[0], each[1], each[2], each[3], each[4], '', '')

        box += '\n### {}\n'.format('B类')
        box += "| 序号        | 刊物简称  |  刊物全称     | 出版社 | 网址      | 中科院分区 |\n| :----------- | :------- | :------- | :----------- | :----------- | :----------- |\n"
        for each in category[2]:
            box += '|{}|{}|{}|{}|{}|{} \n'.format(each[0], each[1], each[2], each[3], each[4], '', '')

        box += '\n### {}\n'.format('C类')
        box += "| 序号        | 刊物简称  |  刊物全称     | 出版社 | 网址      | 中科院分区 |\n| :----------- | :------- | :------- | :----------- | :----------- | :----------- |\n"
        for each in category[3]:
            box += '|{}|{}|{}|{}|{}|{} \n'.format(each[0], each[1], each[2], each[3], each[4], '', '')

        content.append(box)

    with open('./readme.md','w',encoding='utf8') as fw:
        fw.write('[TOC]\n\n' + '\n\n'.join(content))

if __name__ == '__main__':
    detailed_categories = extract_basic_info()
    write_markdown(detailed_categories)
