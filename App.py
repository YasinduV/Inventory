import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
from PIL import Image

#Page configurations
st.set_page_config(page_title= "PR Network Spare", layout= "wide")

hide_stlit_style = "<style> #MaiMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} </style>"
st.markdown(hide_stlit_style, unsafe_allow_html=True)

#Pre-loads
back_pic = Image.open("images/back pic.jpeg")
if "password" not in st.session_state:
    st.session_state["password"] = None

def list_bilder(feild_name):
    list_name = []
    for item in inventory[str(feild_name)]:
        if item not in list_name:
            list_name.append(item)
    
    return(list_name)

def item_builder(brand_name):
    item_type = []
    item_df = inventory.loc[inventory["Brand"]== brand_name]
    item_type = item_df["Spare_type"].values.tolist()
    return(item_type)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')



#Code starts here

with st.container():
    col1,col2,col3,col4 = st.columns([0.3,1.5,0.5,0.1])
    with col1:
        st.empty()
    with col2:
        st.title("Spare Inventory(SLT PR Network Section)")
    with col3:
        st.image(back_pic, width = 200)
    with col4:
        st.empty()

#Load csv to create pandas dataframe

with st.container():
    inventory = pd.read_csv("Data/Spare Inventory.csv")

with st.container():
    Brands = list_bilder("Brand")

    brand_selection = option_menu(menu_title= None, options=Brands, orientation= "horizontal")

    if brand_selection == Brands[0]:
        new_df = inventory.loc[inventory["Brand"]==Brands[0]]
    
    elif brand_selection == Brands[1]:
        new_df = inventory.loc[inventory["Brand"]==Brands[1]]

    elif brand_selection == Brands[2]:
        new_df = inventory.loc[inventory["Brand"]==Brands[2]]
    
    st.dataframe(new_df, height= 290, use_container_width= True)

    #st.write("---")

with st.container():
    with st.sidebar:
        inventory_type = option_menu(menu_title=None, options=["Search Spare","Spare-In","Spare-Out","New Stock","Advanced Options"])

    if inventory_type == "Search Spare":
        vendor = st.sidebar.radio("Brand",Brands, horizontal= True)
        spare_types = item_builder(vendor)
        with st.sidebar.form("add", clear_on_submit=True):
            s_type = st.text_input("Spare Type", placeholder= "Use CAPITAL BLOCK LETTERS")

            search_submit_b = st.form_submit_button("Search")

            if search_submit_b:
                try:
                    s_type = s_type.upper()
                    s_result_df = inventory.loc[inventory["Spare_type"]== s_type]
                    s_quantity = s_result_df.iloc[0]["Quantity"]
                    st.sidebar.header(":package:"+" "+str(s_quantity)+" units are available.")
                except:
                    st.sidebar.error("Please enter a valid Spare Type!")


   
    if inventory_type == "Spare-In":
        vendor = st.sidebar.radio("Brand",Brands, horizontal= True)
        spare_types = item_builder(vendor)
        with st.sidebar.form("add", clear_on_submit=True):
            s_type = st.selectbox("Spare Type", options= spare_types)
            quantity = st.number_input("Quantity",min_value=0, step=1)

            add_submit_b = st.form_submit_button("SAVE")

            if add_submit_b:
                result_df = inventory.loc[inventory["Spare_type"] == s_type]
                ind = result_df.index.values.tolist()
                inventory.loc[ind[0], "Quantity"] = inventory.loc[ind[0],"Quantity"] + quantity
                inventory.to_csv("Data/Spare Inventory.csv", index = False)

    if inventory_type == "Spare-Out":
        vendor = st.sidebar.radio("Brand",Brands, horizontal= True)
        spare_types = item_builder(vendor)
        with st.sidebar.form("sub", clear_on_submit=True):
            s_type = st.selectbox("Spare Type", options= spare_types)
            quantity = st.number_input("Quantity",min_value=0, step=1)

            sub_submit_b = st.form_submit_button("SAVE")

            if sub_submit_b:
                result_df = inventory.loc[inventory["Spare_type"] == s_type]
                ind = result_df.index.values.tolist()
                if inventory.loc[ind[0],"Quantity"] > 0:
                    inventory.loc[ind[0], "Quantity"] = inventory.loc[ind[0],"Quantity"] - quantity
                    inventory.to_csv("Data/Spare Inventory.csv", index = False)
                else:
                    st.sidebar.warning("No spare in stock!")

    if inventory_type == "New Stock":
        vendor = st.sidebar.radio("Brand", Brands, horizontal= True)
        with st.sidebar.form("new_stock", clear_on_submit= True):
            s_type = st.text_input("Spare Type",placeholder= "Use CAPITAL BLOCK LETTERS")
            quantity = st.number_input("Quantity",min_value=0, step=1)
            descripton = st.text_input("Description", placeholder= "Add Description/Comment")

            new_submit_b = st.form_submit_button("SAVE")

            if new_submit_b:
                if s_type == "":
                    st.sidebar.error("Please enter a valid Spare Type!")
                elif quantity == 0:
                    st.sidebar.error("Please enter a valid quantity!")
                else:
                    new_entry = {"Brand":vendor, "Spare_type":s_type.upper(), "Quantity":quantity, "Description":descripton}
                    new_entry_df = pd.DataFrame([new_entry])
                    inventory = pd.concat([inventory, new_entry_df], ignore_index= True)
                    inventory.to_csv("Data/Spare Inventory.csv", index = False)

    if inventory_type == "Advanced Options":
        with st.sidebar:
            mod = option_menu(menu_title=None, options= ["Delete Record", "Add Comment"])
            if mod == "Delete Record":
                st.sidebar.error("You are about to DELETE a record!")
                with st.sidebar.form("del_record", clear_on_submit= True):
                    record_ind = st.text_input("Record Index", placeholder= "Enter the Index Number ")
                    del_submit_b = st.form_submit_button("DELETE & SAVE")

                if del_submit_b:
                    try:
                        if 0 <= int(record_ind) <= len(inventory):
                            inventory.drop(inventory.index[int(record_ind)], inplace= True)
                            inventory.to_csv("Data/Spare Inventory.csv", index = False)
                            st.sidebar.success("Done!")
                    except:
                        st.sidebar.error("Please enter a valid Index!")


            if mod == "Add Comment":
                with st.sidebar.form("add_comment", clear_on_submit= True):
                    dis_ind = st.text_input("Record Index", placeholder= "Enter the Index Number ")
                    comment = st.text_input("Comment", placeholder= "Add or Update comment/description")
                    com_submit_b = st.form_submit_button("UPDATE & SAVE")

                if com_submit_b:
                    try:
                        if 0 <= int(dis_ind) <= len(inventory):
                            inventory.loc[int(dis_ind), "Description"] = comment
                            inventory.to_csv("Data/Spare Inventory.csv", index = False)
                            st.sidebar.success("Done!")
                    
                    except:
                        st.sidebar.error("Please enter a valid Index!")

with st.container():
    col1,col2 = st.columns([5,1])
    with col1:
        st.empty()
    with col2:
        backup_file = convert_df(inventory)
        down_b = st.download_button("DOWNLOAD & BACKUP", backup_file, "Inventory_Backup.csv", "text/csv", key= "spare-backup")
        
        if down_b:
            st.success("Done!")



                    