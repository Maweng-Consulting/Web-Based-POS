from apps.deliveries.models import County, Town

towns = [
    {
        "Nairobi": [
            "Nairobi",
            "Pipeline",
            "Westlands",
            "Kayole",
            "Kariobangi",
            "Eastleigh",
        ]
    },
    {"Mombasa": ["Mombasa"]},
    {"Kisumu": ["Kisumu"]},
    {"Nakuru": ["Nakuru", "Naivasha", "Gilgil"]},
    {
        "Kiambu": [
            "Thika",
            "Kiambu",
            "Ruiru",
            "Juja",
            "Kahawa Sukari",
            "Limuru",
            "Githunguri",
        ]
    },
    {
        "Machakos": [
            "Machakos",
            "Mwala",
            "Kangundo",
            "Masinga",
            "Matuu",
            "Kithimani",
            "Tala",
        ]
    },
    {"Nyeri": ["Nyeri", "Karatina", "Othaya"]},
    {"Meru": ["Meru", "Maua", "Timau", "Nkubu"]},
    {"Kakamega": ["Kakamega", "Mumias", "Lugari", "Lurambi"]},
    {"Eldoret": ["Eldoret"]},
    {"Tharaka-Nithi": ["Chuka", "Marimanti"]},
    {"Embu": ["Embu", "Runyenjes"]},
    {"Kajiado": ["Kajiado", "Ngong", "Kitengela"]},
    {"Kericho": ["Kericho", "Londiani"]},
    {"Kilifi": ["Kilifi", "Malindi", "Watamu", "Kaloleni"]},
    {"Kisii": ["Kisii", "Ogembo", "Nyamira"]},
    {"Kirinyaga": ["Kerugoya", "Kutus", "Kagio"]},
    {"Laikipia": ["Nanyuki", "Rumuruti", "Nyahururu"]},
    {"Bomet": ["Bomet", "Sotik", "Chepalungu"]},
    {"Bungoma": ["Bungoma", "Webuye", "Kimilili"]},
    {"Busia": ["Busia", "Nambale", "Butula"]},
    {"Elgeyo-Marakwet": ["Iten", "Kapsowar"]},
    {"Garissa": ["Garissa", "Dadaab"]},
    {"Homa Bay": ["Homa Bay", "Mbita", "Oyugis"]},
    {"Isiolo": ["Isiolo", "Garbatulla"]},
    {"Lamu": ["Lamu", "Mokowe", "Mpeketoni"]},
    {"Mandera": ["Mandera", "Elwak", "Rhamu"]},
    {"Marsabit": ["Marsabit", "Moyale", "Laisamis"]},
    {"Migori": ["Migori", "Awendo", "Rongo"]},
    {"Murang'a": ["Murang'a", "Kangema", "Kigumo"]},
    {"Narok": ["Narok", "Kilgoris", "Suswa"]},
    {"Nyandarua": ["Ol Kalou", "Nyahururu"]},
    {"Samburu": ["Maralal", "Baragoi", "Wamba"]},
    {"Siaya": ["Siaya", "Bondo", "Ugunja"]},
    {"Taita-Taveta": ["Voi", "Wundanyi", "Taveta"]},
    {"Tana River": ["Hola", "Garsen", "Bura"]},
    {"Trans-Nzoia": ["Kitale", "Endebess", "Kiminini"]},
    {"Turkana": ["Lodwar", "Lokichogio", "Kakuma"]},
    {"Uasin Gishu": ["Eldoret", "Turbo", "Moiben"]},
    {"Vihiga": ["Vihiga", "Mbale", "Luanda"]},
    {"Wajir": ["Wajir", "Habaswein", "Bute"]},
    {"West Pokot": ["Kapenguria", "Chepareria"]},
    {"Kwale": ["Kwale", "Ukunda", "Kinango"]},
    {"Nandi": ["Kapsabet", "Nandi Hills", "Mosoriot"]},
    {"Baringo": ["Kabarnet", "Eldama Ravine", "Mogotio"]},
    {"Kitui": ["Kitui", "Mwingi", "Mutomo"]},
    {"Migori": ["Migori", "Awendo", "Rongo"]},
    {"Kisumu": ["Kisumu", "Ahero", "Maseno"]},
    {"Nyamira": ["Nyamira", "Keroka", "Manga"]},
    {"Taita Taveta": ["Voi", "Wundanyi", "Taveta"]},
]


def load_towns():
    for town in towns:
        county_name = list(town.keys())[0]
        county_towns = list(town.values())[0]
        county = County.objects.filter(name=county_name).first()
        if county:
            for x in county_towns:
                Town.objects.create(county=county, name=x)


# load_towns()
