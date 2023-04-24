from flask import Flask, request, render_template
import csv
import re
import os
import socket

#this script runs on PC take i/p data from user and send it to pi and pi will return the HEX data

TCP_IP = '192.168.137.226'  # replace with this ip of pc
TCP_PORT = 5005
BUFFER_SIZE = 1024
data = ''  # data that has to be sent

# Flask constructor
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('home.html')


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():

    lst_send = []
    data = request.form.get('data', False)

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((TCP_IP, TCP_PORT))
    # s.send(data)
    # received_data = s.recv(BUFFER_SIZE)
    # s.close()

    received_data = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    lst = re.findall('.{1,4}', received_data)
    lst_deci = [int(x, 16) for x in lst]
    lst_send.append(lst)
    lst_send.append(lst_deci)
    print("received data:", lst)

    return render_template('display.html', lst_ele=lst_send)


@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    return render_template('decode.html')


@app.route('/decode', methods=['GET', 'POST'])
def decode_file():
    deci_list = []
    if request.method == 'POST':
        if request.files:

            # storing the uploaded file in a directory
            uploaded_file = request.files['filename']
            file_path = os.path.join(
                app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(file_path)

            # reading hex digits from the uploaded file
            f = open(file_path, "r")
            bytes = f.read()
            list_hex = re.findall('.{1,4}', bytes)
            indx = list_hex.index('AABB')

            print(indx)
            print(len(list_hex))

            counter = 0
            temp_list = []
            list_ele = []

            for ele in range(indx, len(list_hex)):

                if list_hex[ele] == 'AABB' and counter in range(1, 29):
                    while counter < 30:
                        temp_list.append("Invalid Data")
                        counter += 1
                    list_ele.append(temp_list)
                    # print(list_ele)
                    temp_list = []
                    counter = 0

                if counter <= 29:
                    temp_list.append(list_hex[ele])
                    counter += 1
                    if counter == 29:
                        list_ele.append(temp_list)
                        # print(temp_list)
                        temp_list = []
                        counter = 0

            # print(list_ele)
            temp_list_2 = []

            for ele in list_ele:
                for i in ele:
                    if i == 'AABB' or i == 'Invalid Data':
                        temp_list_2.append(i)
                    else:
                        temp_list_2.append(int(i, 16))
                deci_list.append(temp_list_2)
                temp_list_2 = []

            # writing the decimal value data into a csv file
            myFile = open('data_decimal.csv', 'w')
            writer = csv.writer(myFile)
            for rows in deci_list:
                writer.writerow(rows)

            file_to_be_sent = open("data_decimal.csv", 'rb')
            # downloads the csv that has corresponding decimal value
            return render_template("display_file.html", cpl=deci_list)


if __name__ == '__main__':
    # create new directoy UPLOADED
    app.config['FILE_UPLOADS'] = os.getcwd() + "\\uploaded\\"
    app.run(debug=True)
