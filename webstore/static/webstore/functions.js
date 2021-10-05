
console.log("JS have been read");

document.addEventListener('DOMContentLoaded', () => {
    console.log("JS have been read");
});

// Didn't used
function implement_cart_itemNumber(session_cart_list_inString, item_id) {
    number_of_item = 0
    console.log("loaded")
    for (i=0; i<session_cart_list_inString.length; i++) {
        if (session_cart_list_inString[i] == item_id) {
            number_of_item++
        } 
    }
    console.log(number_of_item)
    return number_of_item
}
