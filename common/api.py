if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from api_config import API_URL
from configs.tistory_convert_config import TistoryConverterConfig as Config
import requests
from http import HTTPStatus
from widgets.auth_message_widget import QuitMessage


def token_auth_check():
    print("token_auth_check")
    # 컴퓨터 로컬 안에 license_key와 token을 이용하여 토큰 유효성여부를 체크한다.
    config = Config()
    saved_data = config.get_saved_data()
    auth_result = dict(result=False, error="")
    url = f"{API_URL}/token/"
    try:
        datas = {"license_key": saved_data.license_key, "token": saved_data.token}
        response = requests.post(url, json=datas, timeout=5)

        if HTTPStatus.OK == response.status_code:
            auth_result.update({"result": True})
        elif HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code:
            auth_result.update({"error": "서버에 오류가 발생하였습니다. 관리자에게 문의해주세요."})
        else:
            data = response.json()
            error = data["error"]
            auth_result.update({"result": False, "error": error})

    except Exception as e:
        print(e)
        raise Exception(e)

    if auth_result["result"] == False:
        # QuitMessage(3)
        QuitMessage(10)

    return auth_result


if __name__ == "__main__":
    token_auth_check()
