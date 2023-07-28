let sAB = $("#selectButton")
let sAA = $("#selectCheck")
let sAS = $(".tickboxes")

$(sAA).change(function (e) { 
    e.preventDefault();
    let is_checked = $(this).prop("checked")
    if(is_checked){
        for(let i = 0; i < sAS.length; i++){
            $(sAS[i]).addClass("toggled")
            $(sAS[i]).prop("checked", true)
            $(sAB).prop("disabled", false)
        }
    }else{
        for(let i = 0; i < sAS.length; i++){
            $(sAS[i]).removeClass("toggled")
            $(sAS[i]).prop("checked", false)
            $(sAB).prop("disabled", true)
        }
    }
});

for(let i = 0; i < sAS.length; i++){
    $(sAS[i]).change(function (e) { 
        e.preventDefault();
        let is_checked = $(this).prop("checked")
        let checked
        if(!is_checked){
            $(this).removeClass("toggled")
            $(sAA).prop("checked", false)
            checked = $(".toggled")
        }else{
            $(this).addClass("toggled")
            checked = $(".toggled")
            if(checked.length == sAS.length){
                $(sAA).prop("checked", true)
            }
        }
        if(checked.length == 0){
            $(sAB).prop("disabled", true)
        }else{
            $(sAB).prop("disabled", false)
        }
    });
}