import requests

filename = 'mirae_과세거래_2020.csv'

with open(filename) as fp:
    content = fp.read()

response = requests.post(
    f'http://127.0.0.1:5000/uploader/{filename}', data=content
)

