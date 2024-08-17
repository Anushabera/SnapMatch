// function checkImages() {
//     const district = document.getElementById('district').value;
//     const taluk = document.getElementById('taluk').value;
    
//     if (district && taluk) {
//         const folderPath = `D_${district}_T_${taluk}/result`;
        
//         // Clear previous images
//         const imageContainer = document.getElementById('image-container');
//         imageContainer.innerHTML = '';

//         // Fetch images from the server
//         fetch(`/get-images?folder=${encodeURIComponent(folderPath)}`)
//             .then(response => response.json())
//             .then(data => {
//                 if (data.images.length === 0) {
//                     imageContainer.innerHTML = '<p>No images found</p>';
//                 } else {
//                     data.images.forEach(image => {
//                         const imgElement = document.createElement('img');
//                         imgElement.src = image;
//                         imgElement.onclick = () => openModal(image); // Attach onclick event
//                         imageContainer.appendChild(imgElement);
//                     });
//                 }
//             })
//             .catch(error => console.error('Error fetching images:', error));
//     }
// }

// function openModal(imageUrl) {
//     const modal = document.createElement('div');
//     modal.className = 'modal';
    
//     const modalContent = document.createElement('img');
//     modalContent.className = 'modal-content';
//     modalContent.src = imageUrl;
    
//     modal.appendChild(modalContent);
//     document.body.appendChild(modal);
    
//     // Close modal when clicked outside of the image
//     modal.onclick = () => closeModal(modal);
// }

// function closeModal(modal) {
//     document.body.removeChild(modal);
// }





///////////////////////////////////    database              //////////////////////////


function checkImages() {
    const district = document.getElementById('district').value;
    const taluk = document.getElementById('taluk').value;
    
    if (district && taluk) {
        // Clear previous images
        const imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = '';

        // Fetch images from the server
        fetch(`/get-images?district=${encodeURIComponent(district)}&taluk=${encodeURIComponent(taluk)}`)
            .then(response => response.json())
            .then(data => {
                if (data.images.length === 0) {
                    imageContainer.innerHTML = '<p>No images found</p>';
                } else {
                    data.images.forEach(image => {
                        const imgElement = document.createElement('img');
                        imgElement.src = image;
                        imgElement.onclick = () => openModal(image); // Attach onclick event
                        imageContainer.appendChild(imgElement);
                    });
                }
            })
            .catch(error => console.error('Error fetching images:', error));
    }
}

function openModal(imageUrl) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    
    const modalContent = document.createElement('img');
    modalContent.className = 'modal-content';
    modalContent.src = imageUrl;
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // Close modal when clicked outside of the image
    modal.onclick = () => closeModal(modal);
}

function closeModal(modal) {
    document.body.removeChild(modal);
}


