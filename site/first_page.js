// click on sign in: get user name and password and enter to db, call post reqest
function sign_in(){
    var name = document.getElementById("name_in").value;
    var password = document.getElementById("pass_in").value;

   
}

// click on sign up: get user name and password and enter to db, call post reqest
function sign_up(){
    var name = document.getElementById("name_up").value;
    var password = document.getElementById("pass_up_1").value;

     // Post reqesr with name and pass
     $.ajax({
        type: 'POST',
        url: '/api/sign_up/',
        data: JSON.stringify ({name: name, password: password}),
        success: function(data) { alert('data: ' + data); },
        contentType: "application/json",
        dataType: 'json'
    });

     // new window
     window.window.location.replace("second_page.html");
}