
$.ajaxSetup({
  contentType: "application/json; charset=utf-8"
});

var loadPageThenLoadScriptsListed = function(){
  // Handler when the DOM is fully loaded

  //left calendar month toggle
  var left = document.getElementById("left");

  left.addEventListener("click", prevMonth);

  //right calendar month toggle
  var right = document.getElementById("right");

  right.addEventListener("click", nextMonth);

  //get default startTime()
  startTime();

  //display month data
  getCalendarByMonth();


};

if (
    document.readyState === "complete" ||
    (document.readyState !== "loading" && !document.documentElement.doScroll)
) {
  loadPageThenLoadScriptsListed();
} else {
  document.addEventListener("DOMContentLoaded", loadPageThenLoadScriptsListed);
}



function checkTime(i) {
              if (i < 10) {
                i = "0" + i;
              }
              return i;
            }

function startTime() {
  var today = new Date();
  var h = today.getHours();
  var min = today.getMinutes();
  var str = today.toDateString();

  // add a zero in front of numbers<10
  min = checkTime(min);

  document.getElementById("today").innerHTML = str + " " + h + ":" + min ;

  t = setTimeout(function() {
    startTime()
  }, 500);
}

// function myFunc(variable){
//             var s = document.getElementById(variable);
//             s.value = "new value";


function prevMonth() {
  var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", 
                      "December"];

  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentmonth = domMonthYear.textContent.split(" ")[0];

  for(i=0; i<monthNames.length; i++) {
      name = monthNames[i]
      if (name == currentmonth) {
        if (monthNames[i] == monthNames[0]) {
          var reducedYear = parseInt(currentYear) - 1
          var stringYear = reducedYear.toString()
          domMonthYear.innerHTML = monthNames.slice(-1)[0] + " " + stringYear
        } else {
          domMonthYear.innerHTML = monthNames[i-1] + " " + currentYear
        }
    
      }
  }  

}


function nextMonth() {
  var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", 
                      "December"];

  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentMonth = domMonthYear.textContent.split(" ")[0];

  for(i=0; i<monthNames.length; i++) {
      name = monthNames[i]
      if (name == currentMonth) {
        if (monthNames[i] == monthNames.slice(-1)[0]) {
          var increasedYear = parseInt(currentYear) + 1
          var stringYear = increasedYear.toString()
          domMonthYear.innerHTML = monthNames[0] + " " + stringYear
        } else { 
          domMonthYear.innerHTML = monthNames[i+1] + " " + currentYear
        }
      }
  }  

}

function getCalendarByMonth() {
  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentMonth = domMonthYear.textContent.split(" ")[0];

  var data = currentMonth + " " + currentYear

  $.post("/month-days", data, function(response){
    console.log(response, status)
  })

  // .then(
  //     function success(data) {
  //       console.log("success")
  //         if (monthYear !== domMonthYear) {
  //             alert('Something went wrong.  Name is now ' + name);
  //         }
  //     },

  //     function fail(data, status) {
  //       console.log("fail")
  //         alert('Request failed.  Returned status of ' + status);
  //     }
  // );
  // stop link reloading the page
  //event.preventDefault();
}


// function getEvents() {
//   var data = $.get('/month-events')
// }



// function calendar(month) {

//     //Variables to be used later.  Place holders right now.
//     var padding = "";
//     var totalFeb = "";
//     var i = 1;
//     var testing = "";

//     var current = new Date();
//     var cmonth = current.getMonth(); // current (today) month
//     var day = current.getDate();
//     var year = current.getFullYear();
//     var tempMonth = month + 1; //+1; //Used to match up the current month with the correct start date.
//     var prevMonth = month - 1;

//     //Determing if Feb has 28 or 29 days in it.  
//     if (month == 1) {
//         if ((year % 100 !== 0) && (year % 4 === 0) || (year % 400 === 0)) {
//             totalFeb = 29;
//         } else {
//             totalFeb = 28;
//         }
//     }

//     // Setting up arrays for the name of the months, days, and the number of days in the month.
//     var monthNames = ["January", "February", "March", "April", "May", "June",
//                       "July", "August", "September", "October", "November", 
//                       "December"];
//     var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thrusday",
//                     "Friday", "Saturday"];
//     var totalDays = ["31", "" + totalFeb + "", "31", "30", "31", "30", "31", 
//                      "31", "30", "31", "30", "31"];

//     // Temp values to get the number of days in current month, and previous month. Also getting the day of the week.
//     var tempDate = new Date(tempMonth + ' 1 ,' + year);
//     var tempweekday = tempDate.getDay();
//     var tempweekday2 = tempweekday;
//     var dayAmount = totalDays[month];

//     // After getting the first day of the week for the month, padding the other days for that week with the previous months days.  IE, if the first day of the week is on a Thursday, then this fills in Sun - Wed with the last months dates, counting down from the last day on Wed, until Sunday.
//     while (tempweekday > 0) {
//         padding += "<td class='premonth'></td>";
//         //preAmount++;
//         tempweekday--;
//     }
//     // Filling in the calendar with the current month days in the correct location along.
//     while (i <= dayAmount) {

//         // Determining when to start a new row
//         if (tempweekday2 > 6) {
//             tempweekday2 = 0;
//             padding += "</tr><tr>";
//         }

//         // checking to see if i is equal to the current day, if so then we are making the color of that cell a different color using CSS. Also adding a rollover effect to highlight the day the user rolls over. This loop creates the actual calendar that is displayed.
//         if (i == day && month == cmonth) {
//             padding += "<td class='currentday'  onMouseOver='this.style.background=\"#00FF00\"; this.style.color=\"#FFFFFF\"' onMouseOut='this.style.background=\"#FFFFFF\"; this.style.color=\"#00FF00\"'>" + i + "</td>";
//         } else {
//             padding += "<td class='currentmonth' onMouseOver='this.style.background=\"#00FF00\"' onMouseOut='this.style.background=\"#FFFFFF\"'>" + i + "</td>";
//         }
//         tempweekday2++;
//         i++;
//     }


//     // Outputing the calendar onto the site.  Also, putting in the month name and days of the week.
//     var calendarTable = "<table class='calendar'> <tr class='currentmonth'><th colspan='7'>" + monthNames[month] + " " + year + "</th></tr>";
//     calendarTable += "<tr class='weekdays'>  <td>Sun</td>  <td>Mon</td> <td>Tues</td> <td>Wed</td> <td>Thurs</td> <td>Fri</td> <td>Sat</td> </tr>";
//     calendarTable += "<tr>";
//     calendarTable += padding;
//     calendarTable += "</tr></table>";
//     document.getElementById("calendar").innerHTML += calendarTable;

// }
