function logout(){
  event.preventDefault();
  $.ajax({
      url: '/logout',
      type: 'POST',
      success: function(response) {
        console.log("logout")
        window.location = "/";
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function controlPanel(){
  window.location = "/";
}
