from gpt3 import gpt3, gpt3_curie
from tkinter import *
from ctypes import windll
import threading
import time

windll.shcore.SetProcessDpiAwareness(1)             # For the GUI to make the text sharper/clearer

maxTokens = 300
Frame = Tk()

Frame.title("Article Writer")
# text entry box
entry = Text(Frame, width=40, height=5, wrap=WORD, exportselection=False)
entry.grid(column=0, row=2)
# keyword text entry box
keyEntry = Text(Frame, width=30, height=5, wrap=WORD, exportselection=False)
keyEntry.grid(column=1, row=2)
# Header text entry box
headerEntry = Text(Frame, width=30, height=5, wrap=WORD, exportselection=False)
headerEntry.grid(column=2, row=2)
# submit button
button1 = Button(Frame, text="Submit", command=lambda: button_click())
button1.grid(column=1, row=1)
# slider
slider = Scale(Frame, from_=0.00, to=1.00, orient=HORIZONTAL, resolution=0.01, label="Temperature")
slider.set(0.1)
slider.grid(column=1, row=3)
# keywords checkbox
keywords = Checkbutton(Frame, text="Keywords", variable="keyBool", onvalue=1, offvalue=0, width=8, height=5)
keywords.grid(column=1, row=4)
# Header checkbox
headers = Checkbutton(Frame, text="Headers", variable="headerBool", onvalue=1, offvalue=0, width=8, height=5)
headers.grid(column=2, row=4)
# HTML checkbox
HTML = Checkbutton(Frame, text="HTML", variable="HTMLBool", onvalue=1, offvalue=0, width=8, height=5)
HTML.grid(column=2, row=5)
# output text
output = Text(Frame, wrap=WORD, exportselection=False)
output.bind('<KeyRelease>', lambda event: make_suggestion(), add='+')        # Not being used
output.bind('<Alt_L>', lambda event: make_suggestion(), add='')
output.grid()
# translate button,
tb = Button(Frame, text="English", command=lambda: translate_English_click())
tb.grid(column=1, row=5)
# create translate button
tb = Button(Frame, text="Dutch", command=lambda: translate_Dutch_click())
tb.grid(column=1, row=6)


def add_tags(tag, word):
    return "<%s>%s</%s>" % (tag, word, tag)

def button_click():
    input = entry.get("1.0", 'end-1c')
    temperature = slider.get()
    maxTokens = 2000
    key_words = keyEntry.get("1.0", 'end-1c')
    header_list = headerEntry.get("1.0", 'end-1c').split(",")
    out = ""
    price = 0

    if keywords.getvar("keyBool") == 1 and key_words != "" and headers.getvar("headerBool") == 0:
        input = "Write an entire article consisting of 4 paragraphs on " + input + " in Dutch, using the following keywords: " + input + ", " + key_words
        print(input)
        out, price = gpt3(input, maxTokens, temperature)

    elif headers.getvar("headerBool") == 1:
        for header in header_list:
            if HTML.getvar("HTMLBool") == 1:
                header = add_tags(f"h2", header)
            input = "Write a long paragraph on " + header + "."
            outnew, price = gpt3(input, maxTokens, temperature)
            out = out + header + "\n" + outnew + "\n\n"
    else:
        out, price = gpt3(input, maxTokens, temperature)

    output.delete("1.0", END)
    output.insert('0.0', out)
    priceText = "Est. costs:", price, "$"


def save_in_output():
    pass


def translate_English_click():
    input = output.get("1.0", 'end-1c')
    temperature = slider.get()
    maxTokens = 2000
    prompt = "Translate the following into English:  " + input
    out, price = gpt3(prompt, maxTokens, temperature)
    output.delete("1.0", END)
    output.insert('1.0', out)


def translate_Dutch_click():
    input = output.get("1.0", 'end-1c')
    temperature = slider.get()
    maxTokens = 2000
    if headers.getvar("headerBool") == 1:
        out = ""
        header_list = headerEntry.get("1.0", 'end-1c').split(",")
        for header in header_list:
            input.split('\n')
            index = input.index(header) + 1
            paragraph = input[index]
            prompt = "Translate this paragraph about" + header + "to Dutch:\n" + paragraph
            outnew, price = gpt3(prompt, maxTokens, temperature)
            out = out + header + "\n\n" + outnew + "\n"
    else:
        prompt = "Translate the following into Dutch: " + input
        out, price = gpt3(prompt, maxTokens, temperature)


def get_output():
    return output.get("1.0", 'end-1c')


maxTokens1 = 50
def make_suggestion():
    text = get_output()
    if text != "":
        output.tag_delete("suggestion")
        print("text: " + text)
        suggestion, price = gpt3_curie(text, maxTokens1, slider.get())
        output.insert('end', suggestion, 'suggestion')
        output.tag_configure('suggestion', foreground='red')
        output.bind('<Tab>', lambda event: [output.tag_configure('suggestion', foreground='black'), lambda event: output.tag_delete('suggestion'),])
        output.bind('<Escape>', lambda event: [output.replace('1.0', 'end-1c', text), lambda event: output.tag_delete('suggestion')])
        output.mainloop()

# BETA: Timed suggestion function
# run_loop runs when a key is pressed, and it only runs run_loop2 when there has been no keys pressed for 2 seconds.
# Gets the suggestion from the model and updates the text box accordingly.
# Does this by adding the text suggestion in a different color and when tab is pressed, the suggestion is added

Frame.mainloop()
