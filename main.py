#!usr/bin/env python3

from brain_cards import *
from tkinter import *
from tkinter import messagebox


def main():
    start()


def start():
    window = Tk()
    box = CardBox()

    def learn():
        cards = box.learn_cards()
        ind = 0
        str_count = str(len(cards))
        for card in cards:
            ind += 1
            title = str(ind) + '/' + str_count
            show_card(card, title)
        box.save_cards()

    def add_card():
        add_window = Tk()
        add_window.title("Новая карточка*")
        add_window.geometry('340x130')

        word_lbl = Label(add_window, text="Слово:")
        word_lbl.grid(column=0, row=2, sticky=W, padx=5, pady=5)

        word_value = Entry(add_window, width=40)
        word_value.insert(0, '')
        word_value.grid(column=1, row=2, sticky=W, pady=5)

        translation_lbl = Label(add_window, text="Перевод:")
        translation_lbl.grid(column=0, row=3, sticky=W, padx=5, pady=5)

        translation_value = Entry(add_window, width=40)
        translation_value.insert(0, '')
        translation_value.grid(column=1, row=3, sticky=W)

        association_lbl = Label(add_window, text="Ассоциация:")
        association_lbl.grid(column=0, row=4, sticky=W, padx=5, pady=5)

        association_value = Entry(add_window, width=40)
        association_value.insert(0, '')
        association_value.grid(column=1, row=4, sticky=W)

        def save_card():
            word = word_value.get()
            translation = translation_value.get()
            association = association_value.get()

            new_card = Card(word=word, translation=translation, association=association)
            if not new_card:
                messagebox.showinfo('Ошибка', 'Не удалось создать карточку!')
                return
            if not box.add_card(new_card):
                messagebox.showinfo('Повтор', 'Карточка с таким словом уже существует!')
                return

            word_value.delete(0, END)
            translation_value.delete(0, END)
            association_value.delete(0, END)

        save_btn = Button(add_window, text='Сохранить', command=save_card)
        save_btn.grid(column=0, row=5, columnspan=2, padx=20, pady=5)

        add_window.mainloop()

    def show_card(card, title):
        card_window = Tk()
        card_window.title("Карточка " + title)
        card_window.geometry('320x100')

        word_lbl = Label(card_window, text='Слово:')
        word_lbl.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        word_value = Entry(card_window, width=40)
        word_value.insert(0, card.get_heads())
        word_value.grid(column=1, row=0, sticky=W, pady=5)

        translation_lbl = Label(card_window, text="Перевод:")
        translation_lbl.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        translation_value = Entry(card_window, width=40)
        translation_value.insert(0, '')
        translation_value.grid(column=1, row=1, sticky=W)

        def check_card():
            translation = translation_value.get()
            if not card.check_word(translation):
                messagebox.showinfo('Ассоциация', card.get_tails())
            card_window.destroy()
            card_window.quit()

        save_btn = Button(card_window, text='Проверить', command=check_card)
        save_btn.grid(column=0, row=2, columnspan=2, padx=20, pady=5)

        card_window.mainloop()

    window.title("BrainCards")
    window.geometry('250x105')

    menu = Menu(window)
    menu.add_command(label='Добавить...', command=add_card)

    window.config(menu=menu)

    btn_start = Button(window, width=30, height=5, text='Начать', command=learn)
    btn_start.grid(column=4, row=0, padx=15, pady=10)

    window.mainloop()


if __name__ == '__main__':
    main()
