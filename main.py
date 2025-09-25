import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

pokemon_sets = [
    "Pokemon 1999 Topps Movie",
    "Pokemon 1999 Topps Movie Evolution",
    "Pokemon 1999 Topps TV",
    "Pokemon 2000 Topps Chrome",
    "Pokemon 2000 Topps TV",
    "Pokemon 2020 Battle Academy",
    "Pokemon Ancient Origins",
    "Pokemon Aquapolis",
    "Pokemon Arceus",
    "Pokemon Astral Radiance",
    "Pokemon BREAKpoint",
    "Pokemon BREAKthrough",
    "Pokemon Base Set",
    "Pokemon Base Set 2",
    "Pokemon Battle Styles",
    "Pokemon Best of Game",
    "Pokemon Black & White",
    "Pokemon Black Bolt",
    "Pokemon Boundaries Crossed",
    "Pokemon Brilliant Stars",
    "Pokemon Burger King",
    "Pokemon Burning Shadows",
    "Pokemon Call of Legends",
    "Pokemon Celebrations",
    "Pokemon Celestial Storm",
    "Pokemon Champion's Path",
    "Pokemon Chilling Reign",
    "Pokemon Chinese CS4aC",
    "Pokemon Chinese CS4bC",
    "Pokemon Chinese CSM2aC",
    "Pokemon Chinese CSM2bC",
    "Pokemon Chinese CSM2cC",
    "Pokemon Chinese Gem Pack",
    "Pokemon Chinese Gem Pack 2",
    "Pokemon Chinese Promo",
    "Pokemon Chinese Scarlet & Violet 151",
    "Pokemon Cosmic Eclipse",
    "Pokemon Crimson Invasion",
    "Pokemon Crown Zenith",
    "Pokemon Crystal Guardians",
    "Pokemon Dark Explorers",
    "Pokemon Darkness Ablaze",
    "Pokemon Delta Species",
    "Pokemon Deoxys",
    "Pokemon Destined Rivals",
    "Pokemon Detective Pikachu",
    "Pokemon Diamond & Pearl",
    "Pokemon Double Crisis",
    "Pokemon Dragon",
    "Pokemon Dragon Frontiers",
    "Pokemon Dragon Majesty",
    "Pokemon Dragon Vault",
    "Pokemon Dragons Exalted",
    "Pokemon EX Latias & Latios",
    "Pokemon Emerald",
    "Pokemon Emerging Powers",
    "Pokemon Evolutions",
    "Pokemon Evolving Skies",
    "Pokemon Expedition",
    "Pokemon Fates Collide",
    "Pokemon Fire Red & Leaf Green",
    "Pokemon Flashfire",
    "Pokemon Forbidden Light",
    "Pokemon Fossil",
    "Pokemon Furious Fists",
    "Pokemon Fusion Strike",
    "Pokemon Generations",
    "Pokemon Go",
    "Pokemon Great Encounters",
    "Pokemon Guardians Rising",
    "Pokemon Gym Challenge",
    "Pokemon Gym Heroes",
    "Pokemon HeartGold & SoulSilver",
    "Pokemon Hidden Fates",
    "Pokemon Hidden Legends",
    "Pokemon Holon Phantoms",
    "Pokemon Japanese 10th Movie Commemoration Promo",
    "Pokemon Japanese 1996 Carddass",
    "Pokemon Japanese 1997 Carddass",
    "Pokemon Japanese 2002 McDonald's",
    "Pokemon Japanese 2005 Gift Box",
    "Pokemon Japanese 20th Anniversary",
    "Pokemon Japanese 25th Anniversary Collection",
    "Pokemon Japanese 25th Anniversary Golden Box",
    "Pokemon Japanese 25th Anniversary Promo",
    "Pokemon Japanese Advent of Arceus",
    "Pokemon Japanese Alter Genesis",
    "Pokemon Japanese Amazing Volt Tackle",
    "Pokemon Japanese Ancient Roar",
    "Pokemon Japanese Awakening Legends",
    "Pokemon Japanese Awakening Psychic King",
    "Pokemon Japanese Bandit Ring",
    "Pokemon Japanese Battle Partners",
    "Pokemon Japanese Battle Region",
    "Pokemon Japanese Best of XY",
    "Pokemon Japanese Black Bolt",
    "Pokemon Japanese Blue Shock",
    "Pokemon Japanese Blue Sky Stream",
    "Pokemon Japanese CD Promo",
    "Pokemon Japanese Challenge from the Darkness",
    "Pokemon Japanese Charizard VMAX Starter Set",
    "Pokemon Japanese Clash of the Blue Sky",
    "Pokemon Japanese Classic: Blastoise",
    "Pokemon Japanese Classic: Charizard",
    "Pokemon Japanese Classic: Venusaur",
    "Pokemon Japanese Clay Burst",
    "Pokemon Japanese Crimson Haze",
    "Pokemon Japanese Crossing the Ruins",
    "Pokemon Japanese Cyber Judge",
    "Pokemon Japanese Dark Phantasma",
    "Pokemon Japanese Darkness, and to Light",
    "Pokemon Japanese Detective Pikachu",
    "Pokemon Japanese Double Blaze",
    "Pokemon Japanese Double Crisis",
    "Pokemon Japanese Dream League",
    "Pokemon Japanese Dream Shine Collection",
    "Pokemon Japanese EX Battle Boost",
    "Pokemon Japanese Eevee Heroes",
    "Pokemon Japanese Emerald Break",
    "Pokemon Japanese Expansion Pack",
    "Pokemon Japanese Expedition Expansion Pack",
    "Pokemon Japanese Fusion Arts",
    "Pokemon Japanese Future Flash",
    "Pokemon Japanese GG End",
    "Pokemon Japanese GX Battle Boost",
    "Pokemon Japanese GX Ultra Shiny",
    "Pokemon Japanese Gengar Vmax High-Class",
    "Pokemon Japanese Glory of Team Rocket",
    "Pokemon Japanese Go",
    "Pokemon Japanese Gold, Silver, New World",
    "Pokemon Japanese Golden Sky, Silvery Ocean",
    "Pokemon Japanese Heat Wave Arena",
    "Pokemon Japanese Holon Phantom",
    "Pokemon Japanese Holon Research",
    "Pokemon Japanese Incandescent Arcana",
    "Pokemon Japanese Intense Fight in the Destroyed Sky",
    "Pokemon Japanese Jet-Black Spirit",
    "Pokemon Japanese Jungle",
    "Pokemon Japanese Leaders' Stadium",
    "Pokemon Japanese Legendary Shine Collection",
    "Pokemon Japanese Lost Abyss",
    "Pokemon Japanese Mask of Change",
    "Pokemon Japanese Matchless Fighter",
    "Pokemon Japanese Mega Brave",
    "Pokemon Japanese Mega Symphonia",
    "Pokemon Japanese Miracle Crystal",
    "Pokemon Japanese Miracle Twins",
    "Pokemon Japanese Mysterious Mountains",
    "Pokemon Japanese Mystery of the Fossils",
    "Pokemon Japanese Night Unison",
    "Pokemon Japanese Night Wanderer",
    "Pokemon Japanese Offense and Defense of the Furthest Ends",
    "Pokemon Japanese Old Maid",
    "Pokemon Japanese Paradigm Trigger",
    "Pokemon Japanese Paradise Dragona",
    "Pokemon Japanese Phantom Gate",
    "Pokemon Japanese Player's Club",
    "Pokemon Japanese PokeKyun Collection",
    "Pokemon Japanese Premium Champion Pack",
    "Pokemon Japanese Promo",
    "Pokemon Japanese Rage of the Broken Heavens",
    "Pokemon Japanese Raging Surf",
    "Pokemon Japanese Rayquaza-EX Mega Battle Deck",
    "Pokemon Japanese Red Collection",
    "Pokemon Japanese Remix Bout",
    "Pokemon Japanese Reviving Legends",
    "Pokemon Japanese Rocket Gang",
    "Pokemon Japanese Rocket Gang Strikes Back",
    "Pokemon Japanese Ruler of the Black Flame",
    "Pokemon Japanese SVG Special Set",
    "Pokemon Japanese Scarlet & Violet 151",
    "Pokemon Japanese Scarlet Ex",
    "Pokemon Japanese Shield",
    "Pokemon Japanese Shining Darkness",
    "Pokemon Japanese Shining Legends",
    "Pokemon Japanese Shiny Collection",
    "Pokemon Japanese Shiny Star V",
    "Pokemon Japanese Shiny Treasure ex",
    "Pokemon Japanese Sky Legend",
    "Pokemon Japanese Snow Hazard",
    "Pokemon Japanese SoulSilver Collection",
    "Pokemon Japanese Southern Island",
    "Pokemon Japanese Space Juggler",
    "Pokemon Japanese Split Earth",
    "Pokemon Japanese Star Birth",
    "Pokemon Japanese Start Deck 100",
    "Pokemon Japanese Starter Set SVOM",
    "Pokemon Japanese Stellar Miracle",
    "Pokemon Japanese Super Electric Breaker",
    "Pokemon Japanese Super-Burst Impact",
    "Pokemon Japanese Tag All Stars",
    "Pokemon Japanese Tag Bolt",
    "Pokemon Japanese Tag Team Starter Set",
    "Pokemon Japanese Terastal Festival",
    "Pokemon Japanese The Town on No Map",
    "Pokemon Japanese Time Gazer",
    "Pokemon Japanese Topsun",
    "Pokemon Japanese Triplet Beat",
    "Pokemon Japanese VMAX Climax",
    "Pokemon Japanese VS",
    "Pokemon Japanese VSTAR Universe",
    "Pokemon Japanese Vending",
    "Pokemon Japanese Violet Ex",
    "Pokemon Japanese Web",
    "Pokemon Japanese White Flare",
    "Pokemon Japanese Wild Blaze",
    "Pokemon Japanese Wild Force",
    "Pokemon Japanese Wind from the Sea",
    "Pokemon Japanese World Championships 2023",
    "Pokemon Japanese Yamabuki City Gym",
    "Pokemon Journey Together",
    "Pokemon Jungle",
    "Pokemon Korean Promo",
    "Pokemon Korean Terastal Festival ex",
    "Pokemon Legend Maker",
    "Pokemon Legendary Collection",
    "Pokemon Legendary Treasures",
    "Pokemon Legends Awakened",
    "Pokemon Lost Origin",
    "Pokemon Lost Thunder",
    "Pokemon Majestic Dawn",
    "Pokemon McDonalds 2018",
    "Pokemon McDonalds 2019",
    "Pokemon McDonalds 2021",
    "Pokemon McDonalds 2022",
    "Pokemon McDonalds 2023",
    "Pokemon McDonalds 2024",
    "Pokemon Mysterious Treasures",
    "Pokemon Neo Destiny",
    "Pokemon Neo Discovery",
    "Pokemon Neo Genesis",
    "Pokemon Neo Revelation",
    "Pokemon Next Destinies",
    "Pokemon Noble Victories",
    "Pokemon Obsidian Flames",
    "Pokemon POP Series 1",
    "Pokemon POP Series 2",
    "Pokemon POP Series 3",
    "Pokemon POP Series 4",
    "Pokemon POP Series 5",
    "Pokemon POP Series 9",
    "Pokemon Paldea Evolved",
    "Pokemon Paldean Fates",
    "Pokemon Paradox Rift",
    "Pokemon Phantom Forces",
    "Pokemon Pikachu Libre & Suicune",
    "Pokemon Plasma Blast",
    "Pokemon Plasma Freeze",
    "Pokemon Plasma Storm",
    "Pokemon Platinum",
    "Pokemon Power Keepers",
    "Pokemon Primal Clash",
    "Pokemon Prismatic Evolutions",
    "Pokemon Promo",
    "Pokemon Rebel Clash",
    "Pokemon Rising Rivals",
    "Pokemon Roaring Skies",
    "Pokemon Ruby & Sapphire",
    "Pokemon Rumble",
    "Pokemon Sandstorm",
    "Pokemon Scarlet & Violet",
    "Pokemon Scarlet & Violet 151",
    "Pokemon Scarlet & Violet Energy",
    "Pokemon Secret Wonders",
    "Pokemon Shining Fates",
    "Pokemon Shining Legends",
    "Pokemon Shrouded Fable",
    "Pokemon Silver Tempest",
    "Pokemon Skyridge",
    "Pokemon Southern Islands",
    "Pokemon Steam Siege",
    "Pokemon Stellar Crown",
    "Pokemon Stormfront",
    "Pokemon Sun & Moon",
    "Pokemon Supreme Victors",
    "Pokemon Surging Sparks",
    "Pokemon Sword & Shield",
    "Pokemon TCG Classic: Blastoise Deck",
    "Pokemon TCG Classic: Charizard Deck",
    "Pokemon TCG Classic: Venusaur Deck",
    "Pokemon Team Magma & Team Aqua",
    "Pokemon Team Rocket",
    "Pokemon Team Rocket Returns",
    "Pokemon Team Up",
    "Pokemon Temporal Forces",
    "Pokemon Trick or Trade 2022",
    "Pokemon Trick or Trade 2023",
    "Pokemon Trick or Trade 2024",
    "Pokemon Triumphant",
    "Pokemon Twilight Masquerade",
    "Pokemon Ultra Prism",
    "Pokemon Unbroken Bonds",
    "Pokemon Undaunted",
    "Pokemon Unified Minds",
    "Pokemon Unleashed",
    "Pokemon Unseen Forces",
    "Pokemon Vivid Voltage",
    "Pokemon White Flare",
    "Pokemon World Championships 2007",
    "Pokemon XY"
]

def space_replace(lst):
    for i in range(len(lst)):
        lst[i] = lst[i].replace(" ", "-").lower()
    return lst

#language?
#setname = white
#using the - list
"""
this should return the set name like this:
first ask langauge (english, Japenese, Chinese)
inout: White Flare
return: white-flare

"""




def find_name(language, set_name,lst):
    if language == "chinese":
        for name in lst:
            if "chinese" in name and set_name in name:
                return name
        return "chinese set not found"


    elif language == "japanese":
        for name in lst:
            if "japanese" in name and set_name in name:
                return name
        return "japanese set not found"
                
    

    elif language == "english":
        for name in lst:
            if "japanese" not in name and "chinese" not in name and set_name in name:
                return name
        return "english set not found"
    else:
        return "language not found"
    




def create_url(set_name, card_name):
    url = f"https://www.pricecharting.com/game/{set_name}/{card_name}"
    return url
    
    

def get_rate():
    try:
        url = "https://www.xe.com/en-ca/currencyconverter/convert/?Amount=1&From=USD&To=CAD"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        rate_text = soup.find('p', class_='sc-c5062ab2-1 jKDFIr').text.strip()
        rate = float(rate_text[0:4])
        return rate
    except Exception:
        return 1.35


def usd_to_cad(usd):
    rate = get_rate()
    cad = usd * rate
    return cad



def get_price_and_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get price data
    price = soup.find('span', class_='price js-price').text.strip()
    price_change = soup.find('span', class_='change').text.strip()

    price_float = float(price[1:])
    
    # Handle positive/negative price changes
    if price_change.startswith('+$'):
        price_change_float = float(price_change[2:])
    elif price_change.startswith('-$'):
        price_change_float = -float(price_change[2:])
    else:
        # Fallback for other formats
        price_change_float = float(price_change[2:]) if len(price_change) > 2 else 0

    price = round(price_float, 2)
    price_change = round(price_change_float, 2)

    # Get card image
    card_image = None
    try:
        # Look for the card image - PriceCharting typically has it in an img tag with specific classes
        img_element = soup.find('img', class_='js-show-dialog') or soup.find('img', {'alt': True})
        if img_element and img_element.get('src'):
            card_image = img_element['src']
            # Ensure it's a full URL
            if card_image.startswith('//'):
                card_image = 'https:' + card_image
            elif card_image.startswith('/'):
                card_image = 'https://www.pricecharting.com' + card_image
    except Exception as e:
        print(f"Error getting card image: {e}")
        card_image = None

    return price, price_change, card_image
    
    
    
    

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        language = request.form.get('language', 'english').lower()
        set_name = request.form.get('set_name', '').lower().replace(" ", "-")
        card_name = request.form.get('card_name', '').lower().replace(" ", "-")
        
        set_list = space_replace(pokemon_sets.copy())
        found_set = find_name(language, set_name, set_list)
        
        if "not found" in found_set:
            result = {'error': found_set}
        else:
            url = create_url(found_set, card_name)
            try:
                usd_price, usd_price_change, card_image = get_price_and_image(url)
                cad_price = round(usd_to_cad(usd_price), 2)
                cad_price_change = round(usd_to_cad(usd_price_change), 2)
                
                # Format price changes with proper +/- signs
                usd_change_formatted = f"+${abs(usd_price_change)}" if usd_price_change >= 0 else f"-${abs(usd_price_change)}"
                cad_change_formatted = f"+C${abs(cad_price_change)}" if cad_price_change >= 0 else f"-C${abs(cad_price_change)}"
                
                result = {
                    'url': url,
                    'usd_price': usd_price,
                    'usd_price_change': usd_price_change,
                    'usd_change_formatted': usd_change_formatted,
                    'cad_price': cad_price,
                    'cad_price_change': cad_price_change,
                    'cad_change_formatted': cad_change_formatted,
                    'language': language.title(),
                    'set_name': request.form.get('set_name', ''),
                    'card_name': request.form.get('card_name', ''),
                    'change_positive': usd_price_change >= 0,
                    'card_image': card_image
                }
            except Exception as e:
                result = {'error': 'Could not fetch price. Please check card name and set.'}
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)