document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');
    studentScores = document.querySelectorAll('.score-input');
    studentScores.forEach(studentScore => {
        studentScore.addEventListener('change', function(e) {
            stringId = studentScore.className.slice(11, 18).trim();
            id = stringId.split("-")

            const grade = studentScore.value;
            console.log(`/submission/${id[0]}/${id[1]}/${id[2]}`);

            // get student.id course.id and task.id
            fetch(`/submission/${id[0]}/${id[1]}/${id[2]}`, {
                method: 'PUT',
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    grade: grade
                })
            })
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}