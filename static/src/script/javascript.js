document.getElementById("uploadForm").onsubmit = function (e) {
  var fileInput = document.getElementById("fileInput");
  var file = fileInput.files[0];
  if (file.size > 10 * 1024 * 1024) {
    alert("File size exceeds 10MB limit");
    e.preventDefault();
  }
};
