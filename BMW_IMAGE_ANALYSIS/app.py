
import numpy as np
from flask import Flask, render_template, request, redirect,url_for

from keras.models import load_model
from keras.preprocessing import image
from IPython.display import display, HTML
import flask
import pandas as pd
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/mxp1pw2/Library/CloudStorage/OneDrive-TheHomeDepot/PycharmProjects/BMW_IMAGE_ANALYSIS/UploadFolder'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template("index.html")

@app.route('/uploads')
def uploads():
    page = request.args
    # bot = dict(page)["variable"][0]
    bot = dict(page)["variable"]
    bot2 = "/" + bot
    print("nnnnn", bot, bot2)
    return render_template("upload.html",bot="/"+bot)


@app.route('/CompleteAnalysis', methods=['GET', 'POST'])
def upload_file6():
    file = flask.request.files.getlist("file[]")
    model = load_model('Adessafinalmodels/newmodelcarsvsbmw.h5')
    model2 = load_model('Adessafinalmodels/bmw10_normal_rms_ep75.h5')
    model3 = load_model('Adessafinalmodels/my_model2.h5')

    # save the model to disk
    count=0
    output = []
    for i in file:
        count+=1
        test_image = image.load_img(i, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)

        if result[0][0] < 0.2:
            prediction = '0'
            me = "Its a BMW car"
        else:
            me = "Its NOT a BMW"
        filename = secure_filename(i.filename)
        output.append(filename)
        output.append(me)

        if(me == "Its a BMW car"):
            test_image = image.load_img(i, target_size=(64, 64))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = model2.predict(test_image)
            n = np.argmax(result)

            if n == 0:
                me1 = "Its BMW X series car"
            elif (n == 1):
                me1 = "Its BMW I series car"
            elif (n == 2):
                me1 = "Its BMW 3 series car"
            else:
                me1 = "Its BMW Alpina series car"

            #filename = secure_filename(i.filename)
            output.append(me1)
        else:
            me1 = "Can Predict only for BMW"
            output.append(me1)
        if (me == "Its a BMW car"):
            test_image = image.load_img(i, target_size=(150, 150))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = model3.predict(test_image)

            if result[0][0] < 0.9:
                # prediction = '0'
                me2 = "car surface is damaged"
            else:
                me2 = "this is good car"
            #filename = secure_filename(i.filename)
            output.append(me2)
        #print(output)
        else:
            me2 = "Can Predict only for BMW"
            output.append(me2)

    columns = [{"field": "ImageFileName", "title": "ImageFileName", "sortable": True},
               {"field": "Type Car Prediction", "title": "Type Car Prediction", "sortable": True},
               {"field": "Car Series Predictions", "title": "Car Series Predictions", "sortable": True},
               {"field": "Damage Prediction", "title": "Damage prediction", "sortable": True}]
    res = []
    l=0
    for m in range(count):
        b = {columns[0]["field"]:output[l],columns[1]["field"]:output[l+1],columns[2]["field"]:output[l+2],columns[3]["field"]:output[l+3]}
        l+=4
        res.append(b)



    return render_template("table.html",
                           data=res,
                           columns=columns,
                           title='Prediction Results')


@app.route('/CarDamage', methods=['GET', 'POST'])
def upload_file2():
    file = flask.request.files.getlist("file[]")   
    # model = load_model('Adessafinalmodels/my_model2.h5')
    model = load_model('/Users/mxp1pw2/Library/CloudStorage/OneDrive-TheHomeDepot/PycharmProjects/BMW_IMAGE_ANALYSIS/Adessafinalmodels/my_model2.h5')



    # save the model to disk
    output = {}
    for i in file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], i.filename)
        print("xxxxxxxx", i.filename, i, path)
        i.save(path)

        test_image = image.load_img(path, target_size=(64, 64))
        # test_image = image.load_img(i, target_size=(150, 150))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)

        if result[0][0] < 0.9:
            #prediction = '0'
            me="car surface is damaged"
        else:
            me="this is good car"
        filename = secure_filename(i.filename)
        output[filename] = me
    columns = [{"field": "ImageFileName", "title": "ImageFileName","sortable": True},{"field": "Damage Prediction","title": "Damage prediction","sortable": True}]
    res = []
    for key,val in output.items():
        b = {columns[0]["field"]:key,columns[1]["field"]:val}
        res.append(b)

    return render_template("table.html",
      data=res,
      columns=columns,
      title='Prediction Results')

@app.route('/CarAnalysis', methods=['GET', 'POST'])
def upload_file3():

    file = flask.request.files.getlist("file[]")
    # print("", os.getcwd(), os.path.join(os.path.dirname(__file__)+ '/UploadFolder', file))


    # file_name = os.path.dirname(__file__) + '\\Adessafinalmodels\\newmodelcarsvsbmw.h5'

    model = load_model('/Users/mxp1pw2/Library/CloudStorage/OneDrive-TheHomeDepot/PycharmProjects/BMW_IMAGE_ANALYSIS/Adessafinalmodels/newmodelcarsvsbmw.h5')
    # model = load_model('../BMW_IMAGE_ANALYSIS/Adessafinalmodels/newmodelcarsvsbmw.h5')

    # save the model to disk
    output = {}
    for i in file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], i.filename)
        print("xxxxxxxx", i.filename, i, path)
        i.save(path)

        test_image = image.load_img(path, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)

        if result[0][0] < 0.2:
            prediction = '0'
            me="Its a BMW car"
        else:
            me="Its NOT a BMW"
        filename = secure_filename(i.filename)
        output[filename] = me
		
    columns = [{"field": "ImageFileName", "title": "ImageFileName","sortable": True},{"field": "Type Car Prediction","title": "Type Car Prediction","sortable": True}]
    res = []
    for key,val in output.items():
        b = {columns[0]["field"]:key,columns[1]["field"]:val}
        res.append(b)

    return render_template("table.html",
      data=res,
      columns=columns,
      title='Prediction Results')

@app.route('/CarSeries', methods=['GET', 'POST'])
def upload_file():

    file = flask.request.files.getlist("file[]")
    model = load_model('Adessafinalmodels/bmw10_normal_rms_ep75.h5')
    output={}
    for i in  file:
        test_image = image.load_img(i, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        n = np.argmax(result)

        if n == 0:
            me = "Its BMW X series car"
        elif (n == 1):
            me = "Its BMW I series car"
        elif (n == 2):
            me = "Its BMW 3 series car"
        else:
            me = "Its BMW Alpina series car"
			
        filename = secure_filename(i.filename)
        output[filename] = me

    columns = [{"field": "ImageFileName", "title": "ImageFileName","sortable": True},{"field": "Car Series Predictions","title": "Car Series Predictions","sortable": True}]
    res = []
    for key,val in output.items():
        b = {columns[0]["field"]:key,columns[1]["field"]:val}
        res.append(b)

    return render_template("table.html",
      data=res,
      columns=columns,
      title='Prediction Results')

	  
if __name__ == '__main__':
    app.run(debug=True)
