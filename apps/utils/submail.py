import requests
import json


appid = '42927'
appkey = '27e94f2c43e363dcce2c3095d7f5b5c5'
# 发送单条短信
def send_sms(appid, code, mobile, appkey):
    t = '60s'
    url = 'https://api.mysubmail.com/message/send'
    content = '【ITs-WHY】您的验证码是：{}，请在{}内输入'.format(code, t)
    res = requests.post(url, data={
        "appid": appid,
        "to":mobile,
        "signature":appkey,
        "content": content,
    })
    re_json = json.loads(res.text)
    return re_json

# 测试代码
if __name__ == '__main__':
    res = send_sms(appid, '123456', '15638534763', appkey)
    res_json = json.loads(res.text)
    status = res_json['status']
    if status == 'success':
        print('发送成功')
    else:
        msg = res_json['msg']
        print('{}'.format(msg))
    print(res.text)