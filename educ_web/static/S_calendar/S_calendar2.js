document.addEventListener("DOMContentLoaded", function() {
    generateCalendar()
    assignIDtoDiv()
    dueDateActivate()
})

function assignIDtoDiv(){
    let days = document.getElementsByClassName('day')
    let weeks = document.getElementsByClassName('week')
    for(let i = 0; i < days.length; i++){
        if(days[i].innerHTML){
            days[i].id = `day-${days[i].innerHTML}`
            days[i].onclick = activateDayCard 
        }
    }
    for(let i = 0; i < weeks.length; i++){
        weeks[i].id = `week-${i}`
    }
}
function activateDayCard(){
    let week = this.parentNode.parentNode
    let task = week.children[1]
    let activatedDay = document.getElementsByClassName('activated')
    if(activatedDay.length > 0){
        let activated = activatedDay[0]
        let activeTask = activated.parentNode.parentNode.children[1]
        if(activated.parentNode !== this.parentNode || activated === this){
            activeTask.id = ``
            activeTask.style.maxHeight = `0px` 
            activeTask.style.border = `none`
        }
        activated.classList.remove('activated')
        if(activated === this) return
    }
    if(this.classList.contains('active')){
        this.classList.add('activated')
        task.id = 'activeTask'
        task.style.maxHeight = `${task.scrollHeight + 10}px `
        task.style.border = '1px solid var(--border-color)'
    }
}
function weekCount(year, month_number) {
    var firstOfMonth = new Date(year, month_number, 1);
    var lastOfMonth = new Date(year, month_number + 1, 0);

    var used = firstOfMonth.getDay() + lastOfMonth.getDate();
    
    return Math.ceil( used / 7);
}
function daysInMonth (month, year) {
    return new Date(year, month, 0).getDate();
}

const current = new Date()
const monthName = document.getElementById('monthName')
const calendar = document.getElementById('calendar')
const monthRef = ["January","February","March","April","May","June","July","August","September","October","November","December"];
function generateCalendar(){
    monthName.innerHTML = monthRef[current.getMonth()]
    monthName.dataset.currentMonth = current.getMonth()

    renderCalendar();
}

function dueDateActivate() {
    month = monthName.innerText;
    let userId = document.querySelector("#user-id-calendar");
    userId = userId.className.slice(9, 11).trim();
    fetch(`/task/${userId}`)
    .then(response => response.json())
    .then(task => {

        for(let i=0; i<task.tasks.length; i++) {
            if(task.tasks[i].due_month === month) {
                const taskDueDate = document.querySelector(`#day-${task.tasks[i].due_date}`);
                console.log("taskDueDate: ", taskDueDate);
                taskDueDate.classList.add('active');
                const taskSummary = taskDueDate.parentNode.nextSibling;
                const taskContent = taskSummary.lastChild

                const taskContainer = document.createElement('div');
                taskContainer.style.paddingLeft = "1.5rem";
                taskContainer.style.fontSize = "1.25rem"
                taskContainer.innerHTML = `<strong>${task.tasks[i].title} in course ${task.tasks[i].course}</strong>`;

                taskContent.append(taskContainer)
            }
        }
    });
}

function renderCalendar(){
    console.log(monthName.innerText);
    for(let week=0, date=1; week < weekCount(current.getFullYear(), Number(monthName.dataset.currentMonth)); week++){
        let weekRow = createWeekRow()
        let days = weekRow.children[0]
        for(let day = 0; day < 7; day++){
            let dayCard = document.createElement('div')
            dayCard.className = 'day'

            let firstDay = new Date(current.getFullYear(), Number(monthName.dataset.currentMonth), 1)
            let valid = date <= daysInMonth(Number(monthName.dataset.currentMonth)+1, current.getFullYear())
            if(date === 1 && day === firstDay.getDay()){
                dayCard.innerHTML = `${date}`
                date++
            }else if(date !== 1 && valid){
                dayCard.innerHTML = `${date}`
                date++
            }

            // if(day===0 && dayCard.innerHTML) dayCard.classList.add('active')

            days.appendChild(dayCard)
        }
        calendar.appendChild(weekRow)
    }
}

function createDayCard(id, week){
    let card = document.createElement('div')
    card.classList.add('day')
    card.id = `day-${id}`
    week.append(id)
}
function createWeekRow(){
    let week = document.createElement('div')
    let days = document.createElement('div')
    let task = document.createElement('div')
    let taskHeader = document.createElement('div')
    let tasks = document.createElement('div')
    week.className = `week`
    days.className = `days`
    task.className = `task`
    tasks.className = `tasks`
    taskHeader.className = `taskHeader`
    taskHeader.innerHTML = `Task Summary`
    task.appendChild(taskHeader)
    task.appendChild(tasks)
    week.appendChild(days)
    week.appendChild(task)
    return week
}
function prev(){
    let month = monthName.dataset.currentMonth
    month = Number(month)
    if(month <= 0) return
    monthName.dataset.currentMonth = month - 1 
    monthName.innerHTML = monthRef[month-1]
    removeWeeks()
    renderCalendar()
    assignIDtoDiv()
    dueDateActivate()
}

function next(){
    let month = monthName.dataset.currentMonth
    month = Number(month)
    if(month >= 11) return
    monthName.dataset.currentMonth = month + 1
    monthName.innerHTML = monthRef[month+1]
    removeWeeks()
    renderCalendar()
    assignIDtoDiv()
    dueDateActivate()
}
function removeWeeks(){
    const elements = document.getElementsByClassName('week');
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}

// let activated = null
// function linkTaskToDay(){
//     var active = $("div").find(".active")
//     for(let i = 0; i < active.length; i++){
//         let day = $(active[i])
//         $(day).click(function (e) { 
//             e.preventDefault()
//             let sameParent = $(this).parent().parent().attr('id') === 
//             $(activated).parent().parent().attr('id')
//             let deactivate = false
//             if(this === activated){
//                 deactivate = true
//             }else if (!sameParent){
//                 let tasks = $("div").find(".task")
//                 for(let i = 0; i < tasks.length; i++){
//                     $(tasks[i]).css({
//                         "maxHeight":"0", 
//                         "border":"none",
//                     })
//                 }
//             }
//             activated = this
//             for(let i = 0; i < active.length; i++){
//                 $(active[i]).css({
//                     "border": "none",
//                 })
//             }
            
//             let task = $($(this).parent().siblings()[0])
//             if ($(task).height() && (!sameParent || deactivate)) {
//                 $(task).css({
//                     "maxHeight":"0", 
//                     "border":"none",
//                 });
//             } else {
//                 $(this).css({
//                     "border": "2px solid var(--border-color)",
//                 })
//                 $(task).css({
//                     "maxHeight": ($(task).prop('scrollHeight') + 10) + "px",
//                     "border":"1px solid var(--border-color)",
//                 });
//                 tasks = $(task).children()[1]
//                 list = $(tasks).children()[0]
//                 $(list).html(`<li>${$(this).html()}</li>`)
                
//             }
//         });
//     }
// }

// function bindIDtoDiv(){
//     var days = $("div").find(".day")
//     var weeks = $("main").find(".week")
//     for(let i = 0, j = 1; i < days.length; i++){
//         let day = $(days[i])
//         if($(day).text() != ""){
//             $(day).attr('id', "day-"+j)
//             j++
//         }
//     }for(let i = 0; i < weeks.length; i++){
//         $(weeks[i]).attr('id', "week-"+(i+1))
//     }
// }