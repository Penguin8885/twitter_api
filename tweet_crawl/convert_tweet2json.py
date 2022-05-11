import sys, os
import re
import json

if __name__ == '__main__':
    crt_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = crt_dir + '/tweet.json'

    with open(json_path, 'rb') as f:
        data = json.load(f)

    map_list = []
    for datum in reversed(data):
        text = datum['full_text']
        text = re.sub('#.* ', '', text)
        text = re.sub('#.*$', '', text)
        user = datum['user']['name'] + '@' + datum['user']['screen_name']
        ts = datum['created_at']
        map_list.append({'time':ts, 'user':user, 'text':text})

    with open(crt_dir+'/formatted.json', 'w') as f:
        json.dump(map_list, f)
