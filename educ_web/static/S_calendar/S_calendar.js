
function bindIDtoDiv(){
    var days = $("div").find(".day")
    var weeks = $("main").find(".week")
    for(let i = 0, j = 1; i < days.length; i++){
        let day = $(days[i])
        if($(day).text() != ""){
            $(day).attr('id', "day-"+j)
            j++
        }
    }for(let i = 0; i < weeks.length; i++){
        $(weeks[i]).attr('id', "week-"+(i+1))
    }
}

let activated = null
function linkTaskToDay(){
    var active = $("div").find(".active")
    for(let i = 0; i < active.length; i++){
        let day = $(active[i])
        $(day).click(function (e) { 
            e.preventDefault()
            let sameParent = $(this).parent().parent().attr('id') === 
                                $(activated).parent().parent().attr('id')
            let deactivate = false
            if(this === activated){
                deactivate = true
            }else if (!sameParent){
                let tasks = $("div").find(".task")
                for(let i = 0; i < tasks.length; i++){
                    $(tasks[i]).css({
                        "maxHeight":"0", 
                        "border":"none",
                    })
                }
            }
            activated = this
            for(let i = 0; i < active.length; i++){
                $(active[i]).css({
                    "border": "none",
                })
            }

            let task = $($(this).parent().siblings()[0])
            if ($(task).height() && (!sameParent || deactivate)) {
                $(task).css({
                    "maxHeight":"0", 
                    "border":"none",
                });
            } else {
                $(this).css({
                    "border": "2px solid var(--border-color)",
                })
                $(task).css({
                    "maxHeight": ($(task).prop('scrollHeight') + 10) + "px",
                    "border":"1px solid var(--border-color)",
                });
                tasks = $(task).children()[1]
                list = $(tasks).children()[0]
                $(list).html(`<li>${$(this).html()}</li>`)
            
            }
        });
    }
}
function prev(){

}

function next(){

}

bindIDtoDiv()
linkTaskToDay()