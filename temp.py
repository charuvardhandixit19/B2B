import requests
from bs4 import BeautifulSoup
import pandas as pd

events_data = []

def scrape_event(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Selectors for Eventbrite
        event_name = soup.find('h1', class_='event-title').text.strip() if soup.find('h1', class_='event-title') else "N/A"
        event_dates = soup.find('span', class_='date-info__full-datetime').text.strip() if soup.find('span', class_='date-info__full-datetime') else "N/A"
        location = soup.find('div', class_='location-info__address').text.strip() if soup.find('div', class_='location-info__address') else "Online"
        description = soup.find('div', class_='structured-content-rich-text').text.strip() if soup.find('div', class_='structured-content-rich-text') else "N/A"
        key_speakers = [speaker.text.strip() for speaker in soup.select('div.speakers-section span.speaker')] or ["N/A"]
        
        event = {
            "Event Name": event_name,
            "Event Date(s)": event_dates,
            "Location": location,
            "Website URL": url,
            "Description": description,
            "Key Speakers": key_speakers,
            "Agenda/Schedule": "N/A",  # Update if available
            "Registration Details": "N/A",  # Update if available
            "Pricing": "N/A",  # Update if available
            "Categories": "N/A",  # Update if available
            "Audience Type": "N/A"  # Update if available
        }

        events_data.append(event)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

urls = [
    'https://www.eventbrite.com/e/java-burn-coffee-canada-important-news-must-watch-expert-experiences-tickets-901280934537?aff=ebdssbdestsearch&_gl=1*1msutvn*_up*MQ..*_ga*MzU4MTYwNjI5LjE3MTg1NTc3MTA.*_ga_TQVES5V6SH*MTcxODU1NzcwOS4xLjAuMTcxODU1NzcwOS4wLjAuMA..'
]

for url in urls:
    scrape_event(url)

df = pd.DataFrame(events_data)
df.to_csv('b2b_events.csv', index=False)
