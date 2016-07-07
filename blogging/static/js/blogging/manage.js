$(document).ready(function(){
    /**
     * Select All checkbox functionality
     */
    $('#checkall_id').on('click',function(){
        if(this.checked){
            $('.checkbox').each(function(){
                this.checked = true;
            });
        }else{
             $('.checkbox').each(function(){
                this.checked = false;
            });
        }
    });
    
    /**
     * Conditionally filter down each checkbox. Update state of global checkbox
     */
    $('.checkbox').on('click',function(){
        if($('.checkbox:checked').length == $('.checkbox').length){
            $('#checkall_id').prop('checked',true);
        }else{
            $('#checkall_id').prop('checked',false);
        }
    });
});