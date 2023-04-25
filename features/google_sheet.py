if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt
import pandas as pd

# 500letsdothis@gmail.com
GOOGLE_SERVICE_KEY = {
    "type": "service_account",
    "project_id": "tistory-converter",
    "private_key_id": "0a83247c4468147172ab28fb0ade7a1218cd0498",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCluZWSkeJXxYQA\nUoZ4XWM4t4HDg0K+llAWt/cx7rNFqs7oVBQkR4Vo7JXJ9XXvNgZ3YOxaRSM1IShA\n66dXapYXVzx89j3EPM3isVvLCgL+MTL3UEdGSxXWZhwqKGLQQ5foB/tspvf2YiyJ\nTMz+KbhH4aPnPcRU/2llk30A7wNVtM8Am6/tyA4jGDw6740Db9nx+vjQFHfypRPN\npCqT3zB2L+j9k1ex6mdQyeJeOONVTybDibZgwlXNcCCktarGqwMN97/UO1P7JQKg\n6bVDbRQ3eUa/xFSfL4dIWoHdQBfDwl/WOzLIeD0dRXK5sQH9kyLWqw80xVR0CgpF\nnUVZY93bAgMBAAECggEABFtpPHfma1szzxQYGW/2DOSFayqZZZkJGQJ6lsq4K7B/\nhNjKYuiYeLMH7UV6IEJGMmGgRSsrCPdkTT0vhJ9pu8pdIOybOh6aMjJ7dyx52CKO\nARxdPo5wNnDrjcdCgp1MVFslXlMGrKSZyxa3ywGtD0cDDMnotNK2Yk3q4VT4b4IC\nikutGt8G/dxis0dir1/FApwEu2iqA6Pc1BWC06LmUu8DDQfVLksnMzDenX4bgX6Y\nd6znjoRLWrURBCSXP8R86bhyxI5GTYxKPlVqZUmptjndTgjmT8N9i1SL9Ak1OO2S\nkLqQ0KryBYRgC/GfT021FDqfK1z6O2JaL4xlFT/N+QKBgQDf+48AqVgrsrplSB+x\nFcKDDkSXg8yecU8knax4HEkRVDi4BzjZApn0cQ46CTRHUmRn5UFWME0WJXkGIFL6\nEFNrGwpkHulAd7W2sfXdgZ/qzKlhpdTZRxW+FfntMNNkpcnIzzxrt/cXYTI/OfUJ\nhMllU3azJahebW3Mm/Y/YUAW2QKBgQC9aiM+Q4+ESeEK0QDYQTU2uJyIHx6MGM/A\nN0B1MAxpxZsd1t4uKHorauhup+ec26S1OuYUHZnmyHw6eWjjFeAeAxP+lfCvtkxM\na5GPl/Q1GM1W/T/5FDERBRkMmJm9L2UNAryFenljbwEsqqhEOfpSbxZbiUtd4rT8\n8Xi7hs2x0wKBgF+a+xFnN3F/mrx8qrpl9V8HihO6eG7xIr0YaHPkbvPspUE4I/XN\nfHWwhEgVgbEn5B/M5bSqbV0UpbINvh1rNpAzPJ4764hPEMto7u+b0uzgazR5Gn+c\nLhWzP7kU7Ea71YPXoYzBO8FJBa+jR4rGmUic9b/GRTX5M7Lwp42qLzcRAoGBAKqA\nTQMyK5EIM8PZySng4LbGTVkWsheoCfJbifEy9CmOEAg3Lz5bf0Vv8ZQSHiILcOMW\nBp+a2bttQq4cNbccLOa3HJtxevugXGP5/EhGnzPghI5GXvymGVjZvuegwdsTO6IP\nkYWRbo18EZGUeO0ZR2RGzNhO6QG1HfgGoQgk2ymzAoGBAIARQq7UJ8x1RmwGgXJS\nJoYNAd5jQahVHBiiNFBeLYjdW55V2ZRiXNLgeKIlLhRJy/8d2uU2bodX3iwmzgZ/\nnWZiQMMduvr9jgcpQBcDm+Km/6XaDTRpdN+oN9EugZeRS0ll+Z1690IvN9djoC6l\nMpykird2Lk7kXtpzcZ8SrKSV\n-----END PRIVATE KEY-----\n",
    "client_email": "tistory-converter@tistory-converter.iam.gserviceaccount.com",
    "client_id": "114004113594112861791",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tistory-converter%40tistory-converter.iam.gserviceaccount.com",
}


def get_gspread():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_DEVICE_URI = "https://oauth2.googleapis.com/device/code"
    GOOGLE_TOKEN_INFO_URI = "https://oauth2.googleapis.com/tokeninfo"
    GOOGLE_REVOKE_URI = "https://oauth2.googleapis.com/revoke"
    GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"

    creds_type = GOOGLE_SERVICE_KEY["type"]
    service_account_email = GOOGLE_SERVICE_KEY["client_email"]
    private_key_pkcs8_pem = GOOGLE_SERVICE_KEY["private_key"]
    private_key_id = GOOGLE_SERVICE_KEY["private_key_id"]
    client_id = GOOGLE_SERVICE_KEY["client_id"]

    signer = crypt.Signer.from_string(private_key_pkcs8_pem)

    credentials = ServiceAccountCredentials(
        service_account_email,
        signer,
        scopes=scopes,
        private_key_id=private_key_id,
        client_id=client_id,
        token_uri=GOOGLE_TOKEN_URI,
        revoke_uri=GOOGLE_REVOKE_URI,
    )
    credentials._private_key_pkcs8_pem = private_key_pkcs8_pem

    # 구글시트
    gc = gspread.authorize(credentials)

    return gc


def get_df_from_worksheet(url, sheetname):
    gc = get_gspread()
    # 스프레스시트 문서 가져오기
    spreadsheet = gc.open_by_url(url)
    worksheet = spreadsheet.worksheet(sheetname)
    # 시트 선택하기
    data = worksheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df = df.fillna("")
    return df


def get_dict_setting(url, sheetname):
    df_settings = get_df_from_worksheet(url, sheetname)
    df_settings = df_settings.fillna("")
    dict_settings = {}
    for index, row in df_settings.iterrows():
        key = str(row["Name"])
        value = str(row["Value"])
        dict_settings[key] = value
    return dict_settings


def login_sheet(login_id, login_pw):
    login_check = False

    try:
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HsrET3Ein4viLR_HZ6dZ2UpYTQG8TjNnLNqVSgklmCA/edit#gid=0"
        sheet_name = "티스토리변환"
        df_account = get_df_from_worksheet(spreadsheet_url, sheetname=sheet_name)
        df_success = df_account[
            (df_account["아이디"] == str(login_id)) & (df_account["비밀번호"] == str(login_pw))
        ]
        if len(df_success) > 0:
            login_check = True

    except Exception as e:
        login_check = False

    return login_check
