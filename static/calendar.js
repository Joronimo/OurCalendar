
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
  todayStartTime();
  

  //load calendar days and month on webpage load
  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentMonth = domMonthYear.textContent.split(" ")[0];
  var month = getMonthNumber(currentMonth)
  var year = parseInt(currentYear)
  number_calendar(month, year);


  sendMonthYearForEvents();


};

//run functions only once the page is ready.
if (
    document.readyState === "complete" ||
    (document.readyState !== "loading" && !document.documentElement.doScroll)
) {
  loadPageThenLoadScriptsListed();
} else {
  document.addEventListener("DOMContentLoaded", loadPageThenLoadScriptsListed);
}
//

function todayStartTime() {

  var today = new Date();
  //Mon Nov 26 2018 00:06:07 GMT-0800 (Pacific Standard Time)
  var month = today.getMonth();
  var day = today.getDate();
  var year = today.getYear();

  startTime(year+1900, month, day);
  }
  

function startTime(year, month, day) {
  // for event list, display the date the events are listed under.


  var date = new Date(year, month, day)
  var str = date.toDateString();
 
  document.getElementById("date").innerHTML = str;


}


function prevMonth() {
  // update calendar and load events based on user click 'left ' on calendar.


  var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", 
                      "December"];

  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentmonth = domMonthYear.textContent.split(" ")[0];

  var month = 0
  var year = 0

  for(i=0; i<monthNames.length; i++) {
      name = monthNames[i]
      if (name == currentmonth) {
        if (monthNames[i] == monthNames[0]) {
          var reducedYear = parseInt(currentYear) - 1
          var stringYear = reducedYear.toString()
          domMonthYear.innerHTML = monthNames.slice(-1)[0] + " " + stringYear
          month = 12
          year = reducedYear
        } else {
          domMonthYear.innerHTML = monthNames[i-1] + " " + currentYear
          month = i-1
          year = parseInt(currentYear)
        }
      }
  } 
  number_calendar(month, year);
  sendMonthYearForEvents(function empty(){}) 
}


function nextMonth() {
  // update calendar and load events based on user click 'forward' on calendar.
  
  var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", 
                      "December"];

  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentMonth = domMonthYear.textContent.split(" ")[0];

  var month = 0
  var year = 0

  for(i=0; i<monthNames.length; i++) {
      name = monthNames[i]
      if (name == currentMonth) {
        if (monthNames[i] == monthNames.slice(-1)[0]) {
          var increasedYear = parseInt(currentYear) + 1
          var stringYear = increasedYear.toString()
          domMonthYear.innerHTML = monthNames[0] + " " + stringYear
          month = 1
          year = increasedYear
        } else { 
          domMonthYear.innerHTML = monthNames[i+1] + " " + currentYear
          month = i+2
          year = parseInt(currentYear)
        }
      }
  }
  number_calendar(month, year);
  sendMonthYearForEvents(function empty(){})  

}

function sendMonthYearForEvents(callback) {
  var domMonthYear = document.getElementById("monthYear");
  var currentYear = domMonthYear.textContent.split(" ")[1];
  var currentMonth = domMonthYear.textContent.split(" ")[0];

  var data = currentMonth + " " + currentYear

  $.post("/month-days", data, function(response){
    console.log("success")
    console.log(response)
    events = response
    

    addClickListenersOnCalButtons(events)

    // for cell in calendar
    //    add onclick call updateSidebarEvents with celldate and events
  })
}




function addClickListenersOnCalButtons(events) {
  var domMonthYear = document.getElementById("monthYear");
  var year = domMonthYear.textContent.split(" ")[1];
  var month = domMonthYear.textContent.split(" ")[0];

  function holdData(event){
    cell = event.target
    day = cell.value
    updateSidebarEvents(day, getMonthNumber(month), parseInt(year));
  }

  var cells = document.getElementsByClassName("calendarCells");
    for (id in cells) {
      cells[id].onclick = holdData
    }

}

function updateSidebarEvents(day, month, year){
  // this will update the sidebar with the given day's event info

  $( ".event_item" ).empty();

  startTime(year, month-1, day);

  var counter = 0
  for (event in events){

    // 1:1 me + thoughts: Array(5)
  // 0: "Jon Green"
  // 1: "2018-11-21 12:00:00"
  // 2: "2018-11-21 12:30:00"
  // 3: "meeting with my thoughts"
  // 4: "Jon Green"
    start_time = events[event][1]
    END_TIMES = events[event][2]
    
    start = start_time.split(" ")[0].split("-")
    //start = ["2018", "11", "21"]
    e_year = parseInt(start[0])
    e_month = parseInt(start[1])
    e_day = parseInt(start[2])

    var t = start_time.split(" ")[1].slice(0, -3) 
    var e = END_TIMES.split(" ")[1].slice(0, -3)
    var time = ""
    time = t + " - " + e

    var event_name = "Event: " + Object.keys(events)[counter]
    var desc = "Description: " + events[event][3]
    var host = "Host: " + events[event][0]
    var invited = "Invited: " + events[event][4]

    if (e_year == year && e_month == month && e_day == day){
      $( ".event_item" ).append( "<div class='ei_Dot dot_active'></div>\
                <div class='ei_Title' id='time'>"+time+"</div>\
                <br>\
                <div class='ei_Copy' id='name'>"+event_name+"</div>\
                <br>\
                <div class='ei_Copy' id='desc'>"+desc+"</div>\
                <br>\
                <div class='ei_Copy' id='host'>"+host+"</div>\
                <br>\
                <div class='ei_Copy' id='who'>"+invited+"</div>\
                <br>" );
    
    counter++; 
      
    }


    }
  

  // ban = "2018-11-21 12:00:00"
  // "2018-11-21 12:00:00"
  // ban.split(" ")[0].split("-")
  // (3) ["2018", "11", "21"]

  console.log("update called on sidebar with: ", day, month, year, events)
}


function getMonthNumber(month) {
  var monthNames = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", 
                    "December"];

  var counter = 0
  for(i=0; i<monthNames.length; i++) {
    counter++;
    if (monthNames[i] == month) {
      return counter
    }

  }

}


function get_number_days(month) {
  var date = new Date(2018, month, 0)
  return date.getDate()
}


function clear_calendar(){
  var cells = document.getElementsByClassName("calendarCells")
  for (ii in cells){
    cells[ii].value = ""
  }
}


function number_calendar(month, year) {

    clear_calendar();

    var names = new Array(7);
    names[0] = "su"
    names[1] = "m"
    names[2] = "tu"
    names[3] = "w"
    names[4] = "th"
    names[5] = "f"
    names[6] = "sa"

    var current_week = 1
    
    for (day=1; day <= get_number_days(month); day++){
      var date = new Date(year, month, day)
      var day_of_week = date.getDay()
      var target_cell_id = names[day_of_week] + current_week
      console.log(target_cell_id, day)

      var id_week = document.getElementById(target_cell_id);
      id_week.value = day

      if(day_of_week == 6){
        current_week++;
      }
      
    }
}



