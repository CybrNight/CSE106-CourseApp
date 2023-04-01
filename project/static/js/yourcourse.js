courseTable = document.getElementById('output');

async function getTable() {
    let response = await fetch("/getcourses", {
        method: "GET",
        headers: {
            'Accept': 'application/json',
        }
    });
    if (response.ok) {
        //Get json payload
        const json = await response.json();

        //Delete all rows in the grades view table
        for (var i = 1; i < courseTable.rows.length;) {
            console.log("Deleted row:" + courseTable.rows[i]);
            courseTable.deleteRow(i);
        }

        //Add new rows to the table
        Object.keys(json).forEach(function (key) {

            //Insert row and two cells
            var row = gradesTable.insertRow();
            var courseNameCell = row.insertCell();
            var profCell = row.insertCell();
            var timeCell = row.insertCell();
            var studentsCell = row.insertCell();
            var addCell = row.insertCell();

            //Set the cell values to the name (key) and grade (json[key])
            courseNameCell.innerText = json["courseName"]
            profCell.innerText = json["prof"]
            timeCell.innerText = json["time"]
            studentsCell.innerText = json["enrolled"] / json["maxEnrolled"]
            addCell.innerHTML = "<button type='button' class='btn btn-primary'>Add</button>"
            console.log();
        });
    } else {
        throw new InternalError(`${response.status}:${await response.text()}`);
    }
}

getTable();
