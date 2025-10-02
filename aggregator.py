import os
import requests
from dotenv import load_dotenv
from tkinter import *
import anthropic

root = Tk()
root.geometry("600x600")
root.title("News Aggregator")

text_var = StringVar()
text_var.set("Press for the news!")

load_dotenv()

news_key = os.getenv('NEWS_API_KEY')
claude_key = os.getenv('ANTHROPIC_API_KEY')

t = Text(root, height=20, width=60)

client = anthropic.Anthropic()



def give_urls():
    try:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}")
        if response.status_code == 200:
            data = response.json()

            message= client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Give me a 1 sentence summary for each of the articles in this json : {data}"
                    }
                ]
            )

            t.config(state="normal")
            t.delete("1.0", END)
            t.insert(END, message.content)
            t.config(state="disabled")
            """articles = data['articles']
            t.config(state="normal")
            t.delete("1.0", END)
            #urls = [item['url'] for item in data['data']]
            #label_two['text'] = '\n'.join(urls)
            for article in articles:
                title = article.get('title', 'No title')
                url = article.get('url', 'No url')

                t.insert(END, f"Title: {title}\n")
                t.insert(END, f"Url: {url}\n")

            
            t.config(state="disabled")"""
        else:
            print("Didn't work")
    except Exception as e:
        print(f"Exception: {e}")




label = Label(root, textvariable=text_var)
label.pack(pady=20)

b = Button(root, textvariable=text_var, command=lambda:give_urls())
b.pack(pady=50)

t.pack(pady=60)


root.mainloop()
