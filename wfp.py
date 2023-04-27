import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime
import csv

# Configuration
USERNAME = "hmu.user.four"
PASSWORD = "7pHmWTfvYg9TuSy"
ADMIN_EMAIL = "admin@example.com"
RECIPIENTS = {
    "country_id_1": ["email1@example.com", "email2@example.com"],
    "country_id_2": ["email3@example.com", "email4@example.com"],
    # ... add more countries and their recipients
}

def get_token():
    url = "https://api.hungermapdata.org/swe-notifications/token"
    response = requests.post(url, auth=(USERNAME, PASSWORD))
    return response.json()["token"]

def call_api(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_population_dataframe():
    url = "https://api.hungermapdata.org/swe-notifications/population.csv"
    return pd.read_csv(url)

def calculate_food_insecurity_percent(region_id, days_ago, token):
    url = f"https://api.hungermapdata.org/swe-notifications/foodsecurity?region_id={region_id}&days_ago={days_ago}"
    food_insecurity_data = call_api(url, token)
    return food_insecurity_data["food_insecure"] / food_insecurity_data["population"]

def get_country_from_region(region_id, token):
    url = f"https://api.hungermapdata.org/swe-notifications/region/{region_id}/country"
    return call_api(url, token)

def get_regions_from_country(country_id, token):
    url = f"https://api.hungermapdata.org/swe-notifications/country/{country_id}/regions"
    return call_api(url, token)

def send_email(country_id, subject, body):
    recipients = RECIPIENTS[country_id] + [ADMIN_EMAIL]

    msg = MIMEMultipart()
    msg["From"] = "noreply@fake.smtp.wfp.org"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("fake.smtp.wfp.org", 587)
    server.starttls()
    # Replace USERNAME and PASSWORD with SMTP credentials
    server.login(USERNAME, PASSWORD)
    text = msg.as_string()
    server.sendmail("noreply@fake.smtp.wfp.org", recipients, text)
    server.quit()

def main():
    print("Running---")
    token = get_token()
    print("Token-->",token)
    population_df = get_population_dataframe()
    print("population_df-->",population_df)

    for country_id in RECIPIENTS.keys():
        print("country_id", country_id)
        regions = get_regions_from_country(country_id, token)
        print("regions", regions)

        for region in regions:
            region_id = region["id"]
            population = population_df.loc[population_df["region_id"] == region_id, "population"].item()

            current_percent = calculate_food_insecurity_percent(region_id, 0, token)
            past_percent = calculate_food_insecurity_percent(region_id, 30, token)

            if current_percent >= past_percent + 0.05:
                country = get_country_from_region(region_id, token)
                subject = f"Food security alert for {country['name']}"
                body = f"Food insecurity in {country['name']} has increased by 5% or more in the past 30 days."
                send_email(country_id, subject, body)

if __name__ == "__main__":
    main()
