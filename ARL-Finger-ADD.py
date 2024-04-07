import json

Ehole_list = []
FingerprintHub_list = []


def return_data():
    data = {
        "name": "",
        "rule": ""
    }

    return data


def Ehole():
    with open("./finger/finger.json", "r", encoding="utf-8") as file:
        # 去除非法字符
        content = file.read().replace('\xa0', '')
        load_dict = json.loads(content)

    for finger_json in load_dict['fingerprint']:
        temp_list = []
        data = return_data()
        data['name'] = finger_json['cms']
        if finger_json['method'] == "keyword" and finger_json['location'] == "body":
            for rule in finger_json['keyword']:
                rule = rule.replace('"', r'\"')
                temp_list.append(f'body="{rule}"')

        elif finger_json['method'] == "faviconhash":
            for rule in finger_json['keyword']:
                temp_list.append(f'icon_hash="{rule}"')

        elif finger_json['location'] == "title":
            for rule in finger_json['keyword']:
                temp_list.append(f'title="{rule}"')

        elif finger_json['location'] == "header":
            for rule in finger_json['keyword']:
                rule = rule.replace('"', r'\"')
                temp_list.append(f'header="{rule}"')

        else:
            raise Exception('未找到匹配条目！')

        data['rule'] = ' && '.join(temp_list)
        Ehole_list.append(data)

    # 写入处理好的json
    with open('EHole_ARL_finger.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(Ehole_list, ensure_ascii=False, indent=2))


def FingerprintHub():
    with open("./finger/web_fingerprint_v2.json", "r", encoding="utf-8") as file:
        content = file.read()
        load_dict = json.loads(content)

    for finger_json in load_dict:
        temp_list = []
        data = return_data()
        if finger_json['request_method'] != 'get':
            continue

        data['name'] = finger_json['name']
        for key, value in finger_json['headers'].items():
            value = value.replace('"', r'\"')
            temp_list.append(f'header="{key}: {value}"')

        for rule in finger_json['keyword']:
            # 手动转义双引号
            rule = rule.replace('"', r'\"')
            temp_list.append(f'body="{rule}"')

        data['rule'] = ' && '.join(temp_list)
        FingerprintHub_list.append(data)

    # 写入处理好的json
    with open('FingerprintHub_ARL_finger.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(FingerprintHub_list, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Ehole()
    FingerprintHub()

    print('[+] 处理完成，已输出文件至当前目录！')
