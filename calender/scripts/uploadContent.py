import requests
import json
import argparse
from common import *
import os

"""
curl -XPOST "http://alpha-storage.worksmobile.com/openapi/message/upload.api" \
         -H "consumerKey:2NqRVHLwKJoyhMVweXFI" \
         -H "authorization: Bearer AAAA+UqCOwVLOdscB1a6o7FfTGl+VDzbXCcs35Ktxo"
         "L+zsB/iqp4Egfa/4LOnh9t8+Omb1ddnTRyNG8J+sYoEYlIBmle9iKzgVQ2vWvczn5a7"
         "Wt5aTAc6YnhdJTKt4PjIvDLAueat8VF1CKm4yK1qHpLGp5q47WFqBZqcTJ9Z6u4Xm7G"
         "mBo/SeSG6Q9c/6DbqE73M4hxlkdNjjduJEk2Gh8+Fedu0XnY26W9p5+CzzHieE4HdsG"
         "FR9uZ16xodc9OoBRSJCkA6bki0E45zfOdkjvE1tAhzYbghgD1vU0nDQwKBM28QhHd70"
         "uEbYI6hhYp9I9m3PJzA13ZJ3Xl4q1F1mygfaI=" \
         -H "x-works-apiid:kr1xbFflHaxsx" \
         -F "resourceName=@../image/Rich_Menu.png" -i
"""


def upload_resource_by_file(file_path, storage_domain):
    headers = {
        "consumerKey": CONSUMER_KEY,
        "authorization": "Bearer " + TOKEN,
        "x-works-apiid": API_ID
    }

    files = {
        "resourceName": open(file_path, 'rb')
    }

    url = "http://" + storage_domain + "/openapi/message/upload.api"
    r = requests.post(url, files=files, headers=headers)
    if r.status_code != 200:
        print(r.text)
        print(r.content)
        return None
    if "x-works-resource-id" not in r.headers:
        print(r.headers)
        print(r.text)
        print(r.content)
        return None
    return r.headers["x-works-resource-id"]


def upload_resource_by_locals(file_path, storage_domain):

    resource_id = {}
    carousel_one_path = file_path + "/IMG_Carousel_01.png"
    if os.path.exists(carousel_one_path):
        resource_id["carouselone"] = \
            upload_resource_by_file(carousel_one_path, storage_domain)

    carousel_two_path = file_path + "/IMG_Carousel_02.png"
    if os.path.exists(carousel_two_path):
        resource_id["carouseltwo"] = \
            upload_resource_by_file(carousel_two_path, storage_domain)

    carousel_three_path = file_path + "/IMG_Carousel_03.png"
    if os.path.exists(carousel_three_path):
        resource_id["carouselthree"] = \
            upload_resource_by_file(carousel_three_path, storage_domain)

    rich_menu_path = file_path + "/Rich_Menu.png"
    if os.path.exists(rich_menu_path):
        resource_id["richmenu"] = \
            upload_resource_by_file(rich_menu_path, storage_domain)

    print(file_path)
    print(resource_id)
    return resource_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch Register')
    parser.add_argument('--env', type=str, default="alpha",
                        help='run environment? [alpha|stage|real]')
    parser.add_argument('--update', type=str, default="none",
                        help='Is the update config? [update|none]')
    args = parser.parse_args()
    env = args.env
    storage_domain = "alpha-storage.worksmobile.com"
    if env == "stage":
        storage_domain = "stage-storage.worksmobile.com"
    elif env == "real":
        storage_domain = "storage.worksmobile.com"

    root_path = ABSDIR_OF_PARENT + "/image/"
    resources = {}
    kr_path = root_path + "kr"
    if os.path.exists(kr_path):
        resources["kr"] = upload_resource_by_locals(kr_path, storage_domain)

    jp_path = root_path + "jp"
    if os.path.exists(kr_path):
        resources["jp"] = upload_resource_by_locals(jp_path, storage_domain)

    en_path = root_path + "en"
    if os.path.exists(kr_path):
        resources["en"] = upload_resource_by_locals(en_path, storage_domain)

    if args.update == "update":
        root_path = ABSDIR_OF_PARENT + "/calender/constants/"
        read_lines = None
        if os.path.exists(root_path + "value.py"):
            with open(root_path + "value.py", "r+") as A:
                read_lines = A.readlines()
        else:
            with open(root_path + "value.py_template", "r+") as A:
                read_lines = A.readlines()
        write_lines = []
        for line in read_lines:
            sub_lines = line.split(" ")
            if len(sub_lines) < 2:
                write_lines.append(line)
                continue
            const_name = sub_lines[0]
            sub_names = const_name.split("_")
            if len(sub_names) < 3:
                write_lines.append(line)
                continue
            resource_type = sub_names[0].lower()
            local = sub_names[1].lower()

            res_local = resources.get(local, None)
            if res_local is not None:
                res_type = res_local.get(resource_type, None)
                if res_type is not None:
                    pos = line.find("=")
                    line = line[:pos+1] + " \"" \
                           + resources[local][resource_type] + "\" \n"
            write_lines.append(line)
        with open(root_path + "value.py", "w") as A:
            A.writelines(write_lines)
    print(resources)
