
$(document).ready(function(){

    $('#dob').on('change', function(){
        var dateString = $(this).val();
        var myDate = new Date(dateString);
        var today = new Date();
        if ( myDate > today ) { 
            alert("You cannot enter a date in the future!");
            $('#dob')[0].value = '';
            return false;
        }
        return true;
    });

    $('.advertisement_line_id').on('change', function(){
        $.ajax({
            url: '/getJobName',
            type: 'GET',
            data : {'advertisement_ids': $(this).val()},
            beforeSend : function() {
//                    $("#loader").css('display', 'block');
                $(".custom_preloader").css("display", "block");
            },
            complete : function() {
//                    $("#loader").css("display", "none");
                $(".custom_preloader").css("display", "none");
            },
            success: function(response){
                if (response != undefined){
                    var response_data = JSON.parse(response)['result'];
                    var html_content = "<option value=''>Select</option>";
                    for(var i=0;i<response_data.length;i++){
                        html_content += "<option id='course_id' name='courses.id' value='"+response_data[i][0]+"'>"+response_data[i][1]+"</option>";
                    }
                    $(".job_id").append(html_content);
                }
                else{
                    $("option").remove("#course_id");
                    $(".job_id").append("<option value=''/>");
                }

            },
            error: function(response) {
                alert('Error : '+response);
            }
        });
    });
});