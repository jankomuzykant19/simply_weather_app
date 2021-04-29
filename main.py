from requests import get
from json import loads
from terminaltables import AsciiTable


# load - ładuje z pliku, loads - tyczy się stringów

def main():
    url = "https://danepubliczne.imgw.pl/api/data/synop"
    response = get(url)
    # 2xx - ok
    # 3xx - przekierowanie
    # 4xx - blędy użytkownika
    # 5xx - coś się stało po stronie serwera

    count = 0
    print("Available meteorologic stations:\n")
    for row in loads(response.text):
        print(row['stacja'], end=", ")
        count += 1
        if count % 9 == 0:
            print()

    print('\n' * 2)

    a = input("Insert station/stations devided by ','\n")
    cities = a.split(',')

    rows = [
        ['Station', 'Temperature', 'Pressure', 'Date', 'Hour']
    ]

    avg_temp = 0
    avg_press = 0
    no_press = 0

    for row in loads(response.text):
        avg_temp += float(row['temperatura'])
        if row['cisnienie'] is not None:
            avg_press += float(row['cisnienie'])
        else:
            no_press += 1
        if row['stacja'] in cities:
            rows.append([
                row['stacja'],
                row['temperatura'] + '°C',
                row['cisnienie'],
                row['data_pomiaru'],
                row['godzina_pomiaru'] + ':00'
            ])

    print("Average temperature in Poland:", round(avg_temp / len(loads(response.text)), 2))
    print("Average pressure in Poland:", round((avg_press / (len(loads(response.text)) - no_press)), 2))

    table = AsciiTable(rows)
    print(table.table)


if __name__ == '__main__':
    main()
