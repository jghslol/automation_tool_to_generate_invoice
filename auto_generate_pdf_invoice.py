from fpdf import FPDF
import os
import webbrowser
import random
import json
from datetime import date

RANDOM_NUMBER = str(int("".join(map(str, random.sample(range(0, 100), 5)))))
DATE = str(date.today())

def get_product_item_description_and_amount():
    """
    Function to get user_input for product
    description and amount
    """
    amounts = []
    description_of_invoices = []

    add_description = input("Do you have a product to enter? If yes, type yes, else type no. ")

    while add_description != 'yes' and add_description != 'no':
        add_description = input("Do you have a product to enter? If yes, type yes, else type no. ")

    while add_description == 'yes':
        description = input('Put in a brief description of the products bought: ')
        amount = input('What is the amount of the item: ')

        if type(amount) == float:
            amounts.append(amount)

        while type(amount) != float:
            try:
                amount = float(amount)
                amounts.append(amount)
                break
            except (TypeError, ValueError):
                amount = input('What is the amount of the item, this must be a float: ')

        add_description = input("Do you have another product to enter? If yes, type yes. ")

        description_of_invoices.append(description)

    return {'amounts': amounts, 'description': description_of_invoices}


def read_data_file_for_invoice():
    """
    Function to read and return JSON
    data to create cells for PDF
    """
    f = open('data.json')
    data = json.load(f)
    return data


def create_cell_info_for_descriptions(description_for_invoice, amounts_for_invoice, pdf):
    """
    Function to create cells for descriptions and amounts of products input by user.
    """
    for description in description_for_invoice:
        index = description_for_invoice.index(description)
        pdf.cell(w=450, h=150, txt=description, border=1, align='C')
        pdf.cell(w=0, h=150, txt=str(amounts_for_invoice[index]), border=1, align='C', ln=1)

def create_cell_info_with_user_input(cell_info, total, pdf):
    """
    Function to create cells with user_input (generic)
    """
    user_input = {
        "insert_random_number": RANDOM_NUMBER,
        "insert_date": DATE,
        "insert_total": total
    }

    cell_info['txt'] = user_input[cell_info['txt']]
    pdf.cell(**cell_info)

def create_and_generate_invoice(filename, data_for_invoice, description_for_invoice, amounts_for_invoice, total):
    """
    Function to create and generate Invoice
    """
    pdf = FPDF(orientation='P', unit='pt', format='A4')
    pdf.add_page()
    pdf.set_fill_color(137, 207, 240)

    data = read_data_file_for_invoice()

    for cell_info in data:
        if 'family' in cell_info:
            pdf.set_font(**cell_info)
        elif "user_input" in cell_info['txt']:
            cell_info['txt'] = data_for_invoice[0]
            pdf.cell(**cell_info)
            data_for_invoice.remove(data_for_invoice[0])
        elif cell_info["txt"].startswith("insert"):
            create_cell_info_with_user_input(cell_info, total, pdf)
        elif cell_info["txt"] == "input_description_and_amount":
            create_cell_info_for_descriptions(description_for_invoice, amounts_for_invoice, pdf)
        else:
            pdf.cell(**cell_info)

    pdf.output(filename)
    webbrowser.open('file://' + os.path.realpath(filename))


read_data_file_for_invoice()
print('Hello - this is a command line tool to automatically generate an invoice for you based on certain parameters.')
print('You will now be asked a series of questions in order to populate the invoice to be generated.')

data_for_invoice = [input('What is your company name? '), input('What is the street address of your company? '),
                    input('What is the city, state and zip of your company? '), input('What is the phone number? '),
                    input('What is the client company name? '), input('What is the street address of the client? '),
                    input('What is the client city, state and zip? '), input('What is the client phone number? '),
                    input('What is the client email address? ')
                    ]

description_and_amount = get_product_item_description_and_amount()
amounts_for_invoice = description_and_amount["amounts"]
description_for_invoice = description_and_amount["description"]
total = str(sum(amounts_for_invoice))

create_and_generate_invoice('Invoice.pdf', data_for_invoice, description_for_invoice, amounts_for_invoice, total)


