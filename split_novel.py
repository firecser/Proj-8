import os
import re

# 定义最大字数限制
MAX_WORDS = 10000

# 定义章节匹配正则表达式
# 优化章节匹配正则表达式，支持"第X章"和"第X章 章节标题"格式
CHAPTER_PATTERN = re.compile(r'\n第[一二三四五六七八九十百千万零]+章[^\n]*\n')

def split_novel_by_chapter(file_path, output_dir, start_chapter_num):
    # 读取小说内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找所有章节位置
    chapters = [(m.start(), m.end()) for m in CHAPTER_PATTERN.finditer(content)]

    # 如果没有找到章节，则将整个文件作为一个章节
    if not chapters:
        save_chapter(content, start_chapter_num, output_dir)
        return start_chapter_num + 1

    # 添加文件开头到第一个章节的内容
    if chapters[0][0] > 0:
        save_chapter(content[:chapters[0][0]], start_chapter_num, output_dir)
        start_chapter_num += 1

    # 遍历章节进行分割
    for i, (chapter_start, chapter_end) in enumerate(chapters):
        # 获取当前章节内容
        if i < len(chapters) - 1:
            chapter_content = content[chapter_start:chapters[i+1][0]]
        else:
            chapter_content = content[chapter_start:]
        
        # 保存章节，使用实际章节号
        save_chapter(chapter_content, start_chapter_num + i, output_dir)

    return start_chapter_num + len(chapters)

def save_chapter(content, chapter_num, output_dir):
    # 如果章节字数小于等于一万，直接保存
    if len(content) <= MAX_WORDS:
        output_file = os.path.join(output_dir, f'雪中悍刀行第{chapter_num:03d}章.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        # 按一万字分割章节
        part_num = 1
        start = 0
        while start < len(content):
            end = start + MAX_WORDS
            # 确保不截断中文字符
            while end < len(content) and not content[end].isspace():
                end -= 1
            # 保存分割后的部分
            output_file = os.path.join(output_dir, 
                                     f'雪中悍刀行第{chapter_num:03d}章_{part_num}.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content[start:end])
            start = end
            part_num += 1

if __name__ == '__main__':
    # 输入和输出目录
    input_dir = 'txt'
    output_dir = 'split_txt'

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 初始化章节编号
    current_chapter_num = 1

    # 处理所有txt文件
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_dir, file_name)
            current_chapter_num = split_novel_by_chapter(file_path, output_dir, current_chapter_num)