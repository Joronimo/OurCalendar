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
startTime();