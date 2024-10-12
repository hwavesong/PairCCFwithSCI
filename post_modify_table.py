# -*- coding: utf-8 -*-
import re

def change_to_dblp():
    new_content = list()

    url_expression = re.compile(r'\|(http[s]?://[^\s|]+)\|')
    with open('./readme.md','r',encoding='utf8') as fr:
        for line in fr:
            result = re.findall(url_expression, line)

            if len(result) > 0:
                new_content.append(line.replace(result[0], '[DBLP]({})'.format(result[0])))
            else:
                new_content.append(line)

            if len(result) == 0 and 'http' in line:
                raise NotImplementedError

    with open('./readme1.md', 'w', encoding='utf8') as fw:
        for line in new_content:
            fw.write(line)


if __name__ == '__main__':
    change_to_dblp()
