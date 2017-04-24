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
  var modal = document.getElementsByClassName("modal")[0];
    $.ajax({
        url: '/addMember',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response)
            d = JSON.parse(response)
            console.log(d);
            drawGraph(d);
            getMembers();
            modal.style.display = "none";
            location.reload();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function editMember(){
  event.preventDefault();
  var modal = document.getElementsByClassName("modal")[2];
    $.ajax({
        url: '/editMember',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response)
            d = JSON.parse(response)
            console.log(d);
            drawGraph(d);
            getMembers();
            modal.style.display = "none";
            location.reload();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function removeMember(){
  event.preventDefault();
  var modal = document.getElementsByClassName("modal")[1];
    $.ajax({
        url: '/removeMember',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
          console.log(response)
          d = JSON.parse(response)
          console.log(d);
          drawGraph(d);
          getMembers();
          modal.style.display = "none";
          location.reload();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
