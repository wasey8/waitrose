import requests 
from bs4 import BeautifulSoup
import numpy as np
from flask import Flask,render_template,url_for,request,jsonify
import json
from werkzeug.exceptions import HTTPException
app = Flask(__name__)



@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "error": "Something went wrong, check url again."
    })
    response.content_type = "application/json"
    return response

#-------Currency convert function---------#
def convert():
    url="https://www.google.com/search?q=aed+to+pkr+&sxsrf=ALeKk02To4yhBWpyI9HXCdFIBf4NCDTIXQ%3A1616665927504&ei=R11cYNSdHtOs1fAPidWquAk&oq=aed+to+pkr+&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBQgAEJECMgUIABCRAjIFCAAQsQMyCAgAEMkDEJECMgUIABCRAjICCAAyAggAMgIIADoHCAAQRxCwAzoGCAAQFhAeUMjTDlj54g5glOcOaAFwAngAgAGlA4gBhhWSAQgyLTEwLjAuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwiU3dDylcvvAhVTVhUIHYmqCpcQ4dUDCA0&uact=5"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    r = requests.get(url,headers)
    soup=BeautifulSoup(r.text,"html.parser")
    a=soup.find("div",{"class":"BNeawe iBp4i AP7Wnd"})
    a=a.text
    a=a[:-16]
    a=float(a)
    return a




#-----------------For waitrose categories---------!
@app.route("/waitrose",methods=['POST'])
def waitrose():
    url = request.form.get('url')
    rate=convert() 
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    r = requests.get(url, headers=headers)
    ab=[]
    soup =  BeautifulSoup(r.text, 'html.parser')
    count=0
    for i in soup.find_all("div",{"class":"c-ProductBox--width-100"}):
        products=i.find("h5",{"class","gill-sans-regular-20-18"}).text
        prices=i.find("span",{"span","[ gill-sans-regular-22-22 ] [ mb-5 ]"}).text
        images=i.find('img').attrs['src']
        products=products.strip()
        prices=prices.strip()
        prices=prices.strip('AED')
        prices=prices.strip(' ')
        prices=int(float(prices))
        prices=[prices]
        prices = [element *rate for element in prices]
        prices1 = [int(element *2.5/100) for element in prices]
        arr1 = np.array(prices)
        arr2 = np.array(prices1)
        prices= int(arr1 + arr2)
        prices=str(prices)
        INFO={
            'images':images,
            'title':products,
            'prices': prices
        }
        a=INFO['title'],INFO['images'],INFO['prices']
        count+=1
        ab.append(a)
    count={
        'products_count':count
    }
    for i in ab:
        return jsonify(count,ab)
    return jsonify(category_error="Something went wrong,make sure you're using correct endpoint for the category.")


if __name__ == "__main__":
    app.run(debug=True)

