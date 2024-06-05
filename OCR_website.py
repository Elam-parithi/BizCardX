import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
from OCR_processing import process_image, get_data
from SQL_Datahandler import *
from annotated_text import annotated_text


def create_df(data):
    df = pd.DataFrame(data)
    return df

st.set_page_config(
    page_title="BizCardX",
    page_icon=r"Icons/Calendula.ico",
    layout='wide',
)
st.title("BizCardX: Extracting Business Card Data with OCR")
annotated_text('by ', ('[Elamparithi T](https://www.linkedin.com/in/elamparithi-t/)', 'Data Scientist', "#8ef"))

selected = option_menu('Menu', ["Home", "Modify", "About"],
                       icons=["house", "pencil-square", "info"],
                       default_index=0)

mydb = connect_db()
mycursor = mydb.cursor(buffered=True)
create_table(mycursor)

if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.write("Technologies Used: Python, easy OCR, Streamlit, SQL, Pandas")
        st.write("""The result of the project would be a Streamlit application that allows users to upload
                    an image of a business card and extract relevant information from it using easyOCR.
                    The extracted information would include the company name, card holder name,
                    designation, mobile number, email address, website URL, area, city, state, and pin
                    code. The extracted information would then be displayed in the application's
                    graphical user interface (GUI).
                    """)
    with col2:
        st.image("home.png")

if selected == "Modify":
    st.write("Upload a Business Card")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:
        save_path = os.path.join("uploaded_cards", uploaded_card.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_card.getbuffer())

        image, res = process_image(save_path)

        col1, col2 = st.columns(2)
        with col1:
            st.write("Card_uploaded")
            st.image(uploaded_card)

        with col2:
            with st.spinner("processing..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.write("Completed Data Extracted")
                st.pyplot(image)

        result = [text for _, text, _ in res]
        data = get_data(result, save_path)
        df = create_df(data)
        st.success("Data Extracted !!!___")
        st.write(df)

        if st.button("Upload to MySQL DB"):
            insert_data(mycursor, mydb, df)
            st.success("MySQL DB updated !!!___")

if selected == "Modify":
    col1, col2, col3 = st.columns([3, 3, 2])
    col2.write("Modify")
    column1, column2 = st.columns(2)
    try:
        with column1:
            business_cards = {row[0]: row[0] for row in fetch_data(mycursor, "SELECT card_holder FROM card_data")}
            selected_card = st.selectbox("Select name to update", list(business_cards.keys()))
            st.write("Update or modify any data below")
            result = fetch_data(mycursor,
                                f"SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data WHERE card_holder='{selected_card}'")[
                0]

            data = [
                st.text_input("Company_Name", result[0]),
                st.text_input("Card_Holder", result[1]),
                st.text_input("Designation", result[2]),
                st.text_input("Mobile_Number", result[3]),
                st.text_input("Email", result[4]),
                st.text_input("Website", result[5]),
                st.text_input("Area", result[6]),
                st.text_input("City", result[7]),
                st.text_input("State", result[8]),
                st.text_input("Pin_Code", result[9])
            ]

            if st.button("Commit changes to DB"):
                update_data(mycursor, mydb, data, selected_card)
                st.success("Information updated in database successfully.")

        with column2:
            business_cards = {row[0]: row[0] for row in fetch_data(mycursor, "SELECT card_holder FROM card_data")}
            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
            st.write(f"You have selected {selected_card}'s card to delete")
            st.write("Proceed to delete this card?")

            if st.button("Yes, Delete Card"):
                delete_data(mycursor, mydb, selected_card)
                st.success("card deleted from database.")
    except:
        st.warning("!!!! No Data in DB !!!!")
        st.write()

    if st.button("View updated data"):
        updated_df = pd.DataFrame(fetch_data(mycursor,
                                             "SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data"),
                                  columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
                                           "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)
if selected == "About":
    pass

