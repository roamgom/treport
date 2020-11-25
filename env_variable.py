import os

SECRET_KEY = "hola"
PATH = os.getcwd()
UPLOAD_FOLDER = os.path.join(PATH, 'uploads')
REPORT_FOLDER = os.path.join(PATH, 'reports')

# 양도세 신고서 xlsx 파일
TEMPLATE_XLSX = 'tax_report_template.xlsx'


def setup():
    print("Setting up environments...")
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)
    print("Done!")


if __name__ == '__main__':
    setup()
