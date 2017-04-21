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

function addMember(){
  event.preventDefault();
    $.ajax({
        url: '/addMember',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response)
            d = JSON.parse(JSON.parse(response))
            drawGraph(d)
        },
        error: function(error) {
            console.log(error);
        }
    });
}
