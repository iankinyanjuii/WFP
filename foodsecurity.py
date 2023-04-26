import requests, datetime, csv, smtplib

# Constants
base_url = 'https://api.hungermapdata.org/swe-notifications'
population_csv_url = 'https://api.hungermapdata.org/swe-notifications/population.csv'

email_server = {
        'host': 'fake.smtp.wfp.org', 
        'port': 587, 
        'username': 'user', 
        'password': 'pass'
    }

def get_bearer_token():
    response = requests.post(base_url + '/token', auth=('hmu.user.four','7pHmWTfvYg9TuSy'))
    print("Response Token =====> ", response)

    token = response.json()['token']
    print("Token =====> ", token)
    return token

def get_food_security_data(region, days_ago, bearer_token):
    response = requests.get(base_url + f'/foodsecurity?days_ago={days_ago}', headers={'Authorization': f'Bearer {bearer_token}'})
    print("Response Food Security =====> ", response)
    return response.json()

def calculate_food_insecurity_percentage(country_data, population_data):
    total_population = sum([int(population_data[region]) for region in population_data])
    total_food_insecure = sum([region_data['food_insecure'] for region_data in country_data])
    return (total_food_insecure / total_population) * 100

def read_population_data():
    response = requests.get(population_csv_url)
    reader = csv.DictReader(response.text.splitlines())
    population_data = {}
    for row in reader:
        population_data[row['region_id']] = row['population']
    return population_data

def calculate_total_population(country_data, population_data):
    return sum([int(population_data[region]) for region in country_data])

def has_food_insecurity_increased(country, current_percentage, previous_percentage):
    return (current_percentage - previous_percentage) >= 5

def send_email_notification(recipient, subject, message, email_server):
     print("==== Email Sent ====") 

def main():
    print("Running -------------")
    bearer_token = get_bearer_token()
    population_data = read_population_data()
    for country in ['Country A', 'Country B', 'Country C']:
        country_data = get_food_security_data(country, 30, bearer_token)
        print("Country Data =====> ", country_data)
        current_percentage = calculate_food_insecurity_percentage(country_data, population_data)
        print("Current Percentage =====> ", current_percentage) 
        previous_percentage = calculate_food_insecurity_percentage(country_data, population_data)
        print("Previous Percentage =====> ", previous_percentage) 
        
        if has_food_insecurity_increased(country, current_percentage, previous_percentage):
            message = f"Food insecurity in {country} has increased by more than 5% in the past 30 days."
            send_email_notification('recipient@example.com', f"Food insecurity alert for {country}", message, email_server)

main()