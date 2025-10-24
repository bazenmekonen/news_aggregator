import os
import requests
from dotenv import load_dotenv
from tkinter import *
from tkinter import messagebox
import anthropic

root = Tk()
root.geometry("800x800")
root.title("News Aggregator")

input_label= Label()
input_text = Text(root, height=1, width=60)

text_var = StringVar()
text_var.set("Press for the news!")

load_dotenv()

news_key = os.getenv('NEWS_API_KEY')
claude_key = os.getenv('ANTHROPIC_API_KEY')

t = Text(root, height=20, width=60)
e = Entry(root, width=60, cursor="circle")
bb = Button(root, text="Submit", command=lambda:process_user_input(e))

client = anthropic.Anthropic()
e.pack(side=LEFT, pady=60)

def process_user_input(entry):
    try:
        user_input = entry.get()

        if not user_input.strip():
            messagebox.showwarning("Empty Input", "Please enter in input")

        result = give_urls(user_input)
        t.config(state="normal")
        t.delete("1.0", END)
        t.insert(END, result.content[0].text)
        t.config(state="disabled")
        print(result.usage)

    except Exception as e:
        print(f"Exception: {e}")

def give_urls(user_input):
    try:
        #url = f"https://newsapi.org/v2/top-headlines?country=us"
        url = f"https://newsapi.org/v2/everything?q={user_input}"
        header= {"X-Api-Key": news_key}
        #response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}")
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            data = response.json()

            message= client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Give me a 1 sentence summary for each of the articles in this json : {data}"
                    }
                ]
            )

            return message

            """t.config(state="normal")
            t.delete("1.0", END)
            t.insert(END, message.content[0].text)
            t.config(state="disabled")
            print(message.usage)
"""
        else:
            print("Didn't work")
    except Exception as e:
        print(f"Exception: {e}")


"""t = Text(root, height=20, width=60)
e = Entry(root, width=60, cursor="circle")
bb = Button(root, text="Submit", command=lambda:process_user_input())"""

label = Label(root, textvariable=text_var)
label.pack(pady=20)

#b = Button(root, textvariable=text_var, command=lambda:give_urls())
#b.pack(pady=50)

t.pack(pady=80)
bb.pack(side=LEFT,pady=60)


root.mainloop()
