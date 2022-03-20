import os

from serpapi import GoogleSearch

from flask import Flask, request, render_template
from google.cloud import vision

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shortenurl', methods=['GET', 'POST'])
def shortenurl():
    send = ""
    if request.method == 'POST':
        definitionsstring = "Definiton: "
        liststring = ""
        otherlist = ""
        shortcode = request.form['shortcode']
        params = {
            "q": shortcode,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "api_key": "018bb90a10cda230d8e8abd53dcada5fc928f2fef2e86e6f27b39939655eec11"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "knowledge_graph" in results:
            knowledgetitlenest = results["knowledge_graph"]
            if "description" in knowledgetitlenest:
                description = knowledgetitlenest["description"]
                if " &horbar; Google" in description:
                    description = description.replace(" &horbar; Google", "", 1)
                send = description
            elif len(list(knowledgetitlenest.values())[0]) > 2:
                k = 0
                listvalues = list(knowledgetitlenest.values())[0]
                for value in listvalues:
                    city = value["name"]
                    liststring = liststring + city
                    k = k+1
                    if k==5:
                        break
                    liststring = liststring + ", "
                send = liststring
        elif "answer_box" in results:
            answerboxnest = results["answer_box"]
            if answerboxnest["type"] == "organic_result":
                if "snippet" in answerboxnest:
                    if "list" in answerboxnest:
                        j = 0
                        snippetlist = answerboxnest["list"]
                        for i in snippetlist:
                            otherlist = otherlist + i
                            j = j+1
                            if j == 5:
                                break
                            otherlist = otherlist + ", "
                        send = otherlist
                    else:
                        snippet = answerboxnest["snippet"]
                        send = snippet
                elif "answer" in answerboxnest:
                    answer = answerboxnest["answer"]
                    send = answer
            elif answerboxnest["type"] == "dictionary_results":
                definitions = answerboxnest["definitions"]
                for definition in definitions:
                    definition = definition.replace(".", "", 1)
                    definitionsstring = definitionsstring + definition + ", "
                send = definitionsstring
            elif answerboxnest["type"] == "calculator_result":
                result = answerboxnest["result"]
                send = result
            elif answerboxnest["type"] == "translation_result":
                targettext = answerboxnest["translation"]["target"]["text"]
                send = targettext
        else:
            send = "no results, please try again"
        return render_template('upload_image.html', shortcode=send)
    elif request.method == 'GET':
        return 'A GET request was made'
    else:
        return 'Not a valid request method for this route'

if __name__ == "__main__":
    app.run()
