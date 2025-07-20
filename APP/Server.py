from flask import Flask, render_template, request, flash, jsonify, render_template_string
import os, json, datetime, csv, re

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify("Salut")

@app.route("/receive_data/", methods=["POST"])
def receive_data():
    data = request.get_json()

    try:
        # Extract the data sent
        id_user = data["ID"]
        date_user = data["date"]
        date_receive = datetime.datetime.now().strftime("%X %x")
        message = data["message"]
        destination = data["to"]
        if int(id_user) != int(destination):
            traitement_data_receive_json([id_user, date_user, date_receive, message, destination])
            logs_CSV([id_user, date_user, date_receive, message, destination,"GOOD"])
        else:
            logs_CSV([id_user, date_user, date_receive, message, destination, "ERROR (same ID & Destination)"])
            return jsonify({"status":"ERROR - Your ID and destination it's same"})
        return jsonify({"status": "receive"})

    except:
        logs_CSV([id_user, date_user, date_receive, message, destination, "ERROR"])
        return jsonify({"status":"Data in not valid"})

def traitement_data_receive_json(data: list): #Stockage de la conversation
        ID, to = data[0], data[4]
        data_message_dico = {
            "ID": data[0],
            "date_user": data[1],
            "date_receive": data[2],
            "message": data[3],
            "to": data[4]
        }

        if int(ID) > int(to):
            filename = fr".\stockage\{ID}_{to}_CONV.json"
        else:
            filename = fr".\stockage\{to}_{ID}_CONV.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # On ajoute le nouveau message
        data.append(data_message_dico)

        # On réécrit tout le fichier avec la liste mise à jour
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/get_data/<conv>/<key>", methods=["GET"])
def get_data(conv, key):
    with open(r'.\stockage\Access.json','r') as f:
        access = json.load(f)
        access = access[0]

    if key in access:
        if re.fullmatch(r'^\d+_\d+$', conv):
            c1= str(conv).split("_")[0]
            c2 = str(conv).split("_")[1]
            liste_conv = access[key].split(",")
            if f"{c1}_{c2}" in liste_conv:
                filename = fr".\stockage\{c1}_{c2}_CONV.json"
                if os.path.exists(filename):
                    with open(filename,'r') as r:
                        all_conv = json.load(r)
                    logs_sending_CSV(key, f"Request sucessfull for : {conv}", datetime.datetime.now().strftime("%X %x"))
                    return jsonify((all_conv))
                else:
                    logs_sending_CSV(key, "Conversation not exist", datetime.datetime.now().strftime("%X %x"))
                    return jsonify({"status": "This conversation not exist"})
            else:
                logs_sending_CSV(key, f"Tentative on {conv}, not access", datetime.datetime.now().strftime("%X %x"))
                return jsonify({"status": f"You don't have access for this conversation, attempt is report AAA{{liste_conv}}"})
        else:
            return jsonify({"status": "error"})
    else:
        logs_sending_CSV(key, "This key note exist", datetime.datetime.now().strftime("%X %x"))
        return jsonify({"status": "You key's isn't valable"})


@app.route("/conv_key/<string:key>")
def key_to_conv(key):
    with open(r'.\stockage\Access.json','r') as f:
        access = json.load(f)
        access = access[0]

    if key in access:
        return jsonify({"Conv": access[key] })
    else:
        return jsonify({"Status":"This key no access"})


@app.route("/send_chat")
def send_chat():
    pass


def logs_CSV(data: list):
    ID, to = data[0], data[4]
    if int(ID) > int(to):
        filename = fr".\stockage\{ID}_{to}_LOGS.csv"
    elif int(ID) < int(to):
        filename = fr".\stockage\{to}_{ID}_LOGS.csv"
    elif int(ID)==int(to):
        filename = fr".\stockage\ERROR-SAME_LOGS.csv"

    with open(filename, "a", newline='') as f:
        (csv.writer(f)).writerow(data)


def logs_sending_CSV(key, message, date):
    with open(fr".\stockage\send_error.csv", "a", newline='') as f:
        data = [key, message, date]
        (csv.writer(f)).writerow(data)


if __name__ == '__main__':
    app.run(port=1000)