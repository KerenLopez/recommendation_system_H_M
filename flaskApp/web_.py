from flask import Flask, render_template, request, redirect,send_from_directory,url_for
import pandas as pd
from model import doRecommendations
from jinja2 import Environment, FileSystemLoader


app = Flask(__name__, static_folder='static')
app.config["DEBUG"] = True

pathMerged = 'merged.csv'
df_clientsAndPurchases = pd.read_csv(pathMerged)
df_clientsAndPurchases = df_clientsAndPurchases.drop("Unnamed: 0", axis=1)

# Ruta de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        return redirect('/home?username={}'.format(username))

    return render_template('login.html')


@app.route('/home', methods=['GET'])
def home():
    userID = request.args.get('username')

    model = doRecommendations()
    df_recomended, df_client = model.recommendation(userID)
    df_purchased = model.purchasedArticles(df_client)
    #tabla_html1 = df_purchased.to_html()
    #tabla_html2 = df_recomended.to_html()
    # Preprocess the data
    purchasedItems = list(zip(getImages(df_purchased), getDescriptions(df_purchased)))
    recommendedItems = list(zip(getImages(df_recomended), getDescriptions(df_recomended)))

    # Configure Jinja2
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('home.html')
    return template.render(purchasedItems=purchasedItems, recommendedItems=recommendedItems)

def getImages(df):
    images = []
    for i in range(10, 96):
      numero_formateado = str(i).zfill(2)
      images.append(numero_formateado)
    articlesIds = df['article_id'].values.tolist()
    paths = []
    for i in articlesIds:
        path = ''
        num = str(i)
        first2digits = num[:2]
        if first2digits in images:
            path = url_for('serve_image', filename="0" + first2digits + "/0" + num[:9] + ".jpg")
            paths.append(path)
    return paths

def getDescriptions(df):
    descriptions = []
    productsNames = df['prod_name'].values.tolist()
    productsTypes = df['product_type_name'].values.tolist()
    productsGroups = df['product_group_name'].values.tolist()
    for i in range(0,len(productsNames)): 
        description = "<b>"+productsNames[i]+"</b>"+"<br>"+productsTypes[i]+"<br>"+productsGroups[i]
        descriptions.append(description)
    return descriptions

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder + '/images', filename)


app.run()