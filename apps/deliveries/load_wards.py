from apps.deliveries.models import SubCounty, Ward
wards_in_mombasa = [
    {
        "Mvita": [
            "Tudor",
            "Tononoka",
            "Shimanzi/Ganjoni",
            "Majengo",
            "Mji wa Kale/Makadara"
        ]
    },
    {
        "Nyali": [
            "Frere Town",
            "Kongowea",
            "Kadzandani",
            "Mkomani",
            "Ziwa la Ng'ombe"
        ]
    },
    {
        "Kisauni": [
            "Mjambere",
            "Junda",
            "Bamburi",
            "Mwakirunge",
            "Shanzu"
        ]
    },
    {
        "Changamwe": [
            "Port Reitz",
            "Kipevu",
            "Airport",
            "Changamwe"
        ]
    },
    {
        "Jomvu": [
            "Jomvu Kuu",
            "Mikindani",
            "Miritini"
        ]
    },
    {
        "Likoni": [
            "Bofu",
            "Mtongwe",
            "Likoni",
            "Shika Adabu",
            "Timbwani"
        ]
    }
]



def load_county_wards():
    for ward in wards_in_mombasa:
        sub_county_name = list(ward.keys())[0]
        wards_list = list(ward.values())[0]
        sub_county = SubCounty.objects.filter(name=sub_county_name).first()
        if sub_county:
            for x in wards_list:
                Ward.objects.create(sub_county=sub_county, name=x)


