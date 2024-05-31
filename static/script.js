function uploadFile() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];

    if (!file) {
        alert('Please select a file!');
        return;
    }

    let caption = document.getElementById('caption').value;

    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status === 200) {
            const response = JSON.parse(xhttp.responseText);

            const imgElement = document.createElement('img');
            imgElement.src = response.url;

            const captionElement = document.createElement('p');
            captionElement.textContent = response.caption;

            const divResults = document.getElementById('divResults');
            divResults.appendChild(imgElement);
            divResults.appendChild(captionElement);

            alert('File uploaded successfully!');
        } else {
            console.log('Error uploading file!');
            alert('Error uploading file!');
        }
    };

    xhttp.open('POST', '/upload', true);
    let formData = new FormData();
    formData.append('file', file);
    formData.append('caption', caption);

    xhttp.send(formData);
}

function renderPost() {
    fetch('/dashboard')
        .then(response => response.json())
        .then(data => displayPost(data));
}

function displayPost(data) {
    const items = data.results;
    let content = '';
    for (let i = 0; i < items.length; i++) {
        content += `<div><img src="${items[i].url}" alt="Thumbnail" style="width: 120px; height: 120px;"><p>${items[i].caption}</p></div>`;
    }
    document.getElementById("divResults").innerHTML = content;
}

window.onload = function() {
    renderPost();
};

