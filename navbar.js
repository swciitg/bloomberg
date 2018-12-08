
$("#suscribe").on("click", function(){
    $(".popup-overlay, .popup-content").addClass("active");
    $("#pop-up-background").addClass("active"); 
    //$("#body").hide();
  });
  
  //removes the "active" class to .popup and .popup-content when the "Close" button is clicked 
  $("#close,.close").on("click", function(){
    $(".popup-overlay, .popup-content").removeClass("active");
    $("#pop-up-background").removeClass("active"); 
  }); 
  