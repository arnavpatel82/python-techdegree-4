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

            if product_in_db != None:
                if product_in_db.date_updated < date_updated:
                    product_in_db.product_name = product_name
                    product_in_db.product_price = product_price
                    product_in_db.product_quantity = product_quantity
                    product_in_db.date_updated = date_updated
                    print('product already in database, information updated')
            else:
                product_to_add = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)
                session.add(product_to_add)
            
            session.commit()
            
                    
def view():
    available_ids = []
    for product in session.query(Product):
            available_ids.append(product.id)

    print(f'Available IDs: \n{available_ids}')
    id_choice = input('>')

    while not id_choice.isdigit() or int(id_choice) not in available_ids:
        print()
        print('Please only choose one of the IDs above')
        id_choice = input('>')
    
    print()
    chosen_product = session.query(Product).filter_by(id=id_choice).first()
    print("------------------") 
    print(f'Name: {chosen_product.product_name}')
    print(f'Quantity: {chosen_product.product_quantity}')
    print(f'Price: ${chosen_product.product_price / 100}')
    print(f"Date Updated: {chosen_product.date_updated.strftime('%m/%d/%Y')}")
    print("------------------") 


def add():
    product_name = input('Name: ')
    print()
    product_in_db = session.query(Product).filter(Product.product_name==product_name).one_or_none()

    product_quantity = input('Quantity: ')
    print()
    while not product_quantity.isdigit():
        print('quantity must be a whole number')
        product_quantity = input('Quantity: ')
        print()
    
    while True:
        try:
            product_price = input('Price: ')
            print()
            product_price = '$' + product_price
            product_price = clean_price(product_price)
            break
        except ValueError:
            print("price must be a number such as: '15' or '15.99'")

    while True:
        try:
            date_updated = input('Date Updated: ')
            print()
            date_updated = clean_date(date_updated)
            break
        except ValueError:
            print('date updated must be in this format --> MM/DD/YYYY')

    if product_in_db != None:
        if product_in_db.date_updated < date_updated:
            product_in_db.product_name = product_name
            product_in_db.product_price = product_price
            product_in_db.product_quantity = product_quantity
            product_in_db.date_updated = date_updated
            print('product already in database, information updated')
    else:
        product_to_add = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)
        session.add(product_to_add)
        print('Product added')

    session.commit()

    
def menu():
    print()
    print("------ MENU ------")        
    print('v - view the details of a single product in the database')
    print('a - add a new product to the database')
    print('b - make a backup of the database')
    print("------------------") 
    print()
    choice = input('>')
    print()
    choice = choice.lower()
    while choice not in ['v', 'a', 'b']:
        print('Please only choose one of the options above')
        choice = input('> ')
        print()

    if choice == 'v':
        view()
        input('press enter to return to menu')

    elif choice == 'a':
        add()
        input('press enter to return to menu')

    else:
        # backup
        pass



if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    # add_csv()
    while True:
        menu()