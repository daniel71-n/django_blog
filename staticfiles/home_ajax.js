/*
    Javascript (with AJAX) for sorting and pagination on the homepage.
    Used in the home.html template
*/

document.getElementById("cat_div_heading").addEventListener("click", function() {
 // alert('works');
    try{
        var elem = document.getElementById("categoryList");
        var arrow = document.getElementById("arrow-sign");
        //alert(elem);
        
        if (elem.classList.contains("hidden")){
            elem.classList.remove("hidden");
            arrow.classList.remove("right");
            arrow.classList.add("down");
        }
        else{
            elem.classList.add("hidden");
            arrow.classList.remove("down");
            arrow.classList.add("right");
        }
    }
    catch(err){
        alert(err);
    }
}
)



function getURL(){
//retrieve the current URL path; --> the whole URL first, potential querystrings included, then get the path by discarding everything after the '?' 
try{
var url = window.location
var urlPathOnly = url.toString().split('?')[0];
  }
catch(err){
//alert(err);
  }
return urlPathOnly 
}

function getSortOption(){
//get the otpion that's been selected in the selectlist element
var option = document.getElementById("sort_options").value;
return option
}


function getPageQueryString(val){
//the href attribute of the 'a' element wrapped around each of the page buttons (actually, the html for the whole section) is updated on each AJAX operation, so it's always aware if it's paginating a queryset that has been re-sorted or not
var pageQuery = val.toString();  
ajaxSort(pageQuery);
return false  
 // the function needs to return False in order to prevent the link being clicked on from firing, since this function is the callback called on the 'onClick' event by the handler.
 // if this weren't so, the link would still send out its associated query string when clicked, precluding the AJAX call
}


function ajaxSort(arg=null) {
//it takes a single argument with a default value of null; 
//its purpose is to determine how the function should proceed depending on whether it's being called by a page button having been clicked, or by a sorting option having been selected
//if the arg is null, it's the latter; if it's something else (the 'querystring' that precedes the pagination query string), then it's the forme, and certain different sub-actions need to be taken for each
var queryString = '';

try{
if (arg==null) {
  queryString = getURL();
  var sort_option = getSortOption();
  queryString = queryString+"?&sort_options="+sort_option;
  var sort_query = "?&sort_options=" + sort_option;
  }
else if (arg != null) {
  queryString = arg;
  }  
}
catch(err){
//alert(err);
 }


const articleCards_to_replace = document.getElementById("to_be_replaced");
const paginationDiv_to_replace = document.getElementById("pagination_div");


var request = new XMLHttpRequest();

request.onreadystatechange = function() {
  if(request.readyState === 4) {
    
    if(request.status === 200) {
       try{


var replacementsArray = request.responseText.split('<!---->');
//I explicitly put the set of characters shown in parentheses above in the 'cards.html' document so that I could divide the text in 2: pagination html, used to update the pagination section, and html meant to replace the article 'cards' in the body
//alert(replacementsArray);
const pagination_div_replacement = replacementsArray[0];
const article_cards_replacement = replacementsArray[1];

paginationDiv_to_replace.innerHTML = pagination_div_replacement;
articleCards_to_replace.innerHTML = article_cards_replacement;
}
catch(err){
//alert(err);
      }

  }
    else {
      toBeReplaced.innerHTML = 'An error occurred during your request: ' +  request.status + ' ' + request.statusText;
    }
  }
}
 
request.open('Get', queryString);
try{
request.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest');
}
catch(err){
//alert(err);
} 

request.send();

}


