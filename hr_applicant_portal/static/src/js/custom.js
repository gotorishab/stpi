
$(document).ready(function(){
    $('#advertisement_ids').on('change', function(){
        $.ajax({
            url: '/getJobName',
            type: 'POST',
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
                        html_content += "<option name='courses.id' value='"+response_data[i][0]+"'>"+response_data[i][1]+"</option>";
                    }
                    document.getElementById('job_ids').innerHTML = html_content;
                }
                else{
                    document.getElementById('advertisement_ids').innerHTML = "<option value=''/>";
                }

            },
            error: function(response) {
                alert('Error : '+response);
            }
        });
    });
});