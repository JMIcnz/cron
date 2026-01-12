import os
import requests
import resend

# Free plan does not support this API entrypoint
# https://api.exchangeratesapi.io/v1/convert?access_key=17bc7e3c87a43e7e8ccd3f2d8b742a82&from=NZD&to=CNY&amount=100

# The name must match the environment variable name defined in the .yml file of Github Actions
ACCESS_KEY = os.environ.get("ACCESS_KEY")

if ACCESS_KEY is not None:
    print("API Token successfully loaded.")
else:
    print("API Token not found!")

# Note: GitHub automatically redacts secrets from logs, but you should avoid 
# printing the raw secret value directly to the console as a security best practice.

api_url = "https://api.exchangeratesapi.io/v1/latest?access_key=ACCESS_KEY&format=1"
response = requests.get(api_url)

targetrate = "4.28"
targetratefloat = float(targetrate)

if response.status_code==200:
  responsebody = response.json()
  latesrates = responsebody['rates']
  eur2nzd = latesrates['NZD']
  print(f"EUR to NZD: {eur2nzd}")
  eur2cny = latesrates['CNY']
  print(f"EUR to CNY: {eur2cny}")

  nzd2cnyfloat = float(eur2cny) / float(eur2nzd)
  #nzd2cny = str(nzd2cnyfloat)
  print(f"NZD to CNY: {nzd2cnyfloat}")

else:
    print(f"Failed to retrieve latest forex data. Status code: {response.status_code}")

if nzd2cnyfloat > targetratefloat:
  print("haha, time to trade!")
  # email me

  #email me
  RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
  resend.api_key = RESEND_API_KEY
  #resend.ApiKeys.list()

  print("see if it comes here line 37")

  params = {
    "from": "onboarding@resend.dev",
    "to": ["szjme@outlook.com"],
    "subject": "Good Forex Rate, Trade Now!",
    "html": "<strong>It Reaches the Target Rate, Time to Do Trading.</strong>"
  }

  print(params)

  email = resend.Emails.send(params)
  print(email)

else:
  print("keep waiting, be patient.")



#def check_forex_rate(fromcurrency, tocurrency, targetrate):


#if __name__ == "__main__":
#    check_forex_rate(FROM_CURRENCY, TO_CURRENCY, TARGET_RATE)


# cron to trigger this python app
# https://developers.cloudflare.com/changelog/2025-04-22-python-worker-cron-triggers/
