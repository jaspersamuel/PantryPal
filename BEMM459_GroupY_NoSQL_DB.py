#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install pymongo package
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# In[12]:


import pymongo

# Note: I am using port number 7070. You may have to change this port number if the connection is being refused. 
# To change the port number, open "mongod_use this.bat" (in S:/ drive) and change 7070 to a different number, and then execute the server.
# You can also update the .bat file for the the shell (client) for MongoDB with the same number (this file is called "mongo_use this.bat" and is also under S:/)
mongoclient = pymongo.MongoClient("mongodb://localhost:7200/")

#Check what databases exist - the output is a list of database names
print(mongoclient.list_database_names())


# In[13]:


#Create a new database       
mydb = mongoclient["BEMM459_GroupY"]
print(type(mydb))


# In[27]:


from pymongo import MongoClient
client = MongoClient("mongodb://localhost:7200/")
db = client['BEMM459_GroupY'] 


# # Creating a New collection name Cus_Allergy

# In[17]:


# Accessing the collection
cus_allergy_collection = db["Cus_Allergy"]

# Defining the data which has to be inserted
data = [
    {"Customer_ID": 82702301, "Allergy_Code": "PE"},
    {"Customer_ID": 82702301, "Allergy_Code": "SE"},
    {"Customer_ID": 80788323, "Allergy_Code": "SE"},
    {"Customer_ID": 80788323, "Allergy_Code": "GL"},
    {"Customer_ID": 38200218, "Allergy_Code": "PE"},
    {"Customer_ID": 38200218, "Allergy_Code": "SO"},
    {"Customer_ID": 55239362, "Allergy_Code": "GL"},
    {"Customer_ID": 55239362, "Allergy_Code": "FI"},
    {"Customer_ID": 55239362, "Allergy_Code": "PE"},
    {"Customer_ID": 87484719, "Allergy_Code": "PE"},
    {"Customer_ID": 23607544, "Allergy_Code": "FI"},
    {"Customer_ID": 88041756, "Allergy_Code": None}, 
    {"Customer_ID": 54398406, "Allergy_Code": "DR"},
    {"Customer_ID": 45684501, "Allergy_Code": None},  
    
]

# Insert the data into the collection
cus_allergy_collection.insert_many(data)


# # Adding one more data to the collection

# In[18]:


# Define the remaining data
remaining_data = [
    {"Customer_ID": 82702301, "Allergy_Code": "PE"}
]

# Insert the remaining data into the collection
cus_allergy_collection.insert_many(remaining_data)


# # Filter Query to Show Only Recipe Name and Recipe Allergy

# In[19]:


# Accessing the collection
recipes_collection = db["recipes"]

# Defining the filter to find recipes with Recipe_Allergy as "DR"
filter_query = {"Recipe_Allergy": "DR"}

# Performing the find operation and excluding Recipe_Instruction field
dairy_recipes = recipes_collection.find(filter_query, {"Recipe_Instruction": 0})

# Iterate over the results and print only Recipe Name and Recipe Allergy
for recipe in dairy_recipes:
    print(f"Recipe Name: {recipe.get('Recipe_Name', 'N/A')}, Recipe Allergy: {recipe.get('Recipe_Allergy', 'N/A')}")


# # Updating the Recipe collection with recipe names

# In[21]:


# Accessing the collection Additions to Get Only Recipe ID and Recipe Name

# Accessing the collection
recipes_collection = db["recipes"]

# Defining the data with Recipe_ID and Recipe_Name
recipe_data = [
    {"Recipe_ID": "vvs8110", "Recipe_Name": "BBQ Chicken Skewers"},
    {"Recipe_ID": "ibl2099", "Recipe_Name": "Spicy Chicken Stir-Fry"},
    {"Recipe_ID": "hxj8750", "Recipe_Name": "Cajun Blackened Fish Tacos"},
    {"Recipe_ID": "sqh1810", "Recipe_Name": "Lemon Herb Roasted Chicken"},
    {"Recipe_ID": "vqv2473", "Recipe_Name": "Coconut Curry Vegetables"},
    {"Recipe_ID": "zmw8916", "Recipe_Name": "Prawn & Mango Wrap"},
    {"Recipe_ID": "eyl9906", "Recipe_Name": "Teriyaki Salmon Bowl"},
    {"Recipe_ID": "zwb9798", "Recipe_Name": "BBQ Pulled Pork Sandwiches"},
    {"Recipe_ID": "qca3677", "Recipe_Name": "Apple Cinnamon Pork Chops"},
    {"Recipe_ID": "vcp4371", "Recipe_Name": "Garlic Parmesan Pasta"},
    {"Recipe_ID": "qgj0336", "Recipe_Name": "Greek Quinoa Salad"},
    {"Recipe_ID": "fjy5376", "Recipe_Name": "Vegetarian Chili"},
    {"Recipe_ID": "afa3444", "Recipe_Name": "Pesto Zucchini Noodles"}
]

# Updating each document in the collection with Recipe_Name
for recipe in recipe_data:
    recipes_collection.update_one({"Recipe_ID": recipe["Recipe_ID"]}, {"$set": {"Recipe_Name": recipe["Recipe_Name"]}})

# Find and print only Recipe_ID and Recipe_Name
cursor = recipes_collection.find({}, {"Recipe_ID": 1, "Recipe_Name": 1, "_id": 0})
for document in cursor:
    print(document)


# # Inserting Images in Recipe collection

# In[89]:


import pymongo
import gridfs

# Access the collections
recipes_collection = db["recipes"]
fs = gridfs.GridFS(db)

# URL for the OneDrive image directory
image_directory = "https://universityofexeteruk-my.sharepoint.com/:f:/g/personal/rs1118_exeter_ac_uk/EkXXxuw4jLdIsnLLCW9nYOYBN4JO9jUoWiRd1h8tj_IZxQ?e=IWbyRU"

# Iterate over each recipe
for recipe in recipes_collection.find():
    # Constructing the image URL using the Recipe_ID
    image_url = f"{image_directory}/{recipe['Recipe_ID']}.jpg"

    try:
        # Store the image URL in the recipe document
        recipes_collection.update_one(
            {"_id": recipe["_id"]},
            {"$set": {"Image_URL": image_url}}
        )
        print(f"Image URL successfully added for Recipe_ID: {recipe['Recipe_ID']}")
    except Exception as e:
        print(f"Error adding image URL for Recipe_ID {recipe['Recipe_ID']}: {e}")


# In[90]:


# image views
import pymongo
import gridfs
from IPython.display import Image, display

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:7200/")
db = client["BEMM459_GroupY"]

# Access the collections
recipes_collection = db["recipes"]
fs = gridfs.GridFS(db)

# Fetch the first three recipes
recipes = recipes_collection.find().limit(3)

# Iterate over the recipes
for recipe in recipes:
    # Retrieve the image ID from the recipe document
    image_id = recipe.get("Image_ID")
    
    if image_id:
        # Retrieve the image data from GridFS
        image_data = fs.get(image_id).read()

        # Display the image using IPython.display
        display(Image(data=image_data))
    else:
        print(f"No image found for Recipe_ID: {recipe['Recipe_ID']}")


# # Execute the query and sort the results based on Cooking_Time in descending order

# In[24]:


result = recipes_collection.find({}, {"Recipe_Name": 1, "Cooking_Time": 1, "_id": 0}).sort("Cooking_Time", -1)

# Display the results
for recipe in result:
   print(recipe)


# # creating customer review collection

# In[25]:


import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:7200/")
db = client["BEMM459_GroupY"]

# Create a collection named 'customer_reviews'
customer_reviews_collection = db["customer_reviews"]

# Sample data for customer reviews
sample_reviews = [
    {
        "Review_ID": 1,
        "Recipe_ID": "vvs8110",
        "Customer_ID": 82702301,
        "Review_Text": "This recipe was fantastic!",
        "Rating": 5,
        "Feedback_Img": "https://www.bing.com/images/search?view=detailV2&ccid=q4NVmrmD&id=107FC91CFE51093EDD6587D60E86CAC22EC281FA&thid=OIP.q4NVmrmDCyky7uezch58EAHaHa&mediaurl=https%3a%2f%2fblackwells-butchers.com%2fwp-content%2fuploads%2f2020%2f08%2fhomemade-chicken-curry.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.ab83559ab9830b2932eee7b3721e7c10%3frik%3d%252boHCLsLKhg7Whw%26pid%3dImgRaw%26r%3d0&exph=1000&expw=1000&q=chicken+dish+homade&simid=608041437066821657&FORM=IRPRST&ck=7727D713CF4919638AA794549B4D5B06&selectedIndex=0&itb=0"  # Sample URL
    },
    {
        "Review_ID": 2,
        "Recipe_ID": "ibl2099",
        "Customer_ID": 82702301,
        "Review_Text": "Loved the flavors!",
        "Rating": 4,
        "Feedback_Img": "https://www.bing.com/images/search?view=detailV2&ccid=97eJgDKt&id=617F18480A8E202BA3F7FFFEA538C997C84A85B7&thid=OIP.97eJgDKtNQjum3wq6IUw9gHaLH&mediaurl=https%3a%2f%2fpeasandcrayons.com%2fwp-content%2fuploads%2f2020%2f11%2fsimple-side-salad-recipe-2-1024x1536.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.f7b7898032ad3508ee9b7c2ae88530f6%3frik%3dt4VKyJfJOKX%252b%252fw%26pid%3dImgRaw%26r%3d0&exph=1536&expw=1024&q=salad+dish+homade&simid=608002898313216326&FORM=IRPRST&ck=A5F6E4927098CEC0FCC672320A1A2286&selectedIndex=0&itb=0"  # Sample URL
    },
    {
        "Review_ID": 3,
        "Recipe_ID": "hxj8750",
        "Customer_ID": 80788323,
        "Review_Text": "Not my favorite dish.",
        "Rating": 3,
        "Feedback_Img": None  # No image provided
    }
]

# Insert sample reviews into the collection
customer_reviews_collection.insert_many(sample_reviews)


# # Python Script to recommend recipes based upon the customer allergies

# In[87]:


import pymongo

# Replace with your connection string
client = MongoClient("mongodb://localhost:7200/")
db = client['BEMM459_GroupY']

customer_allergies = db["Cus_Allergy"]
recipes = db["recipes"]

CID = 87484719

x = customer_allergies.find({"Customer_ID": 10320164})
Allergy = x[0]["Allergy_Code"]


# Performing the find operation and excluding Recipe_Instruction field
filter_result = recipes_collection.find({"Recipe_Allergy": {"$ne": Allergy}}, {"Recipe_Instruction": 0})

for x in filter_result:
    x.pop("_id")
    x.pop("Recipe_ID")
    
    print(x,"\n")



# # Dropping the temp_matched_recipes

# In[160]:


# Dropping the temp_matched_recipes collection from the BEMM459_GroupY database

# Accessing the collection to drop
temp_matched_recipes_collection = db["temp_matched_recipes"]

# Dropping the temp_matched_recipes collection
temp_matched_recipes_collection.drop()


# In[ ]:




