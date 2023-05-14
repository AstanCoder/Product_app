
# coding=<UTF-8>
from tkinter import ttk
from tkinter import *

import sqlite3


class Product:
    
    db_name = 'database.db'
    
    
    
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Product Aplication')
        # Frame Container
        frame = LabelFrame(self.wind, text = 'Registra un nuevo proucto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        # Name Input
        Label(frame, text = 'Name: ').grid(row = 0, column = 0)
        self.name = Entry(frame)
        self.name.focus() #ENFOCAR CURSOR
        self.name.grid(row = 0, column = 1)
        
        # Price input
        Label(frame, text = 'Price: ').grid(row = 1, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 1, column = 1)
        
        #Currency input
        Label(frame, text = 'Currency: ').grid(row = 2, column = 0)
        self.currency = Entry(frame) 
        self.currency.grid(row = 2, column = 1)
               
        # Add Product Button
        ttk.Button(frame, text = "Save Product", command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        
        # About Button
        ttk.Button(frame, text = "About", command = self.about).grid(row = 4, columnspan = 2, sticky = W + E)
        
        #Delete product Button
        ttk.Button(text = 'Delete', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        
        #Edit product Button
        ttk.Button(text = 'Edit', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)
        
        
        #Output messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        
        # Table
        self.tree = ttk.Treeview(self.wind, height = 10, columns = [f"#{n}" for n in range(1, 4)])
        self.tree.config(show='headings')
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#1', text = 'Name', anchor = CENTER)
        self.tree.heading('#2', text = 'Price', anchor = CENTER)
        self.tree.heading('#3', text = 'Currency', anchor = CENTER)
        
        self.get_products()
        
    def run_query(self, query, parameters = ()): 
        with sqlite3.connect(self.db_name) as conn: 
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result           
        
    def get_products(self):
        
        #Cleaning Table
        records = self.tree.get_children()
        for element in records: 
            self.tree.delete(element)
            
        #Consulting data    
        query = 'SELECT * FROM product ORDER BY name DESC' 
        db_rows = self.run_query(query)
        
        #Filling Data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = (row[1],row[2],row[3])) 
            
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

            
    def add_product(self): 
        if self.validation(): 
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?)' 
            parameters = (self.name.get(), self.price.get(), self.currency.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.currency.delete(0, END)
        else: 
            self.message['text'] = 'Name and Price are Required'
        self.get_products()
        
    
    def delete_product(self): 
        self.message['text'] = ''
        try: 
            self.tree.item(self.tree.selection())['text'][0]         
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} has been deleted successfully'.format(name)
        self.get_products()
        
    def edit_product(self): 
        self.message['text'] = ''
        
        try: 
            self.tree.item(self.tree.selection())['text'][0]       
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][1]  
        currency = self.tree.item(self.tree.selection())['values'][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Product')
        
        #Old Name
        Label(self.edit_wind, text = 'Old Name: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        
        
        #New Name
        Label(self.edit_wind, text = 'New Name: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)
        
        #Old price
        Label(self.edit_wind, text = 'Old Price: ').grid(row = 0, column = 3)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 0, column = 4)
        
        #New Price
        Label(self.edit_wind, text = 'New Price: ').grid(row = 1, column = 3)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 1, column = 4)
        
        #Currency
        Label(self.edit_wind, text = 'Currency: ').grid(row = 0, column = 5)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = currency), state = 'readonly').grid(row = 0, column = 6)
        
        #New currency
        Label(self.edit_wind, text = 'New Currency: ').grid(row = 1, column = 5)
        new_currency = Entry(self.edit_wind)
        new_currency.grid(row = 1, column = 6)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price, currency, new_currency.get())).grid(row = 4, column = 2, sticky = W + E )
        
    def edit_records(self, new_name, name, new_price, old_price, currency, new_currency): 
        query = 'UPDATE product SET name = ?, price = ?, currency = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, new_currency, name, old_price)
        if new_name == '' or new_price == '':
            self.message['text'] = 'Por favor, rellene todos los Campos'
            self.edit_wind.destroy()
        else: 
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Record {} was successfully Updated'.format(name)
            self.get_products()
        
    def about(self):  
        self.message['text'] = ''
        self.about_wind = Toplevel()
        self.about_wind.title('About')
        
        frame = LabelFrame(self.about_wind, text = 'About: ')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        Label(frame, text = "Product_app is an application to easily count and store products in a database").grid(row = 2, columnspan = 2, sticky = W + E)
        Label(frame, text = "Version: WinOS.0.1.3").grid(row = 4, columnspan = 2, sticky = W + E)
        Label(frame, text = "This app was made on Python, runs on any 64bit Windows System").grid(row = 6, columnspan = 2, sticky = W + E)
       # ttk.Button(frame, text = 'Close', command = self.about_wind.destroy()).grid(row = 6, columnspan = 2) ## TclError: bad window path name
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()


 
    































