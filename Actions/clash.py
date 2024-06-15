import requests
import os

def process_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        processed_lines = []
        for line in lines:
            original_line = line.strip()
            if original_line and not original_line.startswith('#') and not original_line.startswith('PROCESS-NAME,'):
                # Handling IP range lines or mapping using dictionary
                if is_ip_range(original_line) and not starts_with_ip_prefix(original_line):
                    new_line = handle_ip_range(original_line)
                else:
                    new_line = original_line
                # Apply general mappings and append filename
                modified_line = map_line(new_line, filename)
                appley_modified_line = handle_ip_noresolve(modified_line,os.path.splitext(filename)[0])
                processed_lines.append(appley_modified_line)
        return processed_lines
    else:
        return None

def is_ip_range(line):
    return '/' in line and line.split('/')[1].isdigit()

def starts_with_ip_prefix(line):
    return line.startswith("IP-CIDR,") or line.startswith("IP-CIDR6,")


def handle_ip_range(line):
    return f"IP-CIDR,{line}"

def handle_ip_noresolve(line, base_filename):
    if ",no-resolve" in line:
        ip_part, _ = line.split(",no-resolve", 1)
        return f"{ip_part},{base_filename}"
    return f"{line}"

def map_line(line, filename):
    line_without_suffix = line.split(',')[0]
    for key in MAP_DICT:
        if line_without_suffix.startswith(key):
            line_mapped = line.replace(key, MAP_DICT[key])
            return f"{line_mapped},{os.path.splitext(filename)[0]}"
    if line_without_suffix.startswith('+.'):
        return line.replace('+.', 'HOST-SUFFIX,') + f",{os.path.splitext(filename)[0]}"
    return f"HOST,{line}" + f",{os.path.splitext(filename)[0]}"

def write_to_file(url, processed_content):
    parts = url.split('/')
    parent_dir = parts[-2]
    directory = os.path.join('QuantumultX', parent_dir)
    os.makedirs(directory, exist_ok=True)
    filename = os.path.splitext(os.path.basename(url))[0] + '.list'
    path = os.path.join(directory, filename)
    
    with open(path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_content))

# Mapping dictionary
MAP_DICT = {
    'DOMAIN-SUFFIX': 'HOST-SUFFIX',
    'DOMAIN': 'HOST',
    'DOMAIN-KEYWORD': 'HOST-KEYWORD',
    'IP-CIDR': 'IP-CIDR',
    'IP-CIDR6': 'IP6-CIDR',
    'GEOIP': 'GEOIP',
    'IP-ASN': 'IP-ASN',
    'USER-AGENT': 'USER-AGENT'
}

# URLs to process
urls = [
    "https://ruleset.skk.moe/Clash/domainset/apple_cdn.txt",
    "https://ruleset.skk.moe/Clash/domainset/cdn.txt",
    "https://ruleset.skk.moe/Clash/domainset/download.txt",
    "https://ruleset.skk.moe/Clash/domainset/icloud_private_relay.txt",
    "https://ruleset.skk.moe/Clash/domainset/reject.txt",
    "https://ruleset.skk.moe/Clash/domainset/speedtest.txt",
    "https://ruleset.skk.moe/Clash/domainset/steam.txt",
    "https://ruleset.skk.moe/Clash/non_ip/ai.txt",
    "https://ruleset.skk.moe/Clash/non_ip/apple_cdn.txt",
    "https://ruleset.skk.moe/Clash/non_ip/apple_cn.txt",
    "https://ruleset.skk.moe/Clash/non_ip/cdn.txt",
    "https://ruleset.skk.moe/Clash/non_ip/direct.txt",
    "https://ruleset.skk.moe/Clash/non_ip/domestic.txt",
    "https://ruleset.skk.moe/Clash/non_ip/download.txt",
    "https://ruleset.skk.moe/Clash/non_ip/global.txt",
    "https://ruleset.skk.moe/Clash/non_ip/lan.txt",
    "https://ruleset.skk.moe/Clash/non_ip/microsoft_cdn.txt",
    "https://ruleset.skk.moe/Clash/non_ip/microsoft.txt",
    "https://ruleset.skk.moe/Clash/non_ip/apple_services.txt",
    "https://ruleset.skk.moe/Clash/non_ip/stream.txt",
    "https://ruleset.skk.moe/Clash/non_ip/stream_us.txt",
    "https://ruleset.skk.moe/Clash/non_ip/telegram.txt",
    "https://ruleset.skk.moe/Clash/ip/cdn.txt",
    "https://ruleset.skk.moe/Clash/ip/china_ip.txt",
    "https://ruleset.skk.moe/Clash/ip/domestic.txt",
    "https://ruleset.skk.moe/Clash/ip/download.txt",
    "https://ruleset.skk.moe/Clash/ip/lan.txt",
    "https://ruleset.skk.moe/Clash/ip/stream.txt",
    "https://ruleset.skk.moe/Clash/ip/stream_us.txt",
    "https://ruleset.skk.moe/Clash/ip/telegram_asn.txt",
    "https://ruleset.skk.moe/Clash/ip/telegram.txt",
    "https://ruleset.skk.moe/Clash/ip/reject.txt",
]

for url in urls:
    filename = os.path.basename(url)
    processed_content = process_file(url, filename)
    if processed_content is not None:
        write_to_file(url, processed_content)
