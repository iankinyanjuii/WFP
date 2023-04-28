import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime
import math

# Configuration
username = "hmu.user.four"
password = "7pHmWTfvYg9TuSy"

token = ""
countries_dict = { }
region_dict = {}
countries_insecure_dict = {}
countries_insecure_now_dict = {}

def get_token():
    url = "https://api.hungermapdata.org/swe-notifications/token"
    response = requests.post(url, auth=(username, password))
    global token
    token = response.json()["token"]
    
#Point to Note-Token Expires in 3 seconds
def call_api(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_population_dataframe():
    url = "https://api.hungermapdata.org/swe-notifications/population.csv"
    return pd.read_csv(url)

def get_food_insecure(days_ago):
    get_token()
    url = f"https://api.hungermapdata.org/swe-notifications/foodsecurity?days_ago={days_ago}"
    response = call_api(url, token)
    if "error" in response:
        print("Token expired. Retrying")
        get_token()
        response = call_api(url, token)
    return response

def get_country_from_region(region_id):
    url = f"https://api.hungermapdata.org/swe-notifications/region/{region_id}/country"
    response = call_api(url, token)
    if "error" in response:
        print("Token expired. Retrying")
        get_token()
        response = call_api(url, token)
    return response

def get_regions_from_country(country_id):
    url = f"https://api.hungermapdata.org/swe-notifications/country/{country_id}/regions"
    response = call_api(url, token)
    if "error" in response:
        print("Token expired. Retrying")
        get_token()
        response = call_api(url, token)
    return response

def send_email(country):
    # Simulates sending an email
    print(f"Food insecurity in country {country} has increased by 5% or more in the past 30 days.")

def get_countries_population_from_region(csv_data):
    print("Generating population")
    global countries_dict
    global region_dict
   
    for index, row in csv_data.iterrows():
        region = row['region_id']
        population = row['population']
      
        response = get_country_from_region(region)

        print(response)
        country = response['country_id']
        saved_population = countries_dict.get(country, 0) 
        countries_dict.update({country:  saved_population + population}) 

        region_dict.update({region: country})
    
    print("Country - Population ", countries_dict)
    print("Region - Country", region_dict)

    # Get food insecure data - 30 days
    global countries_insecure_dict
    insecure_response = get_food_insecure(30)

    for res in insecure_response:
        insecure_region = res['region_id']
        insecure_country = region_dict.get(insecure_region, 0)

        if insecure_country != 0:
            insecure_population = res['food_insecure_people']
            saved_insecure_population = countries_insecure_dict.get(insecure_country, 0) 

            countries_insecure_dict.update({insecure_country: saved_insecure_population + insecure_population})

    print("Country - Insecure", countries_insecure_dict)

    # Get food insecure data - Now
    global countries_insecure_now_dict
    insecure_response = get_food_insecure(0)

    for res in insecure_response:
        insecure_region = res['region_id']
        insecure_country = region_dict.get(insecure_region, 0)

        if insecure_country != 0:
            insecure_population = res['food_insecure_people']
            saved_insecure_population = countries_insecure_now_dict.get(insecure_country, 0) 

            countries_insecure_now_dict.update({insecure_country: saved_insecure_population + insecure_population})

    print("Country - Insecure NOW", countries_insecure_now_dict)


def main():
    print("Running---")
    get_token()
    population_df = get_population_dataframe()
   
    get_countries_population_from_region(population_df)

    global countries_dict
    for country in countries_dict:
        country_population = countries_dict.get(country, 0)
        insecure_population_30 = countries_insecure_dict.get(country, 0)
        insecure_population_now = countries_insecure_now_dict.get(country, 0)

        if not math.isnan(insecure_population_30) and not math.isnan(country_population):
            past_percent = (insecure_population_30 / country_population) * 100.00
            if not math.isnan(past_percent):
                print("Past percent", past_percent)

            current_percent = (insecure_population_now / country_population) * 100.00
            if not math.isnan(current_percent):
                print("Current percent", current_percent)

            if not math.isnan(current_percent) and not math.isnan(past_percent):
                if current_percent >= past_percent + 0.05:
                    send_email(country)

if __name__ == "__main__":
    main()