import json, requests

BASE_URL = 'https://www.instagram.com/accounts/login/'
LOGIN_URL = BASE_URL + 'ajax/'

def login():
    ''' 세션 생성 '''
    s=requests.session()
    s.headers['Referer'] = "https://www.instagram.com/"
    s.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"

    ''' 인스타그램 로그인'''
    try:
        ''' 로그인 페이지 '''
        s.get(BASE_URL)

        ''' 아이디, 비밀번호 입력 '''
        payload = {
            'username':'username',
            'enc_password':'enc_passwrd',
            'queryParams':'{}',
            'optIntoOneTap':'false'
        }

        ''' csrftoken '''
        s.headers.update({'X-CSRFToken':s.cookies['csrftoken']})

        ''' 로그인 '''
        s.post(LOGIN_URL, payload,allow_redirects=True)

    except Exception as e: # connection error
        print(f'로그인 오류\n{e}')
        return False

    else:
        try:
            if s.cookies['ds_user_id']: # ds_user_id 값이 있으면 로그인 성공
                print('login success.')
                return True

        except:
            print('login fail.')
            return False


if __name__ == "__main__":
    login()
