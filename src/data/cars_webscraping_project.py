# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# HTTP requests
url = "https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=30&mileage_max=&page_size=20&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"
}
page = requests.get(url, headers=headers)

# checking status code
page.status_code

# soup object
soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
soup2

# results
results = soup2.find_all("div", {"class": "vehicle-card"})
len(results)

results[0]

# extracting the name, mileage, rating, rating count, dealer name and price of the vehicle
results[0].find("h2").get_text().strip()
results[0].find("div", {"class": "mileage"}).get_text().strip()
results[0].find("span", {"class": "sds-rating__count"}).get_text().strip()
results[0].find("span", {"class": "sds-rating__link"}).get_text().strip()
results[0].find("div", {"class": "dealer-name"}).get_text().strip()
results[0].find("span", {"class": "primary-price"}).get_text().strip()

# creating empty lists and using for loop to iterate
name = []
mileage = []
rating = []
rating_count = []
dealer_name = []
price = []

# name
for result in results:
    try:
        name.append(result.find("h2").get_text().strip())
    except:
        name.append("n/a")

# mileage
for result in results:
    try:
        mileage.append(result.find("div", {"class": "mileage"}).get_text().strip())
    except:
        mileage.append("n/a")

# rating
for result in results:
    try:
        rating.append(
            result.find("span", {"class": "sds-rating__count"}).get_text().strip()
        )
    except:
        rating.append("n/a")

# rating_count
for result in results:
    try:
        rating_count.append(
            result.find("span", {"class": "sds-rating__link"}).get_text().strip()
        )
    except:
        rating_count.append("n/a")

# dealer name
for result in results:
    try:
        dealer_name.append(
            result.find("div", {"class": "dealer-name"}).get_text().strip()
        )
    except:
        dealer_name.append("n/a")

# price
for result in results:
    try:
        price.append(result.find("span", {"class": "primary-price"}).get_text().strip())
    except:
        price.append("n/a")


# create pandas dataframe
car_dealer = pd.DataFrame(
    {
        "Name": name,
        "Mileage": mileage,
        "Rating": rating,
        "Rating Count": rating_count,
        "Dealer Name": dealer_name,
        "Price": price,
    }
)
car_dealer

# data cleaning
car_dealer["Rating Count"] = car_dealer["Rating Count"].apply(
    lambda x: x.strip("reviews)").strip("(")
)

# checking and correcting data types
car_dealer.dtypes
car_dealer["Rating Count"] = [
    int(str(i).replace(",", "")) for i in car_dealer["Rating Count"]
]
car_dealer["Rating"] = car_dealer["Rating"].str.replace("n/a", "0").astype(float)

car_dealer

# output to excel
car_dealer.to_excel("single_page_car.xlsx", index=False)


# creating empty lists for iteration using for loop
name = []
mileage = []
rating = []
rating_count = []
dealer_name = []
price = []

for i in range(1, 11):

    # url in a variable
    url = (
        "https://www.cars.com/shopping/results/?page="
        + str(i)
        + "&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=30&mileage_max=&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip="
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26"
    }
    page = requests.get(url, headers=headers)

    # soup object
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # results
    results = soup2.find_all("div", {"class": "vehicle-card"})

    # name
    for result in results:
        try:
            name.append(result.find("h2").get_text().strip())
        except:
            name.append("n/a")

    # mileage
    for result in results:
        try:
            mileage.append(result.find("div", {"class": "mileage"}).get_text().strip())
        except:
            mileage.append("n/a")

    # rating
    for result in results:
        try:
            rating.append(
                result.find("span", {"class": "sds-rating__count"}).get_text().strip()
            )
        except:
            rating.append("n/a")

    # rating_count
    for result in results:
        try:
            rating_count.append(
                result.find("span", {"class": "sds-rating__link"}).get_text().strip()
            )
        except:
            rating_count.append("n/a")

    # dealer name
    for result in results:
        try:
            dealer_name.append(
                result.find("div", {"class": "dealer-name"}).get_text().strip()
            )
        except:
            dealer_name.append("n/a")

    # price
    for result in results:
        try:
            price.append(
                result.find("span", {"class": "primary-price"}).get_text().strip()
            )
        except:
            price.append("n/a")

# create pandas dataframe
car_dealer_combined = pd.DataFrame(
    {
        "Name": name,
        "Mileage": mileage,
        "Rating": rating,
        "Rating Count": rating_count,
        "Dealer Name": dealer_name,
        "Price": price,
    }
)

car_dealer_combined

car_dealer_combined.duplicated()

# data cleaning
car_dealer_combined["Rating Count"] = car_dealer_combined["Rating Count"].apply(
    lambda x: x.strip("reviews)").strip("(")
)

# checking and correcting data types
car_dealer_combined.dtypes
car_dealer_combined["Rating Count"] = [
    int(str(i).replace(",", "")) for i in car_dealer_combined["Rating Count"]
]
car_dealer_combined["Rating"] = (
    car_dealer_combined["Rating"].str.replace("n/a", "0").astype(float)
)

car_dealer_combined

# export to excel
car_dealer_combined.to_excel("multiple_page_car.xlsx", index=False)
