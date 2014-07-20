
// Angular Stuff
var app = angular.module('QuailWelcome', ['bootstrap-tagsinput']);

app.controller("PageFlipper", function(){
  
  this.next = function() {
    // next tab
    this.page++;
  };

  this.showIfSelected = function() {
    var element = angular.element("")
  };

  this.page = 0;

});


app.controller("BasicInfo", ["$http", function($http){
  this.data = {
    "host": "0.0.0.0",
    "port": 8000,
    "secret": undefined
  }

  this.master = {}

  this.update = function() {
    console.log(this.data)

    $http({
      method: 'GET',
      url: '/quail.json',
      params: {'data': this.data}
    }).success(function(data, status, headers, cfg) {
      console.log(data)
      return data == "OK";
    }).error(function(data, status, headers, cfg) {
      return false;
    });
  };

}]);




app.controller("People", ["$http", "$scope", function($http, $scope) {

  this.people = [
    {
      "name": ["ryan", "gaus"],
      "aliases": ["myself", "I", "my"],
      "birthday": "July 17 12:00:00",
      "tags": ["me"],
      "frequency": 123,
      "cell-phone": "3154640001"
    },
    {
      "name": ["ryan", "gaus"],
      "aliases": ["myself", "I", "my"],
      "birthday": "July 17 12:00:00",
      "tags": ["me"],
      "frequency": 123,
      "cell-phone": "3154640001"
    }
  ]

  this.NewPerson = {
      "fname": "ryan",
      "lname": "gaus",
      "birthday": "",
      "tags": [],
      "frequency": 0,
      "cell-phone": ""
    }


  this.addPerson = function(person) {
    if (person != undefined) {
      this.people.push(person);
    } else {
      this.people.push(this.NewPerson);
      this.NewPerson = {}
    }
  };

  this.addNewPerson = function() {
    this.people.push(this.NewPerson);
    this.NewPerson = {}
  };

  this.removePerson = function(person) {
    console.log( this.people.indexOf(person) )
    this.people.splice( this.people.indexOf(person) )
  };

  this.getTags = function(person) {
    return person.tags.join(", ")
  };

}]);




app.controller("Person", function($http) {

  this.data = {
    "name": ["ryan", "gaus"],
    "aliases": ["myself", "I", "my"],
    "birthday": "July 17 12:00:00",
    "tags": ["me"],
    "frequency": 1,
    "cell-phone": "3154640001"
  }

  this.getTags = function() {
    return this.data.tags.join(", ")
  };

});