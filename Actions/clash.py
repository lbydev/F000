import requests
import os
def fetch_and_process_content(url):
    """从给定的URL下载内容，去掉以',reject'结尾的部分，并返回处理后的行。"""
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data: HTTP", response.status_code)
        return []
    lines = response.text.strip().split('\n')
    processed_lines = [line.replace(',reject', '') for line in lines if line.endswith(',reject')]
    return processed_lines
def save_content_to_file(content, filename):
    """将处理后的内容保存到规定的文件中。"""
    directory = 'rule-list'
    # 确保目录存在
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    # 写入文件
    with open(path, 'w') as file:
        for line in content:
            file.write(line + '\n')
def process_url(url):
    """处理给定的URL并保存结果。"""
    filename = os.path.splitext(os.path.basename(url))[0] + '.list'
    content = fetch_and_process_content(url)
    save_content_to_file(content, filename)
# 示例使用
url = 'https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list'
process_url(url)