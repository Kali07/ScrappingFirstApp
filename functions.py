from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
import sqlalchemy as db
from sqlalchemy import inspect

class DataBase():
    def __init__(self, name_database='Kalihub'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()


    def create_table(self, name_table, **kwargs):
        columns = [db.Column(k, v) for k, v in kwargs.items()]
        table = db.Table(name_table, self.metadata, *columns)
        # Vérifiez si la table existe déjà
        insp = inspect(self.engine)
        if name_table in insp.get_table_names():
            table.drop(self.engine)
            
        table.create(self.engine, checkfirst=True)
        print(f"Table : '{name_table}' are created succesfully")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys:table.columns.keys()
        else : return table


    def add_row(self, name_table, **kwarrgs):
        name_table = self.read_table('Produits')

        stmt = (
            db.insert(name_table).
            values(kwarrgs)
        )
        self.connection.execute(stmt)
        print(f'Row id added')


    def delete_row_by_id(self, table, id_):
        name_table = self.read_table(name_table)

        stmt = (
            db.delete(name_table).
            where(students.c.id_ == id_)
            )
        self.connection.execute(stmt)
        print(f'Row id {id_} deleted')

    def select_table(self, name_table):
        name_table = self.read_table(name_table)
        stm = db.select([name_table])
        return self.connection.execute(stm).fetchall()
    
    def close_connection(self):
        self.connection.close()
        self.engine.dispose()
        print("Connection closed")


def scrape_data(n_page=5, time_sleep=1, progress_bar=None):
    database = DataBase('Kalihub')
        # Création d'un Tableau1
    database.create_table('Produits',
        id_product=db.Integer,                   
        categorie=db.Integer, 
        title=db.String, 
        price=db.String, 
        link=db.String,
        image=db.String,
        )
    
    # Configurez Selenium
    driver = webdriver.Chrome()
    driver.get("https://www.stmilitaria.com/408-armes")

    
    try:
        driver.find_element(By.ID, 'spm_receive_push_yes_button').click()
    except:
        pass

    # Liste pour stocker les données scrapées
    data_articles = []

    for n in range(1, n_page):
        driver.get(f'https://www.stmilitaria.com/408-armes?page={n}')
        sleep(time_sleep)
        articles = driver.find_elements(By.TAG_NAME, 'article')
        total_articles = len(articles)

        # Calculer le pourcentage de progression
        progress_percentage = (n / n_page) * 100

        # Mettre à jour la barre de progression

        for i, item in enumerate(articles):
            
            try:
                id_article = item.get_attribute('data-id-product')
            except:
                id_article = None
                
            try:
                title = item.find_element(By.CLASS_NAME, 'h3.product-title').text
            except:
                title = None

            try:
                price = item.find_element(By.CLASS_NAME, 'price').text
            except:
                price = None

            try:
                link = item.find_element(By.CLASS_NAME, 'thumbnail.product-thumbnail').get_attribute('href')
            except:
                link = None

            try:
                image = item.find_element(By.CLASS_NAME, 'ml-0.img-fluid').get_attribute('src')
            except:
                image = None
                
            progress_percentage = (n - 1 + (i + 1) / total_articles) / n_page * 100

            if progress_bar:
                progress_bar.progress(progress_percentage / 100)
            
            data_articles.append({
                'id_article':id_article,
                'title': title,
                'price': price,
                'link': link,
                'image': image
            })
            database.add_row(
                'Produits',
                id_product=str(random.randint(10000, 1000000)),
                categorie=id_article,
                title=title,
                price=price,
                link=link,
                image=image,

        )
    database.close_connection()
    driver.quit()
    return data_articles
