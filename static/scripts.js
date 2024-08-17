document.getElementById('file1').onchange = function (event) {
    var reader = new FileReader();
    reader.onload = function () {
        document.getElementById('imgPreview1').src = reader.result;
        document.getElementById('imgPreview1').style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
};

document.getElementById('file2').onchange = function (event) {
    var reader = new FileReader();
    reader.onload = function () {
        document.getElementById('imgPreview2').src = reader.result;
        document.getElementById('imgPreview2').style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
};

document.getElementById('uploadForm').onsubmit = async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.text();
    document.getElementById('result').innerText = result;
};
