import os
import sys

import pandas as pd

from styleframe import StyleFrame, Styler, utils

from env_variable import UPLOAD_FOLDER, REPORT_FOLDER

sys.path.append(os.path.abspath(os.path.curdir))


def tax_transaction_csv_df(csv_file):
    """
    과세거래 내역 DataFrame
    :param csv_file: 과세거래 내역 CSV
    :return: DataFrame
    """
    return pd.read_csv(csv_file, encoding='CP949').dropna(axis=0, how='all')


def tax_transaction_to_report(tax_tr_df):
    """
    양도세 양식 col 에 맞춘 DataFrame
    :param tax_tr_df: 과세거래 DataFrame
    :return: DataFrame
    """
    tax_tr_trades = list()
    for idx, row in tax_tr_df.iterrows():
        # 주식 종목명
        stock_name = row['종목명']
        # 양도주식 수
        sell_number = int(row['매도수량'])
        # 주식등 종류 61 고정
        stock_type = 61
        # 취득유형 1 고정
        obtain_type = "01"
        # 양도일자
        hand_over_date = row['매도결제일']
        # 주당양도가액
        ho_per_price = row['매도단가']
        # 양도가액
        ho_total_price = int(row['매도금액(원)'])
        # 취득일자
        obtain_date = row['매수결제일']
        # 주당취득가액
        o_per_price = row['매수단가']
        # 취득가액
        o_total_price = int(row['매수금액(원)'])
        # 필요경비
        trade_tax = int(row['필요경비(원)'])
        # ISIN 코드
        isin_code = row['표준종목번호']
        # 국외자산국가코드 'US' 고정
        # TODO: 다른 국가 고려
        nation_code = 'US'
        row = [stock_name, sell_number, stock_type, obtain_type,
               hand_over_date, ho_per_price, ho_total_price,
               obtain_date, o_per_price, o_total_price, trade_tax,
               isin_code, nation_code
               ]
        tax_tr_trades.append(row)
    # 양도세 header columns
    report_cols = ['주식 종목명', '취득유형별 양도주식 수', '주식등 종류', '취득유형',
                   '양도일자', '주당양도가액', '양도가액',
                   '취득일자', '주당취득가액', '취득가액', '필요경비',
                   '국제증권식별번호 (ISIN코드)', '국외자산국가코드'
                   ]
    return pd.DataFrame(tax_tr_trades, columns=report_cols)


def tax_report_xlsx_df(xlsx_file):
    """
    양도세 신고서 header 포함된 DataFrame
    :param xlsx_file: 신고서 XLSX
    :return: DataFrame
    """
    report = pd.read_excel(xlsx_file, sheet_name='자료', engine="openpyxl")
    report.columns = report.columns.str.replace(r'[\n\s]+', ' ')
    report.dropna(subset=["주식 종목명"], inplace=True)
    return report


def tax_report_w_trades_df(xlsx_file, tax_tr_trades):
    """
    과세거래 내역 포함된 신고서 내용 DataFrame
    :param xlsx_file: 신고서 XLSX
    :param tax_tr_trades: 과세거래 내역 DataFrame
    :return: DataFrame
    """
    tax_report_head = tax_report_xlsx_df(xlsx_file)
    tax_report = pd.concat([tax_report_head, tax_tr_trades])
    return tax_report


def write_tax_report_xlsx(xlsx_file, csv_file, tax_report_df):
    report_template = StyleFrame.read_excel_as_template(xlsx_file, tax_report_df, sheet_name='자료', engine="openpyxl")
    report_p2_info = StyleFrame.read_excel(xlsx_file, sheet_name='작성안내', read_style=True, engine="openpyxl")
    report_p3_tax_code = StyleFrame.read_excel(xlsx_file, sheet_name='양도물건종류별 세율코드', read_style=True, engine="openpyxl")
    report_p4_stock_type = StyleFrame.read_excel(xlsx_file, sheet_name='양도물건종류별 주식등종류', read_style=True, engine="openpyxl")

    report_template.apply_column_style(cols_to_style=['양도일자', '취득일자'],
                                       styler_obj=Styler(number_format=utils.number_formats.date))
    report_template.apply_column_style(cols_to_style=['양도가액', '취득가액', '필요경비'],
                                       styler_obj=Styler(number_format=utils.number_formats.thousands_comma_sep))

    # 양도세 시트 저장
    report_filename = os.path.join(REPORT_FOLDER, f'Treport_{csv_file.split(".")[0]}.xlsx')
    # report_filename = f'Treport_{csv_file.split(".")[0]}.xlsx'
    report_writer = StyleFrame.ExcelWriter(report_filename)
    report_template.to_excel(excel_writer=report_writer, sheet_name='자료')
    report_p2_info.to_excel(excel_writer=report_writer, sheet_name='작성안내')
    report_p3_tax_code.to_excel(excel_writer=report_writer, sheet_name='양도물건종류별 세율코드')
    report_p4_stock_type.to_excel(excel_writer=report_writer, sheet_name='양도물건종류별 주식등종류')
    # 양도세 신고서 파일 저장
    report_writer.save()

    # 양도세 신고서 파일명 변환
    return report_filename


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='---Treport---\n 해외주식 거래 양도소득세 신고서 작성기')
    # parser.add_argument('--trade', '-t', type=str, help='과세거래 내역서 파일\n ex: 미래에셋대우_과세거래.csv')
    # parser.add_argument('--report', '-r', type=str, help='양도소득세 신고서 양식 파일\n ex: 미래에셋대우_양도세_신고서.xlsx')
    #
    # args = parser.parse_args()
    #
    # trade_csv = args.trade
    # report_xlsx = args.report

    trade_csv = input('과세거래 CSV 파일\n> ')
    report_xlsx = input('양도세 신고서 XLSX 파일\n> ')

    trade_csv_df = tax_transaction_csv_df(trade_csv)
    trade_df = tax_transaction_to_report(trade_csv_df)

    report_df = tax_report_w_trades_df(report_xlsx, trade_df)
    write_tax_report_xlsx(report_xlsx, report_df)
