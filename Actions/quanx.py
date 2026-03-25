import requests
import os
from typing import List, Optional, Tuple

def process_file(url: str, rule_set_name: str) -> Optional[List[str]]:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Clash to Quantumult X mapping
        rule_type_map = {
            'DOMAIN': 'HOST',
            'DOMAIN-SUFFIX': 'HOST-SUFFIX',
            'DOMAIN-KEYWORD': 'HOST-KEYWORD',
            'DOMAIN-WILDCARD': 'HOST-WILDCARD', # Correct mapping for QX
            'IP-CIDR': 'IP-CIDR',
            'IP-CIDR6': 'IP6-CIDR',
            'IP-ASN': 'IP-ASN',
            'GEOIP': 'GEOIP'
            # Removed DST-PORT, SRC-PORT, SRC-IP-CIDR as they are not natively supported as filter types in QX
        }

        processed_lines = []
        for line in response.text.splitlines():
            line = line.split('#')[0].strip()
            if not line:
                continue

            if ',' in line:
                parts = [p.strip() for p in line.split(',')]
                raw_type = parts[0].upper()
                if raw_type in rule_type_map:
                    new_type = rule_type_map[raw_type]
                    value = parts[1]
                    
                    # If somehow a standard HOST or HOST-SUFFIX contains wildcards, convert it to HOST-WILDCARD
                    if ('?' in value or '*' in value) and new_type in ['HOST', 'HOST-SUFFIX']:
                        new_type = 'HOST-WILDCARD'
                        
                    processed_lines.append(f"{new_type},{value},{rule_set_name}")
            else:
                # Handle domain-set (plain domains)
                if line.startswith('+.') or line.startswith('*.'):
                    domain = line[2:]
                    processed_lines.append(f"HOST-SUFFIX,{domain},{rule_set_name}")
                elif line.startswith('.'):
                    domain = line[1:]
                    processed_lines.append(f"HOST-SUFFIX,{domain},{rule_set_name}")
                else:
                    # Default plain domains to HOST-SUFFIX for better coverage (e.g. CDNs)
                    processed_lines.append(f"HOST-SUFFIX,{line},{rule_set_name}")
                    
        return list(dict.fromkeys(processed_lines))
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def write_to_file(filename: str, processed_content: List[str]) -> None:
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(f"{line}\n" for line in processed_content)

def main():
    tasks = [
        ("AI", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/non_ip/ai.txt", "./QuantumultX/non_ip/ai.list"),
        ("AI", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/non_ip/apple_intelligence.txt", "./QuantumultX/non_ip/apple_intelligence.list"),
        ("Telegram", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/non_ip/telegram.txt", "./QuantumultX/non_ip/telegram.list"),
        ("Telegram", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/Clash/ip/telegram.txt", "./QuantumultX/ip/telegram.list"),
        ("Apple_CDN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/domainset/apple_cdn.txt", "./QuantumultX/non_ip/apple_cdn.list"),
        ("Apple_Services", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/apple_services.txt", "./QuantumultX/non_ip/apple_services.list"),
        ("Apple_CN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/apple_cn.txt", "./QuantumultX/non_ip/apple_cn.list"),
        ("Microsoft_CDN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/microsoft_cdn.txt", "./QuantumultX/non_ip/microsoft_cdn.list"),
        ("Microsoft", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/microsoft.txt", "./QuantumultX/non_ip/microsoft.list"),
        ("LAN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/lan.txt", "./QuantumultX/non_ip/lan.list"),
        ("LAN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/ip/lan.txt", "./QuantumultX/ip/lan.list"),
        ("CDN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/domainset/cdn.txt", "./QuantumultX/non_ip/cdn_domainset.list"),
        ("CDN", "https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/refs/heads/master/Clash/non_ip/cdn.txt", "./QuantumultX/non_ip/cdn_non_ip.list")
    ]
    
    print("Starting processing tasks...")
    for policy, url, path in tasks:
        print(f"Fetching: {url}")
        content = process_file(url, policy)
        if content:
            write_to_file(path, content)
            print(f"Saved to: {path}")
        else:
            print(f"Failed to process: {url}")
    print("Tasks completed.")

if __name__ == "__main__":
    main()
