import requests
from typing import List, Optional
import os

def process_file(url: str, rule_set_name: str) -> Optional[List[str]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        rule_type_map = {
            'DOMAIN-SUFFIX': 'HOST-SUFFIX',
            'DOMAIN': 'HOST',
            'DOMAIN-KEYWORD': 'HOST-KEYWORD',
            'IP-CIDR': 'IP-CIDR',
            'IP-CIDR6': 'IP-CIDR6',
            'SRC-IP-CIDR': 'SRC-IP-CIDR',
            'GEOIP': 'GEOIP',
            'DST-PORT': 'DST-PORT',
            'SRC-PORT': 'SRC-PORT'
        }

        processed_lines = []
        for line in response.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(',')
            if len(parts) >= 2:
                rule_type = parts[0]
                if rule_type in rule_type_map:
                    new_rule_type = rule_type_map[rule_type]
                    if new_rule_type in ['IP-CIDR', 'IP-CIDR6'] and parts[-1] == 'no-resolve':
                        parts = parts[:-1]
                    processed_line = f"{new_rule_type},{parts[1]},{rule_set_name}"
                    processed_lines.append(processed_line)
            else:
                if line.startswith('+.'):
                    processed_line = f"HOST-SUFFIX,{line[2:]},{rule_set_name}"
                    processed_lines.append(processed_line)
                elif ',' not in line:
                    processed_line = f"HOST,{line},{rule_set_name}"
                    processed_lines.append(processed_line)

        return processed_lines
    except requests.RequestException:
        return None

def write_to_file(filename: str, processed_content: List[str]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(f"{line}\n" for line in processed_content)

def main():
    urls = {
        "ai": ("https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/non_ip/ai.txt",
                   "./QuantumultX/non_ip/ai.list"),
        "telegram_asn": ("https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/ip/telegram_asn.txt",
                "./QuantumultX/ip/telegram_asn.list"),
        "telegram": ("https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/ip/telegram.txt",
                      "./QuantumultX/ip/telegram.list")
    }

    for rule_set_name, (url, output_file) in urls.items():
        processed_content = process_file(url, rule_set_name)
        if processed_content:
            write_to_file(output_file, processed_content)
        else:
            print(f"Failed to process {rule_set_name} from {url}")

if __name__ == "__main__":
    main()