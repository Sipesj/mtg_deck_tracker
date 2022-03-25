
import pandas as pd
import requests
import time
from cards import Card
from scipy.stats import hypergeom

class Decklist:

    def __init__(self):
        self.decklist = []
        self.advanced_decklist = []
        self.cards_in_deck = []
        self.cards_out_deck = []
        self.total_card_list = []
        self.categories = []
        self.land_draw_prb = ""
        self.nonland_draw_prb = ""
        self.hypergeom=0


    #takes the csv from Archidekt and converts it to a friendlier list of dicts
    #creates a second list of JSONs from scryfall API with more card info
    def get_deck(self, deck_csv):
        deck_contents = pd.read_csv(deck_csv, header=None)
        deck_contents.columns = ["Quantity", "Name", "Category"]
        deck_dict = deck_contents.to_dict()
        for card in deck_dict["Quantity"]:
            card_dict = {
                "Quantity": deck_dict["Quantity"][card],
                "Name": deck_dict["Name"][card],
                "Category": deck_dict["Category"][card]
            }
            self.decklist.append(card_dict)
        #get requests for each card from scryfall API
        for card in self.decklist:
            if card["Category"] != "Sideboard" and card["Category"] != "Maybeboard":
                params = {
                    "fuzzy": card["Name"],
                }
                response = requests.get(url="https://api.scryfall.com/cards/named", params=params)
                response.raise_for_status()
                card_data = response.json()
                card_data["category"] = card["Category"]
                if "produced_mana" not in card_data:
                    card_data["produced_mana"] = None
                if "oracle_text" not in card_data:
                    card_data["oracle_text"] = "working out the kinks with multi-cards"
            #creating a card object for each card in the deck
            for i in range(int(card["Quantity"])):
                new_data = card_data
                new_data["listbox_name"] = f"{card['Name']} {i+1}"
                new_card = Card(name=new_data["name"], image_uris=new_data["image_uris"]["small"], cmc=new_data["cmc"],
                                colors=new_data["colors"],
                                type_line=new_data["type_line"], produced_mana=new_data["produced_mana"],
                                oracle_text=new_data["oracle_text"],
                                category=new_data["category"], listbox_name=new_data["listbox_name"])
                if new_card.category != "Commander":
                    self.cards_in_deck.append(new_card)
                    self.total_card_list.append(new_card)

                else:
                    self.cards_out_deck.append(new_card)
                    self.total_card_list.append(new_card)
            time.sleep(.13)

        for card in self.total_card_list:
            if card.category not in self.categories:
                self.categories.append(card.category)

    #calculates statistics based on cards currently in deck
    def calc_stats(self, category, draw_count, amount_desired):
        population = len(self.cards_in_deck)
        lands_in_deck = 0
        category_in_deck = 0
        for card in self.cards_in_deck:
            if card.category == "Lands":
                lands_in_deck += 1
            if card.category == category:
                category_in_deck += 1
        self.land_draw_prb = (lands_in_deck / population) * 100
        self.nonland_draw_prb = 100 - self.land_draw_prb
        self.hypergeom = hypergeom.sf(amount_desired, population, category_in_deck, draw_count, loc=0)

    #functions to take card objects out of or put back into deck
    def put_card_in_deck(self, listbox_name):
        for card in self.cards_out_deck:
            if card.listbox_name == listbox_name:
                self.cards_out_deck.remove(card)
                self.cards_in_deck.append(card)

    def put_card_out_deck(self, listbox_name):
        for card in self.cards_in_deck:
            if card.listbox_name == listbox_name:
                self.cards_in_deck.remove(card)
                self.cards_out_deck.append(card)

    #acquire card object information to be shown on screen
    #this is done here because the listbox ui widget doesn't play nice with objects and is only a list of strings.
    def get_image_uri(self, listbox_name):
        for card in self.total_card_list:
            if card.listbox_name == listbox_name:
                return card.image_uris

    def get_oracle_text(self, listbox_name):
        for card in self.total_card_list:
            if card.listbox_name == listbox_name:
                return card.oracle_text

    def get_category(self, listbox_name):
        for card in self.total_card_list:
            if card.listbox_name == listbox_name:
                return card.category

    # def calc_stats(self, category, number_draws, desired_amount):
    #     population = len(self.cards_in_deck)
    #     lands_in_deck = 0
    #     category_in_deck = 0
    #     for card in self.cards_in_deck:
    #         if card.category == "Land":
    #             lands_in_deck += 1
    #         if card.category == category:
    #             category_in_deck += 1
    #     self.land_draw_prb = round((lands_in_deck / population) * 100)
    #     self.nonland_draw_prb = round(100 - self.land_draw_prb)
    #     self.hypergeom = round(hypergeom.sf(desired_amount - 1, population, category_in_deck, number_draws, loc=0)*100)



