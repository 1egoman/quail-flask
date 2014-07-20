// initialize bootstrap
$(document).ready(function(){

  // create popovers
  $('.event').popover({
    animation: true,
    trigger: "hover",
    placement: "bottom",
    html: true,
    offset: 10,
    template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'

  });

});

(function(){
  var app = angular.module('QuailApp', []);

  app.controller("CalController", function(){

    // calendar events
    this.events = [
      {
        "name": "TestEvent",
        "date": "Fri Jul 19 2014 10:00:00",
        "color": "red"
      },
      {
        "name": "TestEventTwo",
        "date": "Sat Jul 20 2014 10:00:00",
        "color": "green"
      }
    ]

    // constant date names
    this.monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    this.dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat'];


    // get a list of events that occer on the specified month, day, and year
    this.GetEventsOn = function(day, month, year) {
        
      // all parts specified?
      if ( day === undefined) { day = new Date().getDay() }
      if ( month === undefined) { month = new Date().getMonth()+1 }
      if ( year === undefined) { year = new Date().getFullYear() }

      var out = [];
      var d = this.dayNames[ day % 7 ] + " " + this.monthNames[month-1] + " " + day + " " + year

      for (i = 0; i < this.events.length; i++) {
        var evt = this.events[i];
        if ( evt.date.indexOf(d) > -1 ) {
          out.push(evt)
        }
      };
      return out;
    };



    // get the amount of days in the month specified
    this.GetDaysInMonth = function(month, year) {

      // month/year specified?
      if ( month === undefined && year === undefined ) {
        year = new Date().getYear()
        month = new Date().getMonth()+1
      }

      // get day number
      isLeap = new Date(year, 1, 29).getMonth() == 1
      amt = [31, (isLeap ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1];

      // construct array
      // return Array.apply(null, {length: amt+1}).map(Number.call, Number)
      out = [];
      wk = -1;
      for (i = 0; i < amt+1; i++) {
        if (i % 8 == 0) {
          wk++;
          out.push([]);
        } else {
          out[wk].push(i);
        }
      }
      console.log(out)
      return out;

    }



  });

})()