# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Custom Smoothie!
    """
)

name_on_order = st.text_input("Name on smoothie")
st.write("Choose the fruits you want in your custom smoothie!")

#option = st.selectbox(
 #   "What is your favourite fruit?",
  #  ("Banana", "Strawberries", "Peaches"))

#st.write("You selected:", option)
cnx=st.connection("snowflake")
session=cnx.session()

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)
st.write(ingredients_list)
st.text(ingredients_list)

if ingredients_list:
    

    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string+=fruits_chosen+' '

    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients.select(col(name_on_order))
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


    st.write(my_insert_stmt)
    
    #st.stop

    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



