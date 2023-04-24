from flask import Flask, request, render_template, jsonify, send_file, send_from_directory
import serial
import csv
import time
import re
import json
import os


# port = "\\.\COM4"
# baudrate = 19200
# parity=serial.PARITY_NONE
# no=serial.EIGHTBITS
# stopbits= serial.STOPBITS_ONE
# ser=serial.Serial()
# ser.port=port
# ser.baudrate=baudrate
# ser.timeout=1
# ser.parity=parity
# ser.bytesize=no
# ser.stopbits=stopbits

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['GET' , 'POST'])
def from_pi():

    text = request.form.get('text', False)

    if request.method == "POST":
        return render_template("decode.html")

    return render_template('home.html')


@app.route('/fetch_data' , methods = ['GET' , 'POST'])
def fetch_data():
    lst = list()
    # ser.open()
    # time.sleep(1)
    # time.sleep(1)
    # ser.setDTR(level=0)
    # time.sleep(1)
    # ser.write(text)
    # bytes=ser.read(124)
    #test case

    with open('file.txt' , 'r') as infile:
         
        bytes = infile.read(124)
        #outfile.write(infile.read()[124:])

    #bytes = "AABB6F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F166F16"

    if len(lst) != 0:
        lst.clear()
    lst = re.findall('.{1,4}', bytes)
    current_time = time.strftime("%H:%M:%S")
    #lst.append(current_time) 

    #writing data into CSV
    f = open('data.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(lst)
    f.close()

    #ser.close()
    return jsonify(lst)

@app.route('/decode',  methods = ["GET" , "POST"])
def decode():
    deci_list = []
    if request.method == 'POST':
        if request.files:

            #storing the uploaded file in a directory
            uploaded_file = request.files['filename'] 
            file_path = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(file_path)

            #reading hex digits from the uploaded file
            f = open(file_path, "r")
            bytes = f.read()
            list_hex = re.findall('.{1,4}', bytes)
            indx = list_hex.index('AABB')
            
            print(indx)
            print(len(list_hex))

            counter = 0
            temp_list = []
            list_ele = []
            
            for ele in range(indx , len(list_hex)):

                if  list_hex[ele] == 'AABB' and counter in range(1,29):
                    while counter < 30:
                        temp_list.append("Invalid Data")
                        counter += 1
                    list_ele.append(temp_list)
                    #print(list_ele)
                    temp_list = []
                    counter = 0

                if counter <=29:
                    temp_list.append(list_hex[ele])
                    counter += 1
                    if counter == 29:
                        list_ele.append(temp_list)
                        #print(temp_list)
                        temp_list = []
                        counter = 0

            #print(list_ele)
            temp_list_2 = []

            for ele in list_ele:
                for i in ele:
                    if i == 'AABB' or i == 'Invalid Data':
                        temp_list_2.append(i)
                    else:
                        temp_list_2.append(int(i,16))
                deci_list.append(temp_list_2)
                temp_list_2 = []

            #writing the decimal value data into a csv file
            myFile = open('data_decimal.csv', 'w')
            writer = csv.writer(myFile)
            for rows in deci_list:
                writer.writerow(rows)

            file_to_be_sent = open("data_decimal.csv", 'rb')
            #downloads the csv that has corresponding decimal value
            return render_template("display.html" , cpl = deci_list)
            #return send_file(file_to_be_sent, as_attachment=True, mimetype="text/csv", attachment_filename = 'decimal_data.csv'  , cache_timeout=0)


if __name__ == '__main__':
    #create new directoy UPLOADED
    app.config['FILE_UPLOADS'] = os.getcwd() + "\\uploaded\\"
    app.run(debug=True)


