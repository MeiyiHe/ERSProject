var arr = ['foo', 'bar', 'baz'];
var i = 0;
//alert("entered js file")
function nextItem() {
    i = i + 1; 
    i = i % arr.length; 
    return arr[i]; 
}
/*
function prevItem() {
    if (i === 0) { 
        i = arr.length; 
    }
    i = i - 1; 
    return arr[i]; 
}*/

window.addEventListener('click', function () {
    document.getElementById('output_script').textContent = arr[0]; // initial value
/*
    document.getElementById('prev_button').addEventListener(
        'click', // we want to listen for a click
        function (e) { // the e here is the event itself
            document.getElementById('output_script').textContent = prevItem();
        }
    );
  */  
    document.getElementById('next_button').addEventListener(
        'click', // we want to listen for a click
        function (e) { // the e here is the event itself
            document.getElementById('output_script').textContent = nextItem();
        }
    );
});