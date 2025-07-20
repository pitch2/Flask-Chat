from flask import Flask, render_template, request, flash, jsonify, render_template_string, session, make_response
import os, json, datetime, csv, re, requests

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zec]/'


@app.route("/")
def index():
    return render_template_string("Bonjour")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        coo_key = request.form.get('key')
        session['key'] = coo_key

        return render_template("list_conversations.html", list_conversations=keep_conv(coo_key), key=coo_key)

    return '''
        <form method="post">
            <p><input type="password" name="key" placeholder="Your KEY">
            <p><input type="submit" value="Sent">
        </form>
    '''

def keep_conv(key):
    return json.loads(requests.get(fr"http://127.0.0.1:1000/conv_key/{key}").text)["Conv"].split(",") # -> renvoie une liste



if __name__ == '__main__':
    app.run(port=2000)


'''
data = {
    "conv": "995_789",
    "key": "3uLRF0GpifPqRK19nmS0p3QQ/upYvdSERwRrsb4C3N8="
}

response = requests.request(
    method="GET",
    url="http://localhost:1000/get_data/",
    headers={"Content-Type": "application/json"},
    data=json.dumps(data)
)

print("Status:", response.status_code)
print("Response:", response.json)
'''
