$j(window).on('load', function(){ 



    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var get_message=document.getElementById('main_message');
    var question_frame_element=document.getElementById('question_frame');

    $j(get_message).hide();

    var next_question=document.getElementById('next_question');
    var previous_question=document.getElementById('previous_question');

window.question_number =1;

    function navigation_question(question_number){
        window.question_number= question_number;
            $j.ajax(

            {

                type:'POST',

                url:'/navigation-question/',


                data:{

                        'csrfmiddlewaretoken':csrftoken,

                        'page_number':question_number,
                    },
                    
                    success :function(response){

                        if (response.next==='false') {
                            $j(next_question).addClass('disabled')
                            console.log('diapsehhjsbhj')
                            }


                        else {

                        if (window.question_number===1) {
                            $j(previous_question).addClass('disabled')
                            }
                        else{
                            $j(previous_question).removeClass('disabled')

                        }


                

                            $j(next_question).removeClass('disabled')



                            question_frame_element.innerHTML=
                                     ` <div class="card">
                                            <div class="card-header">
                                            <input type="hidden" name="csrfmiddlewaretoken" value="${response.csrf_token}">
                                                  
                                              <span class="btn btn-danger ">
                                              Q${question_number} </span> 
                                              <span style="margin-left: 20px;" id='question_title' data='${response.id}'>
                                              ${response.question_title}</span> 
                                            </div>

                                            <div class="card-body">
                                                  <ul class="list-group" style="display: inline;">
                                                        <input type="radio" id="${response.id}1" name="${response.id}" ${response.option_1.student_option}>
                                                        <label for="${response.id}1"><li  class="list-group-item bg-gradient-primary">${response.option_1.text}</li></label><br>
                                                        <input type="radio" id="${response.id}2" name="${response.id}" ${response.option_2.student_option}>
                                                        <label for="${response.id}2"><li  class="list-group-item bg-warning">${response.option_2.text}</li></label><br>
                                                        <input type="radio" id="${response.id}3" name="${response.id}" ${response.option_3.student_option}>
                                                        <label for="${response.id}3"><li  class="list-group-item bg-info">${response.option_3.text}</li></label><br>
                                                        <input type="radio" id="${response.id}4" name="${response.id}" ${response.option_4.student_option}>
                                                        <label for="${response.id}4"><li  class="list-group-item bg-light">${response.option_4.text}</li></label><br>
                                                  </ul>
                                            </div>
                                      </div>
                            `


      
                                        var get_question=document.getElementById('question_title');


                                        
                                        var current_question_id=get_question.getAttribute('data');


                                        var option_1 =document.getElementById(current_question_id+'1');
                                        var option_2 =document.getElementById(current_question_id+'2');
                                        var option_3 =document.getElementById(current_question_id+'3');
                                        var option_4 =document.getElementById(current_question_id+'4');

                                        var all_options=[option_1,option_2,option_3,option_4]

                                        all_options.forEach(item => item.addEventListener('change',
                                                    (event)=>{

                                                                    var option_number=item.id.slice(-1);

                                                                        $j.ajax(

                                                                        {

                                                                            type:'POST',

                                                                            url:'/save-question/',


                                                                            data:{

                                                                                // 'csrfmiddlewaretoken':csrftoken,
                                                                                    'csrfmiddlewaretoken':csrftoken,

                                                                                    'pk':current_question_id,
                                                                                    'option':option_number,

                                                                                },
                                                                                
                                                                                success :function(response){
                                                                                    var question_number_element=document.getElementById('question_number');
                                                                                    var answer_number_element=document.getElementById('answer_number');
                                                                                    question_number_element.textContent=question_number;
                                                                                    answer_number_element.textContent=option_number;
                                                                                    $j(get_message).show();                         
                                                                                }
                                                                        })
                                                            }

                                                        
                                                )
                                            )




                            }

                                     
                    }
            })

    }




    navigation_question(window.question_number)











                                    next_question.addEventListener('click',
                                        (event)=>{

                                            console.log('next');
                                            navigation_question(window.question_number+1);
                                        }


                                        );



                                   previous_question.addEventListener('click',
                                        (event)=>{

                                            console.log('previous');
                                            navigation_question(window.question_number-1);
                                        }


                                        );




});










