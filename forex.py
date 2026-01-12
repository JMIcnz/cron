import os
import requests
import resend

# Free plan does not support this API entrypoint
# https://api.exchangeratesapi.io/v1/convert?access_key=17bc7e3c87a43e7e8ccd3f2d8b742a82&from=NZD&to=CNY&amount=100

# The name must match the environment variable name defined in the .yml file of Github Actions
ACCESS_KEY = os.environ.get("ACCESS_KEY")

if ACCESS_KEY is not None:
    print("Exchange Rate Access Key successfully loaded.")
else:
    print("Exchange Rate Access Key not found!")

# Note: GitHub automatically redacts secrets from logs, but you should avoid 
# printing the raw secret value directly to the console as a security best practice.

api_url = "https://api.exchangeratesapi.io/v1/latest?access_key=" + ACCESS_KEY + "&format=1"
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
  nzd2cny = str(nzd2cnyfloat)
  print(f"NZD to CNY: {nzd2cnyfloat}")

else:
    print(f"Failed to retrieve latest forex data. Status code: {response.status_code}")

if nzd2cnyfloat > targetratefloat:
  print("haha, time to trade!")

  #email me
  RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
  resend.api_key = RESEND_API_KEY
  #resend.ApiKeys.list()

  if RESEND_API_KEY is not None:
    print("Resend API Key successfully loaded.")
  else:
    print("Resend API Key not found!")

  params = {
    "from": "onboarding@resend.dev",
    "to": ["szjme@outlook.com","jade.mei@outlook.com","jade.mei@gmail.com","ark021810280@gmail.com"],
    "subject": "Good Forex Rate, " + nzd2cny + " Trade Now, Actiooooooooon!",
    "html": "<strong>It Reaches the Target Rate, Time to Do Trading.</strong>"
  }

  #print(params)

  email = resend.Emails.send(params)
  #print(email)
  print("Email sent.")

else:
  print("keep waiting, be patient.")
  RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
  resend.api_key = RESEND_API_KEY
  params = {
    "from": "onboarding@resend.dev",
    "to": ["szjme@outlook.com","ark021810280@gmail.com"],
    "subject": "Forex Rate is " + nzd2cny + ", Keep Waiting!",
    "html": "<strong>Forex Rate Not Good, Keep Waiting.</strong>"
  }
  email = resend.Emails.send(params)

#def check_forex_rate(fromcurrency, tocurrency, targetrate):


#if __name__ == "__main__":
#    check_forex_rate(FROM_CURRENCY, TO_CURRENCY, TARGET_RATE)


# cron to trigger this python app
# https://developers.cloudflare.com/changelog/2025-04-22-python-worker-cron-triggers/
