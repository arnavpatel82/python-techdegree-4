from models import (Base, session, Product, engine) 
import csv
import datetime


def clean_price(product_price):
    # example input: $4.30
    price = product_price[1:]
    price = float(price) * 100
    return (int(price))


def clean_date(date_updated):
    # example input: 11/1/2018
    return (datetime.datetime.strptime(date_updated, '%m/%d/%Y')) 


def add_csv():
    with open('inventory.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
        
            add = True

            if product_in_db != None:
                if product_in_db.date_updated >= date_updated:
                    
                    add = False
                else:
                    session.delete(product_in_db)
            
            if add:
                product_to_add = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)
                session.add(product_to_add)
                session.commit()
                    

def menu():
    print()
    print("------ MENU ------")        
    print('v - view the details of a single product in the database')
    print('a - add a new product to the database')
    print('b - make a backup of the database')
    print("------------------") 
    print()
    choice = input('> ')
    choice = choice.lower()
    while choice not in ['v', 'a', 'b']:
        print('Please only choose one of the options above')
        choice = input('> ')
    
    if choice == 'v':
        # view
        pass

    elif choice == 'a':
        # add
        pass

    else:
        # backup
        pass



if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    # add_csv()
    menu()