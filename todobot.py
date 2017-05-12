#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json 
import requests
import time
import six.moves.urllib as urllib
from dbhelper import DBHelper

TOKEN = "388030401:AAFNGf8onQ8KS2qFdZuWhE_dXwA8ISlFzb4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = DBHelper()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url) 


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_contactos(chat)
        if text == "/buscar":
            keyboard = build_keyboard(items)
            send_message("A quién buscas?", chat, keyboard)
        elif text == "/start":
            send_message("Epale, que necesitas?", chat)
        elif text.startswith("/agregar"):
            try:
                splitedText = text[8:].split("-")
                # message = str(len(splitedText))
                # send_message(message, chat)
                # db.add_item(chat, nombre, apellido, organizacion, nacionalidad, cedula, codarea, celular)
                db.add_item(chat, splitedText[0].strip(), splitedText[1].strip(), splitedText[2].strip(), splitedText[3].strip(), splitedText[4].strip(), splitedText[5].strip(), splitedText[6].strip())
                # message = "\n".join(splitedText)
                message = contact_for_review(splitedText)
                send_message(str(message), chat);
                send_message("Gracias por la info", chat);
                break
            except IndexError:
                print "Oops!  Not enough arguments.  Try again..."
                send_message("Si no sabes escribir te recomiendo pedir /ayuda", chat)
        elif text.startswith("/ayuda"):
                send_message("Para agregar a alguien utiliza el comando /agregar seguido de todos los valores separados por guiones\n\n" +
                    "/agregar nombre - apellido - organizacion - nacionalidad - cedula - codigo de area - celular" +
                    "\n\nSi necesitas informacion de tus contactos, escribe /buscar\n", chat)
        elif text in items:
            nombre = text.split()[0].strip()
            apellido = text.split()[1].strip()
            # print nombre + " - " + apellido
            contacto = db.get_info_contacto(chat,nombre,apellido)

            message = contact_for_display(contacto)
            send_message(str(message), chat);

            # message = contact_for_review(contacto)
            # send_message(str(message), chat);

        else:
            continue
        #     db.add_item(text, chat)
        #     items = db.get_contactos(chat)
        #     message = "\n".join(items)
        #     send_message(message, chat)

def contact_for_review(contacto):
    message = "Nombre: " + contacto[0]
    message = message +"\nApellido: " + contacto[1]
    message = message +"\nOrganizacion: " + contacto[2]
    message = message +"\nNacionalidad: " + contacto[3]
    message = message +"\nCedula: " + contacto[4]
    message = message +"\nCodigo de area: " + contacto[5]
    message = message +"\nTelefono: " + contacto[6]
    return message

def contact_for_display(contacto):
    message = contacto[1] + " " + contacto[2] + " (" + contacto[3] + ")"
    message = message +"\nCI: " + contacto[4] +"-"+contacto[5]
    message = message +"\nTelf: (" + contacto[6] +") "+contacto[7]
    return message


def build_keyboard(contactos):
    keyboard = [[item] for item in contactos]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        # time.sleep(0.5)

if __name__ == '__main__':
    main()
