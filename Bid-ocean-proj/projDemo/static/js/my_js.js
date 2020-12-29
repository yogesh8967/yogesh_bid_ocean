/* function to get csrf token */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


/* calculates total amount when cart page is loaded at first */
$( document ).ready(function() {
    var sum = 0;
    $('.amount').each(function(i, obj) {
        sum += Number(obj.innerHTML);
    });
    document.getElementById("total_amount").innerHTML = "Total Amount: " + sum;
});

/* function when dish Quantity is increased or decreased from cart, deletes the dish from cart if quantity is 0 */
function myFunction(clicked_id) {
    console.log(clicked_id);
    var a = document.getElementById(clicked_id);
    var otherInput = $(a).closest('.qty-bar').find('.qty-box');
    var qty_val = otherInput.val();
    var n = clicked_id.includes("plus");
    var m = clicked_id.includes("minus");
    if (n == Boolean(true)){
        var new_val = parseInt(qty_val) + 1;
        otherInput.attr("value", new_val);
    }
    if (m == Boolean(true)){
        var new_val = parseInt(qty_val) - 1;
        if (new_val == 0){
            a.parentElement.parentElement.parentElement.parentElement.remove(); 
        }
        else{
            otherInput.attr("value", new_val);
        }
    }
    var abc = a.parentElement.parentElement.parentElement.parentElement.children; 
    var otherInput2 = $(abc).closest('.price');
    var otherInput3 = $(a).closest('.item_row').find('.pricee');
    for (var i = 0; i < a.parentElement.parentElement.parentElement.parentElement.childNodes.length; i++) {
        if (a.parentElement.parentElement.parentElement.parentElement.childNodes[i].className == "price") {
            var new_price = a.parentElement.parentElement.parentElement.parentElement.childNodes[i].innerHTML;
        }
        if (a.parentElement.parentElement.parentElement.parentElement.childNodes[i].className == "amount") {
            a.parentElement.parentElement.parentElement.parentElement.childNodes[i].innerHTML = new_val * new_price;
        }
    }
    var sum = 0;
    $('.amount').each(function(i, obj) {
        sum += Number(obj.innerHTML);
    });
    document.getElementById("total_amount").innerHTML = "Total Amount: " + sum;
    document.getElementById(clicked_id);
    console.log(qty_val)
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        headers: { "X-CSRFToken": csrftoken },
        type: "POST",
        url:  "my-ajax-test/",   
        data: {'text' : clicked_id, 'test' : qty_val},   
        dataType: 'json',
        success:  function(response){
               console.log(response);
           }
    });
}


/* function for admin to update the status of order */
function myFunction2(clicked_id) {
    var obj = document.getElementById(clicked_id);
    var st = obj.innerHTML;
    console.log(st)
    if (st == "Pending"){
        console.log("hey")
        obj.innerHTML = "Recieved"
    }
    else if(st == "Recieved"){
        obj.innerHTML = "Pending"
    }
    $.ajax({
        headers: { "X-CSRFToken": csrftoken },
        type: "POST",
        url:  "my-ajax-test2/",   
        data: {'csrfmiddlewaretoken': csrftoken, 'text' : clicked_id, 'test' : st},   
        dataType: 'json',
        success:  function(response){
               alert(response);
           }
    });
}
