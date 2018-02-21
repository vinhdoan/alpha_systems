import json
import requests

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/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'
slack_data = {'text': "Mua được TIS - 12.40"}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

#
# url = 'http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0908653000&Content=CallVietnam: 3752 is your verification code&ApiKey=1379D32BB315F672631578B6C9C724&SecretKey=EC064FDB3E4D27F06F2B12FDDD0052&SmsType=8'
# result = requests.get(url)
# print(result)