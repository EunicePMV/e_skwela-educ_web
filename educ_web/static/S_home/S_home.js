document.addEventListener('DOMContentLoaded', function() {
    const addCourse = document.querySelector("#add-course");
    addCourse.addEventListener('submit', () => add_course());
});

function add_course() {
    console.log("add course here");
}