import json
import sys
import wget
import tinder as ti
from pathlib2 import Path
import time
import requests


from facebooktoken import get_access_token

if __name__ == '__main__':

    credentials = json.load(open('credentials.json', 'r'))
    fb_id = credentials['FB_ID']
    fb_auth_token = get_access_token(credentials['FB_EMAIL_ADDRESS'], credentials['FB_PASSWORD'])

    print('FB_ID = {}'.format(fb_id))
    print('FB_AUTH_TOKEN = {}'.format(fb_auth_token))


    while True:
        token = ti.auth_token(fb_auth_token, fb_id)

        print('TINDER_TOKEN = {}'.format(token))

        if not token:
            print('could not get Tinder token. Program will exit.')
            sys.exit(0)

        print('Successfully connected to Tinder servers.')

        lat = 52.365
        lon = 4.926
        print(ti.change_loc(lat, lon, token))
        my_profile = ti.profile(token)
        print(json.dumps(my_profile, indent=4, sort_keys=True))

        for user in ti.recommendations(token):
            if not user:
                break

            count_photos = 1
            filename_paths = []
            for urls in user.d['photos']:
                directory = "data/" + str(user.age) + "/" + str(user.user_id) + "/"
                if Path(directory+'1.png').exists() and count_photos == 1:

                    break
                url = urls['url']
                filename_path = directory + str(count_photos) + ".png"
                count_photos += 1
                print(url, "=>", filename_path)
                wget.download(url, out=filename_path, bar=None)
                filename_paths.append(filename_path)

                # if action == 'like':
                #     like_count += 1
                #     print(' -> Like')
                #     stats(like_count, nope_count)
            time.sleep(1)
            try:
                match = ti.like(user.user_id)
            except requests.exceptions.ReadTimeout:
                print "Timeout occurred"

            if match:
                print(' -> Match!')
                # else:
                #     nope_count += 1
                #     print(' -> nope')
                #     stats(like_count, nope_count)
                #     ti.nope(user.user_id)
