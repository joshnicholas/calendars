# %%
import pandas as pd 

from playwright.sync_api import sync_playwright
# from playwright_stealth import stealth_sync

import datetime 
import pytz
# import requests
import json 


import os 
import pathlib
pathos = pathlib.Path(__file__).parent.parent
os.chdir(pathos)

# print(os.getcwd())

today = datetime.datetime.now()
scrape_time = today.astimezone(pytz.timezone("Australia/Brisbane"))
format_scrape_time = datetime.datetime.strftime(scrape_time, "%Y_%m")

from country_named_entity_recognition import find_countries

# %%


def shot_grabber(urlo, out_path, javascript_code, awaito):
    tries = 0

    with sync_playwright() as p:
        try:

            browser = p.firefox.launch()
            # browser = p.chromium.launch()

            context = browser.new_context()

            page = context.new_page()

            # stealth_sync(page)

            page.goto(urlo)

            # print('Before waiting')
            waiting_around = page.locator(awaito)
            waiting_around.wait_for()
            # print("After waiting")

            resulto = page.evaluate(javascript_code)

            browser.close()

            frame = pd.DataFrame.from_records(resulto)

            print(frame)
            print(frame.columns.tolist())

            frame['scraped_date_month']= format_scrape_time 

            frame = frame[['nammo', 'venue', 'date', 'scraped_date_month']]

            with open(f'{out_path}/latest.json', 'w') as f:
                frame.to_json(f, orient='records')

            with open(f'{out_path}/dumps/{format_scrape_time}.json', 'w') as f:
                frame.to_json(f, orient='records')

            # # print("Lenno: ", len(frame))
            return frame 

        except Exception as e:
            tries += 1
            print("Tries: ", tries)
            browser.close()


scraped = pd.read_json('inter/tennis/latest.json')
# scraped = shot_grabber('https://www.atptour.com/en/tournaments',  'inter/tennis',
#     """
#     var contexto = document.querySelector('.tournament-list')
#         Array.from(contexto.querySelectorAll('li'), el => {
#         let nammo = el.querySelector('.name').innerText
#         let venue = el.querySelector('.venue').innerText
#         let date = el.querySelector('.Date').innerText
#         return {nammo, venue, date};
#         })""",
#     '.tournament-list')

# %%

df = scraped.copy()

df['Location'] = df['venue'].apply(lambda x: find_countries(x, is_ignore_case=True))


print(df)

# %%

def get_timezone(stringo):

    country = find_countries(stringo, is_ignore_case=True)[0][0].alpha_2
    timezone = pytz.country_timezones[country][0]

    #### Need to convert the 
    # current_time = today.astimezone(pytz.timezone(timezone))

    # print(scrape_time)
    # print(current_time)

    # print(country)
    # print(timezone)
# print(pytz.country_timezones[testo])


get_timetime("Bologna, Spain |")

# %%
