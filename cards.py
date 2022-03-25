class Card:
    def __init__(self, name, image_uris, cmc, colors, type_line, produced_mana, oracle_text, category, listbox_name):
        self.name = name
        self.image_uris = image_uris
        self.cmc = cmc
        self.colors = colors
        self.type_line = type_line
        self.produced_mana = produced_mana
        self.oracle_text = oracle_text
        self.category = category
        self.listbox_name = listbox_name

