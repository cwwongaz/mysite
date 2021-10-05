This is Ronald from Hong Kong.

This is a webpage developed using Django. 

How to open:    
    1. Go to this file's directory, type "python3 manage.py runserver". It will generate an URL in the command prompt.
    2. Copy and Paste the URL to the browser. (The URL usually be http://127.0.0.1:8000)
    3. Add "/GamerAsia/page/1" to the end of the URL (i.e. If the URL is "http://127.0.0.1:8000", then rephrase the URL into http://127.0.0.1:8000/GamerAsia/page/1)
    

In this final project of CS50w, I wrote a online store webpage for selling. This project used Django as the back-end and JavaScript as the font-end, including:

HTML Templates:
    layout.html: including a navigation bar fixed on top of the screen, to allow users to go back to index page, register, login, logout, check / edit the user profile and check out from shopping cart.

    index.html: incluing the item on sale.

    cart.html: including the items put in the cart.

    item_page.html: when user clicked on the item sheet displayed on the index page, the user will be nagivated to here, which included the detail of the item.
    
        An item includes its id, name, image, price, description, footnote, number in store, and average rating

    new_item.html: create new item only available for admin user.

    login.html: this page allow user to log-in.

    register.html: user can register for an account in this page.

    profile.html: this page includes user's information.



media / images: 
    This file includes the image of item uploaded to the server.

back-end functions and APIs:

    JavaScript: 
        rating: 
            The JavaScript functions are written inline since the operation of the HTML webpage mainly based on the Django back-end, One feature of the JavaScript function is that it achieved the rate function, which allow the logged-in user to rate the item (but didn't set rate amendment funciton here) 

            There are 5 stars representing the rating (1 star is lowest rating and 5 is highest.) The star shows the average rating by all the users by showing how many stars are "lighted up". 
            
            When the cursor is on a star, i.e. the third star, then the light of the star will change and the 1st star to the 3rd star will light up. However, when the cursor is moved away from the star, the light of the stars will change back according to the original rating. User didn't log-in cannot see this JavaScript and cannot rate the item. Also, the back-end API will check whether the user has logged-in.

            When user put the cursor on a star and click, it will fetch an API to record the rating of the item. If the user has rated before, then the new rating will not be recorded. However, if the user haven't rate before, a new rating will be recorded and save into the database.

        User Profile edit:
            The JavaScript allows user to edit their profile page. The display form (cannot be edit now, only showing the user's data) is prefilled by the previous data entered by the user. By clicking the edit button, the form will change to editable, and the edit button will be change to the save button to fetch the API to save the amended data.

    Shopping carts:
        In the shopping cart, I implemented session which allows non logged-in user / user does not have an account to use this function, user can click "add to cart" button via the item_page.html to put the item into the shopping cart.
        
        In the layout.html (navigation bar), user can click the shopping cart icon, it will pop out a div allowing user to go to *check out page* (cart.html), or clear everything in the cart.

        The Session is set to reset after 1 hour.

    cart.html:
        When user clicked *check out* button, they will be navigated to this page. This page has similar style as in the index page, but with slightly differents of the "increase" and "decrease" button of the quantity of items in cart. Also, it has the remove button for a whole item that allow users to remove the item without pressing "decrease" many times.


    Pagination:
        The index page (index.html) and check out page (cart.html) used pagination to make the display concise, it has a navigation bar at the bottom, showing "previous" and "next", and the page number of the previous 2 pages and the next 2 pages.
        i.e. if we are at page 3, the navigation bar will show 
            "" Previous 1 2 3 4 5 Next ""
        
        If it is the first / last pages, the "Previous" / "Next" button will be disabled

        The navigation bar is achived by the Django filter.

    Security:
        The APIs will verify the users and stop unauthorized user to change the information.

