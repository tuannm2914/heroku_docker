import os
import sys
import cv2
import time
import json
import base64
import requests


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string


def get_rs(image_path):
    url = "http://127.0.0.1:8080/api/uet"
    image_base64 = image_to_base64(image_path)
    data = {"image": image_base64, "type_text": "printed"}

    result = ""

    try:
        response = requests.post(url=url, data=json.dumps(data), timeout=10).json()
       
        result = response['text']
    except requests.Timeout:
        sys.stderr.write("request timeout for %s\n" % image_path)
    except requests.ConnectionError:
        sys.stderr.write("connection error\n")
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        sys.stderr.write("request error for %s\n" % image_path)
        

    return result

def process(test_dirs, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    total_img, total_time = 0, 0
    for test_dir in test_dirs:
        for image_name in os.listdir(test_dir):
            if not image_name.endswith(".xml"):
                image_path = os.path.join(test_dir, image_name)
                output_path = os.path.join(output_dir, image_name)

                start = time.time()
                figure, formula = get_boxes(image_path)
                total_time += time.time() - start
                total_img += 1
                
                all_boxes = figure + formula
                draw_rect(image_path, all_boxes, output_path)

    print('Avg. Time: %.2f' % (total_time / total_img if total_img > 0 else 0))


def test():
    image_path = "test1.png"
    rs = get_rs(image_path)
    print(rs)


test()
exit()
"""
if len(sys.argv) != 3:
    sys.stderr.write("test_dirs output_dir\n")
    exit(1)

test_dirs = sys.argv[1].split(',')
output_dir = sys.argv[2]

if any([test_dir == output_dir for test_dir in test_dirs]):
    sys.stderr.write("one of test dir paths != output dir path\n")
    exit(1)

process(test_dirs, output_dir)
"""
