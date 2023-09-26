import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import ImageFont


def AllSales():
    tree.delete(*tree.get_children()) 
    table = viewfiledefault()
    ConstructColumn(table)
    
    viewfile = mycursor.execute("SELECT * FROM viewfile;").fetchall()
    length=len(viewfile)
    for k in range(length):
        RoundPrice(k, 14, viewfile)
        tree.insert("",'end',values=viewfile[k])
          
def head():
    global head_state 
    head_state =1     
    iid = tree.get_children()
    length = len(tree.get_children())-10
    if(0 < length):
        for i in range(length):
            tree.delete(iid[i+10])
            
def Sum():
    if(tree.item(tree.get_children()[0])['values'] == ""):
        print("View is empty. ")
    else:
        print(head_state)
        
        if(head_state == 0):
            print(mycursor.execute("SELECT SUM(`Unit Price` -(`Unit Cost` * (1-`Discount Applied`))) AS 'sum' FROM viewfile;").fetchall()[0][0])
        else: 
            mycursor.execute("DROP VIEW IF EXISTS sumview;")
            mycursor.execute("CREATE VIEW IF NOT EXISTS sumview AS SELECT * FROM 'viewfile' LIMIT 10;")
            print(mycursor.execute("SELECT SUM(`Unit Price` -(`Unit Cost` * (1-`Discount Applied`))) AS 'sum' FROM sumview;").fetchall()[0][0])
        
        
    
def subcommand_determine(event):
    button = command_var.get()
    
    if(button == command_list[0]):
        subcommand_routine(0)      
    elif(button == command_list[1]):
        subcommand_routine(1)
    elif(button == command_list[2]):
        subcommand_routine(2)
    elif(button == command_list[3]):
        subcommand_routine(3)            
 

def subcommand_routine(index):
    subcommand_drop["values"] = subcommand_list[index]
    subcommand_drop.set(subcommand_list[index][0])     
  
def submit():
    command = command_var.get()
    if(command_var.get() != ""):
        if(command == command_list[0]):
            SimpleSearch(0)
        elif(command== command_list[1]):
            if(subcommand_var.get() in subcommand_list[1][0:3]):
                LocationSearch(1)
            else:
                LocationSearch(2)
        elif(command == command_list[2]): 
            SimpleSearch(2)
            
    else:
        print("Please select a search criteria")

def SimpleSearch(index):
    tree.delete(*tree.get_children())    
    
    subcommand = subcommand_var.get()
    user_input = "'"+input_var.get().strip() + "'"
    
    table = viewfiledefault()
    ConstructColumn(table)
    i = subcommand_list[index].index(subcommand)
    viewfile = mycursor.execute("SELECT * FROM viewfile WHERE " + term_list[index][i] + " = " + user_input + ";").fetchall()

    length=len(viewfile)
    for k in range(length):
        RoundPrice(k, 14, viewfile)
        tree.insert("",'end',values=viewfile[k])         

#search_state takes integer 1 or 2. 1 indicates that we are querying for one of the items from subcommand_list[1][0:3]
#2 indicates that we are querying for one of the items from subcomman_list[1][3:5]
#LocationSearch first looks for an exact match(disregarding lower/upper case). If none is found, then it looks for an approximate match.
def LocationSearch(search_state):
    subcommand = subcommand_var.get()
    i = subcommand_list[1].index(subcommand)    
    
    length = len(location_search_list[i])
    query = input_var.get().strip()
    found = 0
    
    text1 = "'Store Locations Sheet'.`City Name`, 'Store Locations Sheet'.StateCode, 'Store Locations Sheet'.`Time Zone`"
    text2 = ""
    round_index = 16     
    if(search_state == 2):
        text1 = "'Store Locations Sheet'.`County` , 'Regions Sheet'.`Region`"
        text2 = " JOIN 'Regions Sheet' ON 'Store Locations Sheet'.StateCode = 'Regions Sheet'.StateCode"
        round_index = 15
    
    tree.delete(*tree.get_children()) 
    mycursor.execute("DROP VIEW IF EXISTS viewfile;")
    mycursor.execute("CREATE VIEW IF NOT EXISTS viewfile AS SELECT 'Sales Orders Sheet'.[index], \
        'Sales Orders Sheet'.`OrderNumber`, 'Sales Orders Sheet'.`Sales Channel`, 'Sales Orders Sheet'.WarehouseCode, \
        date(ProcuredDate, 'unixepoch') as 'ProcuredDate', date(OrderDate, 'unixepoch') as 'OrderDate', date(ShipDate, 'unixepoch') \
        as 'ShipDate', date(DeliveryDate, 'unixepoch') as 'DeliveryDate', \
        'Sales Orders Sheet'._SalesTeamID, 'Sales Orders Sheet'._CustomerID, 'Sales Orders Sheet'._StoreID, \
        " + text1 + ", \
        'Sales Orders Sheet'._ProductID, 'Sales Orders Sheet'.`Discount Applied`, 'Sales Orders Sheet'.`Unit Price`, \
        'Sales Orders Sheet'.`Unit Cost` FROM 'Sales Orders Sheet' JOIN 'Store Locations Sheet' ON \
        'Sales Orders Sheet'._StoreID = 'Store Locations Sheet'._StoreID" + text2 + ";") 
    table = mycursor.execute("PRAGMA table_info(viewfile);").fetchall()
    
    ConstructColumn(table)       
    
    for l in range(length):
        if(query.lower() == location_search_list[i][l].lower()):
            query = location_search_list[i][l]
            global head_state 
            head_state = 0   
            found = 1
            break   
    if(found == 0):
        for j in range(length):         
            if(query.lower() in location_search_list[i][j].lower()):
                query = location_search_list[i][j]
                head_state = 0
                found = 0
                break
        if(found == 0):
            
            return
    
    viewfile = mycursor.execute("SELECT * FROM viewfile WHERE " + term_list[1][i] + " = " + query +";").fetchall()
    length=len(viewfile)
    for k in range(length):
        RoundPrice(k, round_index, viewfile)    
        tree.insert("",'end',values=viewfile[k])    


#This should clear all rows in the table. Inserts a single 
def clear():      
    tree.delete(*tree.get_children())
    tree.insert("",'end',values="")    

#Loads the default state of the table "Sales Orders Sheet" from a database using sqlite3. 
#It's column constitutes all columns from "Sales Orders Sheet" with the exception of CurrencyCode, which is trivial(all USD). 
#Dates are converted from unix timestamp into date. 
def viewfiledefault():
    global head_state 
    head_state =0    
    mycursor.execute("DROP VIEW IF EXISTS viewfile; ")
    mycursor.execute("CREATE VIEW IF NOT EXISTS viewfile AS SELECT [index], `OrderNumber`, \
    `Sales Channel`, WarehouseCode, date(ProcuredDate, 'unixepoch') as 'ProcuredDate', date(OrderDate, \
    'unixepoch') as 'OrderDate', date(ShipDate, 'unixepoch') as 'ShipDate', date(DeliveryDate, 'unixepoch') as \
    'DeliveryDate', _SalesTeamID, _CustomerID, _StoreID, _ProductID, `Order Quantity`, \
    `Discount Applied`, `Unit Price`, `Unit Cost` FROM 'Sales Orders Sheet';") 
    table = mycursor.execute("PRAGMA table_info(viewfile);").fetchall()
    return table 

#index takes value 14 or 16. Rounds price of product and sale to 2 digits
def RoundPrice(k, index, viewfile):
    viewfile[k] = list(viewfile[k])        
    viewfile[k][index] = format(viewfile[k][index], ".2f")
    viewfile[k][index + 1] = format(viewfile[k][index + 1], ".2f")            

def ConstructColumn(table):
    length = len(table)
    s = list(range(length))
    tree["columns"] = str(s)
    tree['show'] = 'headings'  
    for j in range(length):
        tree.heading(str(j), text=table[j][1])
        tree.column(j, width=int(font.getlength(table[j][1])*column_width_factor), anchor='c', stretch = 0)          

#column_name should be a string that begins and ends with `
#table_index takes 0 or 1
def getAllUniqueItems(column_name, table_index):
    table = ["'Store Locations Sheet'", "'Regions Sheet'"]
    unique_list = mycursor.execute("SELECT DISTINCT  " + column_name + " FROM " + table[table_index] + ";").fetchall()
    unique_list = [i[0] for i in unique_list]
    length = len(unique_list)
    for i in range(length):
        unique_list[i] = "'" + unique_list[i] + "'"    
    return unique_list

def Insert():
    pass

def Delete():
    pass

def Update():
    pass

def temp():
    iid = tree.get_children()
    length = len(tree.get_children())-10
    if(0 < length):
        for i in range(length):
            tree.delete(iid[i+10])
    
def t():
    pass

    
conn = sqlite3.connect('data.db')
print("Opened database successfully")
mycursor = conn.cursor()

viewfiledefault()

window = tk.Tk()
window.title("Retail Management")

input_var=tk.StringVar()
command_var = tk.StringVar()
subcommand_var = tk.StringVar()

command_list = ["Search by ID", "Search by Location", "Search by Other","Edit"]
subcommand_list = [["Sales Team ID", "Customer ID", "Store ID", "Product ID"], 
                   ["City Name", "State Code", "Time Zone", "County", "Region"], 
                   ["Order Number", "Sales Channel", "Warehouse Code"],
                   ["Insert", "Delete", "Update"]]
term_list = [["`_SalesTeamID`", "`_CustomerID`", "`_StoreID`", "`_ProductID`"], ["`City Name`", "`StateCode`", "`Time Zone`", "`County`", "`Region`"],
             ["`OrderNumber`", "`Sales Channel`", "`WarehouseCode`"]]

table = mycursor.execute("PRAGMA table_info(viewfile);").fetchall()

city_name_list = getAllUniqueItems(term_list[1][0], 0)
state_code_list = getAllUniqueItems(term_list[1][1], 0)
time_zone_list = getAllUniqueItems(term_list[1][2], 0)
county_list = getAllUniqueItems(term_list[1][3], 0)
region_list = getAllUniqueItems(term_list[1][4], 1)
location_search_list = [city_name_list, state_code_list, time_zone_list, county_list, region_list]

column_width_factor = 1.1
font = ImageFont.truetype("arial.ttf", 15)

head_state = 0


frame1 = tk.Frame(master=window, width=300, height=600)
frame1.pack(side = tk.LEFT)

frame2 = tk.Frame(master=window, width=800, height=600)
frame2.pack(fill=tk.BOTH, expand=True)


button_AllSales = tk.Button(master=frame1, text="All Sales", command = AllSales)
button_AllSales.place(x=0, y=0)

button_Head = tk.Button(master=frame1, text="Head", command = head)
button_Head.place(x = 55, y=0)

button_sum = tk.Button(master=frame1, text="Sum", command = Sum)
button_sum.place(x = 95, y=0)

button_clear = tk.Button(master=frame1, text="Clear", command = clear)
button_clear.place(x = 130, y=0)

label = tk.Label(master=frame1)
label.place(x=0, y=200)

search_label = tk.Label(master=frame1, text="Please input search criteria: ")
search_label.place(x = 0, y=80)

input_entry = tk.Entry(frame1,textvariable = input_var, font=('calibre',10,'normal'))
input_entry.place(x=0, y=100)

command_drop= ttk.Combobox(master = frame1, textvariable= command_var, 
                           state="readonly",values=command_list)
command_drop.bind('<<ComboboxSelected>>', subcommand_determine, command_list)
command_drop.place(x=0, y=120)

subcommand_drop= ttk.Combobox(master = frame1, textvariable= subcommand_var, state="readonly", value=subcommand_list[0])
subcommand_drop.place(x=0, y=140)

command_drop.set(command_list[0])        
subcommand_drop.set(subcommand_list[0][0])        

sub_btn=tk.Button(frame1,text = 'Submit', command = submit)
sub_btn.place(x=0, y=160)


tree = ttk.Treeview(frame2, selectmode='browse')
tree.place(x=0, y=0, width=780, height=580)

vsb = tk.Scrollbar(frame2, orient="vertical", command=tree.yview, repeatdelay=0)
vsb.place(x=780, y=0, height =580)

hsb = tk.Scrollbar(frame2, orient="horizontal", command=tree.xview, repeatdelay=0)
hsb.place(x=0, y=580, width = 780)

tree.configure(yscrollcommand=vsb.set)
tree.configure(xscrollcommand=hsb.set)

tree.tag_configure('oddrow', background="white")
tree.tag_configure('evenrow', background="lightblue")


ConstructColumn(table)

tree.insert("",'end',values="")


window.mainloop()




