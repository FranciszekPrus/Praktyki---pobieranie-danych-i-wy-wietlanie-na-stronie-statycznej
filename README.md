Skrypt pobiera:
  - czas - data godzina(https://www.timeanddate.com/worldclock/poland/warsaw)
  - pogodę - na dzień dzisiejszy i trzy następne (data, opis pogody (np. mgła) przedstawiony ikonką oraz temperaturę min i max
  - święta - święta nietypowe (https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{month}/{day}.json) (https://api.open-meteo.com/v1/forecast latitude=51.8036&longitude=15.7152&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Europe/Warsaw)
  - imieniny - użyto widgetu ze strony imienniczek.pl (https://imienniczek.pl/widget/js)

Skrypt generuje także stroną html na której umieszczone zostały pozyskane dane.
