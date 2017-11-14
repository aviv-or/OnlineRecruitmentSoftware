$( document ).ready(function(){
    $('.form-field .field-input').focusin(function(event){
        target = $(event.target);
        icon = target.parent().find('.field-icon');
        icon.addClass("field-icon-active");
        target.addClass("field-input-active");
    });

    $('.form-field .field-input').focusout(function(event){
        target = $(event.target);
        icon = target.parent().find('.field-icon');
        val = target.val();
        if (val != "")
            return;
        target.removeClass("field-input-active");
        icon.removeClass("field-icon-active");
    });

    $('.form-field .field-input').keyup(function(event){
        target = $(event.target);
        clear = target.parent().find('.field-clear');
        val = target.val();
        if (val != "")
            clear.addClass("field-clear-active");
        else
            clear.removeClass("field-clear-active");
    });

    $('.form-field .field-input').change(function(event){
        target = $(event.target);
        clear = target.parent().find('.field-clear');
        icon = target.parent().find('.field-icon');
        val = target.val();
        if (val != "")
            clear.addClass("field-clear-active");
        else
            clear.removeClass("field-clear-active");
    });

    $('.form-field .field-clear span').click(function(event){
        target = $(event.target);
        input = target.parent().parent().find('.field-input');
        icon = target.parent().parent().find('.field-icon');
        input.val("")
        target.parent().removeClass("field-clear-active");
        icon.removeClass("field-icon-active");
        input.focus()
    });

});