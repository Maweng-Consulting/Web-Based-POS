from apps.deliveries.models import County, SubCounty

sub_counties = [
    {
        "Machakos": [
            "Machakos Town",
            "Mavoko",
            "Kangundo",
            "Matungulu",
            "Mwala",
            "Yatta",
            "Kathiani",
            "Masinga",
        ]
    },
    {
        "Kiambu": [
            "Kiambu Town",
            "Gatundu South",
            "Gatundu North",
            "Ruiru",
            "Thika Town",
            "Juja",
            "Githunguri",
            "Kabete",
            "Kikuyu",
            "Limuru",
            "Lari",
            "Kiambaa",
            "Kipipiri",
            "Kieni",
            "Mukurwe-ini",
            "Othaya",
            "Tetu",
        ]
    },
    {
        "Nakuru": [
            "Nakuru Town East",
            "Nakuru Town West",
            "Naivasha",
            "Gilgil",
            "Subukia",
            "Rongai",
            "Njoro",
            "Molo",
            "Kuresoi North",
            "Kuresoi South",
            "Bahati",
        ]
    },
    {"Mombasa": ["Mvita", "Nyali", "Kisauni", "Changamwe", "Jomvu", "Likoni"]},
    {
        "Nairobi": [
            "Westlands",
            "Kasarani",
            "Embakasi East",
            "Embakasi West",
            "Embakasi South",
            "Embakasi Central",
            "Embakasi North",
            "Kibra",
            "Lang'ata",
            "Dagoretti South",
            "Dagoretti North",
            "Starehe",
            "Kamukunji",
            "Makadara",
            "Roysambu",
            "Ruaraka",
            "Mathare",
        ]
    },
]


def load_sub_counties():
    for town in sub_counties:
        county_name = list(town.keys())[0]
        county_towns = list(town.values())[0]
        county = County.objects.filter(name=county_name).first()
        if county:
            for x in county_towns:
                SubCounty.objects.create(county=county, name=x)
