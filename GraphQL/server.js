fs = require('fs')
fs.readFile('/etc/shadow', 'utf8', function (err,data) {
	  if (err) {
		      return console.log(err);
		    }
	  console.log(data);
});
