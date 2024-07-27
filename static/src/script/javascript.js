document.getElementById("uploadForm").onsubmit = function (e) {
  var fileInput = document.getElementById("fileInput");
  var file = fileInput.files[0];
  if (file.size > 10 * 1024 * 1024) {
    alert("File size exceeds 10MB limit");
    e.preventDefault();
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const fileInput = document.querySelector('input[type="file"]');
  const progressBar = document.querySelector("#progress-bar");
  const progressContainer = document.querySelector("#progress-container");
  const submitButton = document.querySelector('input[type="submit"]');

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      alert("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);

    xhr.upload.addEventListener("progress", function (event) {
      if (event.lengthComputable) {
        const percentComplete = (event.loaded / event.total) * 100;
        progressBar.style.width = percentComplete + "%";
        progressBar.innerHTML = Math.floor(percentComplete) + "%";
      }
    });

    xhr.upload.addEventListener("loadstart", function () {
      progressContainer.classList.remove("hidden");
      submitButton.disabled = true;
    });

    xhr.upload.addEventListener("loadend", function () {
      submitButton.disabled = false;
    });

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          window.location.href = xhr.responseURL;
        } else {
          alert("Upload failed");
        }
      }
    };

    xhr.send(formData);
  });
});
