import HCaptcha
from HCaptcha import *
import random
import requests
import json
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url_fingerprint = 'https://discord.com/api/v9/auth/fingerprint' # Get the fingerprint

response = requests.post(url_fingerprint)
fingerprint = json.loads(response.text)['fingerprint']
response = data = {
  'captcha_key': HCaptcha.Solver(host="http://discord.com/", sitekey="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34").solve(), #Solve the captcha
  'consent': 'true',
  'date_of_birth': f"2000-04-20",
  'email': random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + '@' + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") + random.choice("abcdefghijklmnopqrstuvwxyz1234567890") +  '.' + random.choice("abcdefghijklmnopqrstuvwxyz") + random.choice("abcdefghijklmnopqrstuvwxyz") + random.choice("abcdefghijklmnopqrstuvwxyz"),
  'fingerprint': fingerprint,
  'gift_code_sku_id': 'null',
  'invite': 'skid', # ENTER YOUR INVITE HERE
  'password': "4567uhgTUHGTUY%^&",
  'username':  "Piggy",
}

response = requests.post("https://discord.com/api/v9/auth/register", headers=headers, json=data, ) # Send the register request
print(response.text)