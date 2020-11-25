import os
import uuid

from flask import Flask, request, redirect, flash, abort, jsonify

from mirae_stock_report import (tax_transaction_csv_df, tax_transaction_to_report,
                                tax_report_w_trades_df, write_tax_report_xlsx)

from env_variable import SECRET_KEY, UPLOAD_FOLDER, TEMPLATE_XLSX, setup

app = Flask(__name__)

ALLOWED_FORMAT = set(['csv'])

# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config.update(
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    SECRET_KEY=SECRET_KEY
)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMAT


@app.route('/')
def hi():
    return 'yes'


@app.route('/uploader', methods=['POST'])
def upload_file():
    # .csv : 과세거래
    # .xlsx : 신고서 양식 -> 하나의 파일로 고정
    if 'file' not in request.files:
        message = jsonify({'message': 'No file in request'})
        message.status_code = 400
        return message
    file = request.files['file']
    if file.filename == '':
        message = jsonify({'message': 'No file selected for uploading'})
        message.status_code = 400
        return message
    if file and allowed_file(file.filename):
        filename = f'{uuid.uuid1()}.csv'

        # TODO: 파일 저장 에러예외 처리
        target_csv = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(target_csv)

        # 양도소득세 신고서 양식에 맞춰 처리
        target_trade_csv_df = tax_transaction_csv_df(target_csv)
        target_df = tax_transaction_to_report(target_trade_csv_df)
        report_df = tax_report_w_trades_df(TEMPLATE_XLSX, target_df)

        report_filename = write_tax_report_xlsx(TEMPLATE_XLSX, filename, report_df)

        message = jsonify({'message': report_filename})
        message.status_code = 201
        return message
    else:
        message = jsonify({'message': 'Allowed file type: *.csv'})
        message.status_code = 400
        return message


if __name__ == '__main__':
    setup()
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
