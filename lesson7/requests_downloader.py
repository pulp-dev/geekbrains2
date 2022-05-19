import requests


# r.headers['Content_Type']
def get_right_extension(content_type):
    return content_type.split('/')[1].split('+')[0]


def save_info_file(response):
    extension = get_right_extension(response.headers['Content-Type'])
    with open(f'image.{extension}', 'wb') as f:
        f.write(response.content)


URL = 'https://wildgeesetravel.files.wordpress.com/2017/09/barbuda-115-re.jpg'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79 "
}

r = requests.get(URL, headers=headers)
save_info_file(r)

print()
