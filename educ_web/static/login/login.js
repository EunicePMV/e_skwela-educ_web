document.addEventListener('DOMContentLoaded', function() {
    const submit = document.querySelector("#submit");
    submit.addEventListener('click', function() {
        window.location.replace('/home')
    })
});