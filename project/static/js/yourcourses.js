function getAllGrades() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/coursetest");
    xhttp.onload = function() {
        format(this.responseText);
    }; 
    xhttp.send();
}
function format(data) {
    let parsed = JSON.parse(data);
    let table = "<table><tr><th>Course Name</th><th>Teacher</th><th>Time</th><th>Student Enrolled</th><th>Add Class</th></tr>";
    for (let i = 0; i < parsed.length; i++) {
        //table += "<tr><td>" + parsed[i].name + "</td><td>" + parsed[i].grade + "</td></tr>";
        table += "<tr><td>" + parsed[i].name + "</td><td>" + parsed[i].teacher + "</td><td>" + parsed[i].time + "</td><td>" + parsed[i].students + "</td><td><button type='button' class='btn btn-primary'>Add</button></td></tr>";
    }
    table += "</table>";
    document.getElementById("output").innerHTML = table;
}