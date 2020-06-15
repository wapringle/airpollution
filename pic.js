/*
 * Function to load and display an image in a canvas
 * The onload function is called when image is loaded in oder to display same
 */
function loadImage(canvas,src,dwidth,dheight) {
  //var canvas = document.getElementById(cc);
  var ctx = canvas.getContext('2d');
  var img = new Image();
  img.src = src;
  img.onload = function() {
    ctx.drawImage(img, 0, 0,dwidth=dwidth,dheight=dheight);
    img.style.display = 'none';
  };

}
