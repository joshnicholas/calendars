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

# from country_named_entity_recognition import find_countries

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
            print(e)
            print("Tries: ", tries)
            browser.close()


# scraped = pd.read_json('inter/tennis/latest.json')
scraped = shot_grabber('https://www.espn.com.au/tennis/schedule',  'inter/e_schedule',
    """
    var contexto = document.querySelector('.layout')
        Array.from(contexto.querySelectorAll('.Table__TR'), el => {
            if (el.querySelector('.AnchorLink') !== null)
            {
        let nammo = el.querySelector('.eventAndLocation__col').innerText
        let date = el.querySelector('.dateRange__col').innerText
        let linko = el.querySelector('.AnchorLink').href
        return {nammo, date, linko};
            }
        })""",
    '.layout')

# %%

# df = scraped.copy()

# df['Location'] = df['venue'].apply(lambda x: find_countries(x, is_ignore_case=True))


# print(df)

# %%

#     var contexto = document.querySelector('.Card')
#         Array.from(contexto.querySelectorAll('.Table__TR'), el => {
#             if (el.querySelector('.AnchorLink') !== null)
#             {
#         let nammo = el.querySelector('.eventAndLocation__col').innerText
#         let date = el.querySelector('.dateRange__col').innerText
#         let linko = el.querySelector('.AnchorLink').href
#         return {nammo, date, linko};
#             }
#         })

# Table__TBODY
# .getAttribute("href")
# if (el.querySelector('.eventAndLocation__col') !== null)