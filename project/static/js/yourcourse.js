class CourseApp {

    constructor(courseTable) {
        this.courseTable = courseTable
    }

    async getTable() {
        const This = this;
        let response = await fetch("/getcourses", {
            method: "GET"
        });
        if (response.ok) {
            //Get json payload
            const json = await response.json();



            //Delete all rows in the grades view table
            for (var i = 1; i < this.courseTable.rows.length;) {
                console.log("Deleted row:" + this.courseTable.rows[i]);
                this.courseTable.deleteRow(i);
            }
            for (var counter in json.counters) {
                console.log(json.counters[counter].counter_name);
            }

            //Add new rows to the table
            console.log(json)
            Object.keys(json).forEach(key => {
                const course = json[key];

                //Insert row and two cells
                var row = This.courseTable.insertRow();
                var courseNameCell = row.insertCell();
                var profCell = row.insertCell();
                var timeCell = row.insertCell();
                var studentsCell = row.insertCell();
                var addCell = row.insertCell();

                //Set the cell values to the name (key) and grade (json[key])
                courseNameCell.innerText = course.courseName;
                profCell.innerText = course.prof;
                timeCell.innerText = course.time;
                studentsCell.innerText = `${course.enrolled} / ${course.maxEnroll}`;
                addCell.innerHTML = "<button type='button' class='btn btn-primary'>Add</button>";
                console.log();
            });
        } else {
            throw new InternalError(`${response.status}:${await response.text()}`);
        }
    }
}
window.onload = function () {
    const courseTable = document.getElementById('course-table');
    console.log(courseTable === null)

    c = new CourseApp(courseTable);


    c.getTable().catch(error => {
        console.log(error);
    });
}




