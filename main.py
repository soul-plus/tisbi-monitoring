import json
import csv
import requests
import secrets


def add_zero(string):
    if len(string) == 1:
        string = "0" + string
    return string


if __name__ == '__main__':
    path = "C:/Users/program.KAZGIK/Desktop/fd/даuнные.csv"
    with open(path, mode='r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        lst = list(reader)

        result_list = []
        dict_keys = list(lst[0].keys())
        student_keys = dict_keys[:6]
        group_key = dict_keys[6:]

        for item in lst:
            item['birth_month'] = add_zero(item['birth_month'])
            item['birth_day'] = add_zero(item['birth_day'])

            student_dict = {key: int(item[key]) if key in ('id', 'orphan') else item[key] for key in student_keys}
            group_dict = {key: int(item[key]) if key != 'title' else item[key] for key in group_key}
            replacement = {"vpo_group_id": "id"}
            for k, v in list(group_dict.items()):
                group_dict[replacement.get(k, k)] = group_dict.pop(k)
            student_dict['secret'] = secrets.token
            student_dict['vpo_group'] = group_dict

            result_list.append(student_dict)

        res_list = []
        for item in result_list:
            result = json.dumps(item)
            print(result)
            r = requests.post("https://test-edu.ru/get-link", data=result, verify=False)
            print(r.status_code, r.reason)
            response = r.json()
            status_code = r.status_code
            # status_code = 200
            # response = {'code': 0, 'url': '(url для прохождения тестирования)'}

            if status_code == 200:
                id_dict = {key: value for key, value in item.items() if key in ('id')}
                res_dict = {**id_dict, **response}
                res_str = "UPDATE `testirovanie` SET `link`='%s' WHERE `id_mmis` = '%s';\n" \
                          % (res_dict['url'], res_dict['id'])
                res_list.append(res_str)
            else:
                res_list.append(response)
            print(res_list)

        path = "C:/Users/program.KAZGIK/Desktop/fd/result_testlinks.txt"
        with open(path, mode='w', encoding="utf-8") as res_file:
            for item in res_list:
                res_file.write(str(item))