$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.modal').modal();
    $("#id_typebusiness").change(function () {
      var url = $("#businessForm").attr("data-categories-url");  // get the url of the `load_cities` view
      var typebusinessId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'typebusiness': typebusinessId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_category").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

    });
  });
