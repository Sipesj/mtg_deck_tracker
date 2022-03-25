import io
from tkinter import *
from decklist_builder import Decklist
from PIL import ImageTk, Image
import urllib.request

class DeckTrackerInterface:

    def __init__(self):

        self.window = Tk()
        self.window.title("Deck Tracker")
        self.window.minsize(500,500)
        self.decklist = Decklist()
        self.decklist.get_deck(deck_csv="shu_yun_update.csv")

        self.left_frame = Frame(self.window)
        self.listbox_in_deck = Listbox(self.left_frame, width=40, activestyle="none", selectmode="single")
        self.listbox_in_deck.xview()
        self.listbox_list = [card.listbox_name for card in self.decklist.cards_in_deck]
        print(self.listbox_list.sort())
        for card in self.listbox_list:
            self.listbox_in_deck.insert(END, card)
        self.listbox_in_deck.bind("<<ListboxSelect>>", self.card_in_clicked)
        self.listbox_in_deck.grid(column=0, row=1)

        self.listbox_out_deck = Listbox(self.left_frame, width=40, activestyle="none", selectmode="single")
        self.listbox_out_deck.xview()
        self.listbox_out_deck.insert(END, self.decklist.cards_out_deck[0].listbox_name)
        self.listbox_out_deck.bind("<<ListboxSelect>>", self.card_out_clicked)
        self.listbox_out_deck.grid(column=1, row=1)

        self.label_in_deck = Label(self.left_frame, text="Cards currently in library")
        self.label_in_deck.grid(column=0, row=0)

        self.label_out_deck = Label(self.left_frame, text="Cards currently not in library")
        self.label_out_deck.grid(column=1, row=0)

        self.put_card_out_button = Button(self.left_frame, text=">>️", command=self.card_in_deck_button)
        self.put_card_out_button.grid(column=0, row=2)

        self.put_card_in_button = Button(self.left_frame, text="<<️️", command=self.card_out_deck_button)
        self.put_card_in_button.grid(column=1, row=2)

        self.card_image_canvas = Canvas(self.left_frame, bg="white", height=204, width=146,)
        self.card_image_canvas.grid(column=0, row=3, rowspan=2)

        self.oracle_text_label = Label(self.left_frame, text="", wraplength=200)
        self.oracle_text_label.grid(column=1, row=3)

        self.category_label = Label(self.left_frame, text="", wraplength=200)
        self.category_label.grid(column=1, row=4)

        self.left_frame.grid(column=0, row=0)

        self.right_frame = Frame(self.window)

        self.land_prb_label = Label(self.right_frame, text=f"{self.decklist.land_draw_prb}% chance to draw a land")
        self.land_prb_label.grid(column=0, row=0)

        self.nonland_prb_label = Label(self.right_frame, text=f"{self.decklist.nonland_draw_prb}%"
                                                              f" chance to draw a non-land")
        self.nonland_prb_label.grid(column=0, row=1)

        self.categories_title = Label(self.right_frame, text="Card Category")
        self.categories_title.grid(column=0, row=2)
        self.spinbox_categories = Spinbox(self.right_frame, value=self.decklist.categories)
        self.spinbox_categories.grid(column=0, row=3)

        self.desired_amount_title = Label(self.right_frame, text="Amount Desired")
        self.desired_amount_title.grid(column=1, row=2)
        self.spinbox_desired_amount = Spinbox(self.right_frame, from_=1, to_=99)
        self.spinbox_desired_amount.grid(column=1, row=3)

        self.number_draws_title = Label(self.right_frame, text="Drawing How Many Cards")
        self.number_draws_title.grid(column=2, row=2)
        self.spinbox_number_draws = Spinbox(self.right_frame, from_=1, to_=99)
        self.spinbox_number_draws.grid(column=2, row=3)

        self.calculate_button = Button(self.right_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(column=1, row=4)

        self.hypergeom_label = Label(self.right_frame, text="")
        self.hypergeom_label.grid(column=0, row=5)
        self.right_frame.grid(column=1, row=0)


        self.window.mainloop()



    def card_in_deck_button(self, *args):
        if self.listbox_in_deck.curselection() != ():
            selected_card = self.listbox_in_deck.get(ANCHOR)
            self.listbox_out_deck.insert(END, selected_card)
            self.decklist.put_card_out_deck(selected_card)
            self.listbox_in_deck.delete(ANCHOR)
            self.calculate()



    def card_out_deck_button(self, *args):
        if self.listbox_out_deck.curselection() != ():
            selected_card = self.listbox_out_deck.get(ANCHOR)
            self.listbox_in_deck.insert(END, selected_card)
            self.decklist.put_card_in_deck(selected_card)
            self.listbox_out_deck.delete(ANCHOR)
            self.calculate()

    def card_in_clicked(self, *args):
        selected_card = self.listbox_in_deck.get(int(self.listbox_in_deck.curselection()[0]))
        print(self.listbox_in_deck.curselection())
        image_uri = self.decklist.get_image_uri(selected_card)
        oracle_text = self.decklist.get_oracle_text(selected_card)
        category = self.decklist.get_category(selected_card)
        image_data = urllib.request.urlopen(image_uri).read()
        image = Image.open(io.BytesIO(image_data))
        self.photoimage = ImageTk.PhotoImage(image)
        self.card_image_canvas.create_image(73,102, image=self.photoimage)
        self.oracle_text_label.config(text=oracle_text)
        self.category_label.config(text=category)

    def card_out_clicked(self, *args):
        selected_card = self.listbox_out_deck.get(int(self.listbox_out_deck.curselection()[0]))
        print(self.listbox_out_deck.curselection()[0])
        image_uri = self.decklist.get_image_uri(selected_card)
        oracle_text = self.decklist.get_oracle_text(selected_card)
        category = self.decklist.get_category(selected_card)
        image_data = urllib.request.urlopen(image_uri).read()
        image = Image.open(io.BytesIO(image_data))
        self.photoimage = ImageTk.PhotoImage(image)
        self.card_image_canvas.create_image(73,102, image=self.photoimage)
        self.oracle_text_label.config(text=oracle_text)
        self.category_label.config(text=category)


    #decklist calculates stats any time the deck has changed or the hypergeometric dist to be tracked is
    #changed and initiated
    def calculate(self):
        category = self.spinbox_categories.get()
        desired_amount = int(self.spinbox_desired_amount.get())
        number_draws = int(self.spinbox_number_draws.get())
        self.decklist.calc_stats(category=category, number_draws=number_draws, desired_amount=desired_amount)
        self.land_prb_label.config(text= f"{self.decklist.land_draw_prb}% chance to draw a land")
        self.nonland_prb_label.config(text=f"{self.decklist.nonland_draw_prb}% chance to draw a non-land")
        self.hypergeom_label.config(text=f"{self.decklist.hypergeom}% chance to draw {desired_amount} "
                                         f"{category} cards in {number_draws} draws.")
