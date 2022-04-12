from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
from model_ubcf_main import Recommendation

recommend = Recommendation()
SBPRS_app = Flask(__name__)  # intitialize the flaks app  # common 



@SBPRS_app.route('/', methods = ['POST', 'GET'])
def home():
    flag = False 
    data = ""
    if request.method == 'POST':
        flag = True
        reviews_username = request.form["User_id"]
        data=recommend.getTopProducts(reviews_username)
    return render_template('SBPRS_index.html', data=data, flag=flag)


if __name__ == '__main__' :
    SBPRS_app.run(debug=True)  # this command will enable the run of your flask app or api
    
    #,host="0.0.0.0")


    