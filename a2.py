# Written By: Afra Azreen (Student ID: 40234047) - Submitted 12/03/24
# Importing the modules which are required. 
# Note that rather than modifying the sampleScraper module, I have extracted elements of the code which are necessary for my program. 
import requests
from bs4 import BeautifulSoup

# Defining this as a global variable so that all elements have access to it. 
base_url = "https://forums.redflagdeals.com/"

def userMenu():

    """This function is responsible for displaying the menu to the user, essentially showing which indexes correspond to which elements. """

    print("***** Web Scraping Adventure *****")
    print("1. Display Latest Deals")
    print("2. Analyze Deals by Category")
    print("3. Find Top Stores")
    print("4. Log Deal Information")
    print("5. Exit")

def getListings():

    """ 
    This function retrieves the listing of all hot deals from the RedFlagDeals website. 

    Returns:
    - listing (list): A list of BeautifulSoup objects representing all the deal listings.
   
     """

    # The requests.get comes from the requests module. 
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()

    # Parses the listing 
    soup = BeautifulSoup(response.content, "html.parser")
    listings = soup.find_all("li", class_="row topic")
    return listings

def extractInfo(listing, selector):
    """ This method extracts the specified information from the given listing. 

    It takes in two parameters, listing and selector.

    - listing (BeautifulSoup): The BeautifulSoup obejct represents a deal listing.
    - selector (str): CSS selector for the element to extract. 
    
    This method returns the extracted information, or "N/A" if the method was not found. 
    
    """

    # Beautiful Soup object's method in order find the first element in the listing object that matches the given CSS selector selector
    element = listing.select_one(selector)

    # This line returns the text content of the found element after stripping any leading or trailing whitespace if element is not None. If element is None, it returns the string "N/A", indicating that the desired information could not be extracted from the listing.
    return element.text.strip() if element else "N/A"

def option1(listings):

    """
    This function allows us to display the latest deals to the user. 
    For each component of the deals, we go and extract the information from the listing, by calling the extractInfo() method, and then we print it in the end.

    It takes in a parameter: 
    - listing (BeautifulSoup): The BeautifulSoup obejct represents a deal listing.

    """



    # This line calculates the number of deals found in the listings and assigns it to the variable counter.
    counter = len(listings)
    print("\n")
    print("Total deals found: ", counter)
    print("\n")

    # Extracts the info by category.
    deals = []
    for listing in listings:
        store = extractInfo(listing, '.topictitle_retailer')
        item = extractInfo(listing, '.topic_title_link')
        votes = extractInfo(listing, '.total_count_selector')
        username = extractInfo(listing, '.thread_meta_author')
        timeStamp = extractInfo(listing, '.first-post-time')
        category = extractInfo(listing, '.thread_category a')
        replies = extractInfo(listing, '.posts')
        views = extractInfo(listing, '.views')
        url_element = listing.select_one('.topic_title_link')['href']
        url = base_url + url_element if url_element else "N/A"

        # Store each deal as a dictionary for easy sorting
        deal = {
            'store': store,
            'item': item,
            'votes': int(votes) if votes.isdigit() else 0,  # Convert to integer for sorting
            'username': username,
            'timeStamp': timeStamp,
            'category': category,
            'replies': int(replies) if replies.isdigit() else 0,  # Convert to integer for sorting
            'views': int(views) if views.isdigit() else 0,  # Convert to integer for sorting
            'url': url
        }
        deals.append(deal)

    # Prompt user for sorting criterion
    # This code prompts the user to specify the sorting criteria for the deals. It continuously prompts until a valid input ('votes', 'replies', or 'views') is provided.
    sort_by = input("Sort by (votes/replies/views): ").lower()
    while sort_by not in ['votes', 'replies', 'views']:
        print("Invalid input. Please enter 'votes', 'replies', or 'views'.")
        sort_by = input("Sort by (votes/replies/views): ").lower()

    # Sort deals based on user input
    # Based on the user's input, the deals list is sorted in descending order according to the specified sorting criteria (votes, replies, or views).
    deals.sort(key=lambda x: x[sort_by], reverse=True)

    # Print sorted deals
    for deal in deals:
        print("Store: ", deal['store'])
        print("Item: ", deal['item'])
        print("Votes: ", deal['votes'])
        print("Username: ", deal['username'])
        print("Timestamp: ", deal['timeStamp'])
        print("Category: ", deal['category'])
        print("Replies: ", deal['replies'])
        print("Views: ", deal['views'])
        print("URL: ", deal['url'])
        print("---------------------------------")
        print("\n")


def option2(listings):

    """
    This is a function created to analyze the deals by category.

    It takes in a parameter: 
    - listing (BeautifulSoup): The BeautifulSoup obejct represents a deal listing.

    Then it prints the deals by category. 
    
    """
    
    catcount = {}

    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category != "N/A":
            catcount[category] = catcount.get(category, 0) + 1


    # Here, I will determine the longest category name for formatting purposes.
    longest_category = max(len(category) for category in catcount)


    # This determines the length of the longest number for formatting
    longest_count = max(len(str(counter)) for counter in catcount.values())

    print("\n")
    print("Deals by Category:")
    print("\n")

    # Here, I will be printing the deals available by category, as in the number of deals available.
    # The formatting is aligned by using the rjust method on the category names and also on the counters

    for category, counter in sorted(catcount.items()):
        count_str = f"{counter} deals".rjust(longest_count + 6)
        print(f"{category.rjust(longest_category)}: {count_str}")

    print("*" * (longest_category + longest_count + 9)) 
    print("\n")


def option3():

    """ This function does not take any parameters, instead it displays the top stores, extracting the information using the extractInfo() method.
        This displays the top stores, essentially allowing you to focus on the store with the most deals.
        Displays them in a formatted manner. 
    """
    
    storeNum = int(input("Enter the number of top stores to display: "))
    listings = getListings()

    storeCount = {}
    for listing in listings:
        store = extractInfo(listing, '.topictitle_retailer')
        if store != "N/A":
            storeCount[store] = storeCount.get(store, 0) + 1

    storesSort = sorted(storeCount.items(), key=lambda x: x[1], reverse=True)

    # Like previous option, here we determine the longest store name for formatting
    longest_store = max(len(store) for store, _ in storesSort[:storeNum])


     # This determines the length of the longest num for formatting. 
    longest_count = max(len(str(count)) for _, count in storesSort[:storeNum])

    print("\nTop Stores")
    for store, counter in storesSort[:storeNum]:
        count_str = f"{counter} deals".rjust(longest_count + 6)
        print(f"{store.rjust(longest_store)} : {count_str}")

    print("*" * (longest_store + longest_count + 9))
    print("\n")


def option4():

    """
    This function does not take in any parameters and is responsible for logging all the deals with a specified category. 
    It asks the user for the category number, and then logs all those deals to a file called log.txt

    """
    
    listings = getListings()

    cats = set()
    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category != "N/A":
            cats.add(category)

    print("\n")
    print("List of Categories:")
    print("\n")

    for i, category in enumerate(cats, start=1):
        print(f"{i}. {category}")

    catchoice = int(input("Enter the number corresponding to the category: "))
    chosencat = list(cats)[catchoice -1]


    # The function iterates through the deal listings again and filters out deals belonging to the chosen category. It collects the URLs of these deals in the catdeals list.
    catdeals = []
    for listing in listings:
        category = extractInfo(listing, '.thread_category a')
        if category == chosencat:
            url_element = listing.select_one('.topic_title_link')['href']
            url = base_url + url_element if url_element else "N/A"
            catdeals.append(url)

    with open('log.txt', "w") as f:
        for deal_link in catdeals:
            f.write(deal_link+'\n')
    
    print("All the links have been logged successfully.")
    print("\n")


def switch(choice):

    """ This method takes in the choice parameter and imitates a switch statement to handle all processing for the console application."""

    if choice == 1:
        listings = getListings()
        option1(listings)
    
    elif choice == 2:
        listings = getListings()
        option2(listings)
    
    elif choice == 3:
        option3()
    
    elif choice == 4:
        option4()
    
    elif choice == 5:
        print("Exiting the program. Goodbye!")
        exit()
    
    else:
        print("Error, something went wrong.")


def main():

    """ This is the main method, where the entire program begins. """

    choice = None

    while True:
        userMenu()
        choice = int(input("Enter your choice (1-5): "))
        switch(choice)

        if choice == 5:
            break


if __name__ == "__main__":
    main()