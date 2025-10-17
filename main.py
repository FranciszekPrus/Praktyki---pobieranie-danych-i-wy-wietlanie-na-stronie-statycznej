import os
import webbrowser
from playwright.sync_api import sync_playwright
import requests
from datetime import datetime

def pobierz_czas():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.timeanddate.com/worldclock/poland/warsaw", timeout=20000)
            page.wait_for_selector("#ct", timeout=15000)
            czas_str = page.query_selector("#ct").inner_text().strip()
            browser.close()
            return czas_str
    except Exception as e:
        print(f"Nie udało się pobrać czasu({e})")
        return datetime.now().strftime("%H:%M:%S")

def pobierz_pogode():
    try:
        lat, lon = 51.8036, 15.7152
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Europe/Warsaw")
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        weather_icons = {
            0: "https://openweathermap.org/img/wn/01d@2x.png",  # bezchmurnie
            1: "https://openweathermap.org/img/wn/02d@2x.png",  # częściowo słonecznie
            2: "https://openweathermap.org/img/wn/03d@2x.png",  # pochmurno
            3: "https://openweathermap.org/img/wn/09d@2x.png",  # przelotny deszcz
            45: "https://openweathermap.org/img/wn/50d@2x.png",  # mgła
            48: "https://openweathermap.org/img/wn/50d@2x.png",  # mgła z lodem
            51: "https://openweathermap.org/img/wn/09d@2x.png",  # mżawka lekka
            53: "https://openweathermap.org/img/wn/09d@2x.png",  # mżawka umiarkowana
            55: "https://openweathermap.org/img/wn/09d@2x.png",  # mżawka silna
            61: "https://openweathermap.org/img/wn/10d@2x.png",  # deszcz lekki
            63: "https://openweathermap.org/img/wn/10d@2x.png",  # deszcz umiarkowany
            65: "https://openweathermap.org/img/wn/10d@2x.png",  # deszcz silny
            71: "https://openweathermap.org/img/wn/13d@2x.png",  # śnieg lekki
            73: "https://openweathermap.org/img/wn/13d@2x.png",  # śnieg umiarkowany
            75: "https://openweathermap.org/img/wn/13d@2x.png",  # śnieg silny
            80: "https://openweathermap.org/img/wn/09d@2x.png",  # przelotny deszcz
            81: "https://openweathermap.org/img/wn/09d@2x.png",  # przelotny deszcz silny
            82: "https://openweathermap.org/img/wn/11d@2x.png",  # burzowo
        }

        pogoda_dni = []
        for i in range(4):
            max_temp = data["daily"]["temperature_2m_max"][i]
            min_temp = data["daily"]["temperature_2m_min"][i]
            weathercode = data["daily"]["weathercode"][i]

            ikona = weather_icons.get(weathercode, "https://www.weatherbit.io/static/img/icons/na.png")

            dzien_data = datetime.strptime(data["daily"]["time"][i], "%Y-%m-%d").strftime("%d %B %Y")
            pogoda_dni.append(f"<b>{dzien_data}</b><br><img src='{ikona}' alt='pogoda'><br>min {min_temp}°C, max {max_temp}°C")

        return pogoda_dni

    except Exception as e:
        print(f"Błąd pobierania pogody: {e}")
        return ["Brak danych o pogodzie"] * 3

def pobierz_swieta():
    try:
        dzisiaj = datetime.now()
        month = dzisiaj.month
        day = dzisiaj.day
        url = f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{month}/{day}.json"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data:
            return [item.get("name") for item in data]
        else:
            return ["Brak danych dotyczących świąt"]
    except Exception as e:
        print(f"Błąd pobierania świąt{e}")
        return ["Brak danych dotyczących święta"]


def pobierz_imieniny():
    return '<div id="imieniny-widget"></div><script type="text/javascript" src="https://imienniczek.pl/widget/js"></script>'

czas_str = pobierz_czas()
pogoda = pobierz_pogode()
swieta = pobierz_swieta()

godz, min, sek = map(int, czas_str.split(":"))


pogoda_html = "<table border='1' style='margin:0 auto; border-collapse:collapse;'>\n<tr>\n"
for linia in pogoda:
    pogoda_html += f"<td style='padding:10px; text-align:center;'>{linia}</td>\n"
pogoda_html += "</tr>\n</table>"

swieta_html = "<ul style='list-style-type:none; padding:0;'>"
for s in swieta:
    swieta_html += f"<li>{s}</li>"
swieta_html += "</ul>"

html = fr"""<!DOCTYPE html>
<html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Gedia Praktyki</title>

        <style>
            @font-face {{
                font-family: 'Helenoir-Compact';
                src: url('fonty/Helenoir-Compact.oft') format('oft');
                font-weight: normal;
                font-style: normal;
            }}
            body {{
                font-family: 'Helenoir-Compact';
                text-align: center;
                margin: 0;
                background: linear-gradient(120deg, #f0f4f8, #d9e4f5);
                color: black;
                ;
            }}

            header {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                color: white;
                background-color: #051214;
                margin: 0;
                padding: 10px 20px;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 1000;
                border-bottom: 3px #041213;
                height: 80px;
            }}

            header img {{
                height: 50px;
                width: auto;
            }}

            main {{
                padding-top: 110px;
                padding-bottom: 80px; 
                background-color: #FFFFFF;
                
            }}
            
            .content-wrapper {{
                background-color: #C7D1D3;
                padding: 20px;
                border-radius: 10px;
                margin: 5px 10px 0 10px; 
                box-sizing: border-box;
                height: calc(100vh - 80px - 50px - 50px); 
            }}

            footer {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px;
                color: white;
                background-color: #051214;
                margin: 0;
                padding: 10px 20px;
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                z-index: 1000;
                border-top: 3px #041213;
                height: 30px; 
            }}

            #dataPolska {{
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            
            #godzinaPolska {{
                font-size: 60px;
                font-weight: bold;
                margin-bottom: 0px;
            }}
            #pogoda td {{
                background-color: #051214;
                color: white;\
                border: 1px solid #ffffff;  /* opcjonalna biała ramka dla lepszej czytelności */
                padding: 10px;
                text-align: center;
            }}
        </style>
    </head>
    
    <body>
        <header>   
            <h1>GEDIA POLAND</h1>
            <img src="C:\Users\Kleszczu\PycharmProjects\gediahtml\GEDIA_logo.png">
        </header>

        <main>
            <div class="content-wrapper">
                <p id="dataPolska"></p>
                <p id="godzinaPolska"></p>

                <h2>PROGNOZA POGODY</h2>
                <div id="pogoda">{pogoda_html}</div>

                <h2>OBCHODZIMY DZISIAJ NASTĘPUJĄCE ŚWIĘTA</h2>
                <div id="swieta">{swieta_html}</div>
        
                <h2>IMIENINY</h2>
                {pobierz_imieniny()}
            </div>
        </main>

        <footer>
            <h5>Stworzono przez: Franciszek Prus sierpień 2025 - praktyki zawodowe</h5>
        </footer>

        
        <script>
            let czasPL = new Date();
            czasPL.setHours({godz}, {min}, {sek}, 0);

            const nazwyMiesiecy = ["stycznia","lutego","marca","kwietnia","maja","czerwca",
            "lipca","sierpnia","września","października","listopada","grudnia"];

            const dataEl = document.getElementById('dataPolska');
            const godzinaEl = document.getElementById('godzinaPolska');

            function aktualizujZegar() {{
                const dzien = String(czasPL.getDate()).padStart(2, '0');
                const miesiac = nazwyMiesiecy[czasPL.getMonth()];
                const rok = czasPL.getFullYear();
                const godz = String(czasPL.getHours()).padStart(2, '0');
                const min = String(czasPL.getMinutes()).padStart(2, '0');
                const sek = String(czasPL.getSeconds()).padStart(2, '0');

                dataEl.textContent = `${{dzien}} ${{miesiac}} ${{rok}}`;
                godzinaEl.textContent = `${{godz}}:${{min}}:${{sek}}`;

                czasPL.setSeconds(czasPL.getSeconds() + 1);
            }}

            aktualizujZegar();
            setInterval(aktualizujZegar, 1000);
        </script>
    </body>
</html>
"""

plik = "Gedia - pobieranie danych.html"
with open(plik, "w", encoding="utf-8") as f:
    f.write(html)

webbrowser.open(f"file://{os.path.abspath(plik)}")

