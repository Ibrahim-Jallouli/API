function displayImage() {
    var fileInput = document.getElementById('file');
    var imageContainer = document.getElementById('imageContainer');
    var uploadedImage = document.getElementById('uploadedImage');

    var file = fileInput.files[0];

    if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            uploadedImage.src = e.target.result;
            imageContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        uploadedImage.src = '#';
        imageContainer.style.display = 'none';
    }
}

function applyTransformation(transformation) {
    var uploadedImage = document.getElementById('uploadedImage');
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = uploadedImage.width;
    canvas.height = uploadedImage.height;
    context.drawImage(uploadedImage, 0, 0, canvas.width, canvas.height);

    // Préparez les données à envoyer au serveur
    var imageDataURL = canvas.toDataURL('image/png');
    var data = JSON.stringify({ 'transformation': transformation, 'image_data': imageDataURL });

    // Utilisez AJAX pour envoyer la requête au serveur
    var xhr = new XMLHttpRequest();
    // Modifiez le chemin de la requête POST en fonction de la transformation spécifiée
    xhr.open('POST', '/' + transformation, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            uploadedImage.src = response['image_url'];
        }
    };

    xhr.send(data);
}

function downloadImage() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/download_image', true);
    xhr.responseType = 'blob';

    xhr.onload = function () {
        var blob = new Blob([xhr.response], { type: 'image/png' });
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'modified_image.png';
        link.click();
    };

    xhr.send();
}

function resetImage() {
    // Rechargez l'image d'origine
    displayImage();
}
