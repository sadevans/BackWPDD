let chatSocket;
let gridContainer = document.getElementById('photo-grid');

document.getElementById('start-button').addEventListener('click', function() {
    console.log(chatSocket)
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        console.log('WebSocket уже подключен');
        return;
    }

    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
    console.log(chatSocket)


    chatSocket.onopen = function() {
        console.log('WebSocket соединение установлено');
        const message = {
            'message': 'WebSocket соединение установлено'
          };
          chatSocket.send(JSON.stringify(message));
    };


    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data.message)
        
        if (data.message == 'Success'){
            document.getElementById('start-button').style.display = 'none';
            document.getElementById('pallet-info').style.display = 'block';
        }

        else if (data.type == 'new_pallete_arrived'){
            console.log(data.message);
            clearGrid();
            resetCircles();
            document.getElementById('pallete_id').innerText = `Pallete ID: ${data.pallete_id}`;
        }
        else if (data.type == 'camera_done'){
            mes = `Camera №${data.camera_id} has taken ${data.num_photos} photo...`;
            console.log(mes);

        }else if (data.type=='pipeline_log'){
            mes = data.message;
            console.log(mes);
            addPhotosToGrid(data.images, data.photo_id);
            updateCircleStatus(data.photo_id, data.answer_text);

        }
        else if (data.type == 'pipeline_send_answer'){
            console.log(data.message);
            console.log(data.images.length);
            console.log(data.answer);
        }
        
         else if (data.error) {
            console.error('Error received: ', data.error);
            statusElement.innerText = 'Status: Error';
        }

    };

    chatSocket.onclose = function(e) {
        console.error('WebSocket connection closed unexpectedly');
        statusElement.innerText = 'Status: Disconnected';
        
        document.getElementById('start-button').style.display = 'block';
        document.getElementById('inImageContainer').style.display = 'none';
        document.getElementById('inImage').style.display = 'none';

    };
});


function addPhotosToGrid(images, photo_id) {

    document.getElementById('inImageContainer').style.display = 'block';

    const isGridEmpty = gridContainer.children.length === 0;

    if (isGridEmpty && photo_id == 1) {
        let largePhotoContainer = document.createElement('div');
        largePhotoContainer.classList.add('grid-item-large');

        let largePhoto = document.createElement('img');
        largePhoto.src = 'data:image/jpeg;base64,' + images[0];
        largePhoto.alt = "Large Dynamic Photo";
        largePhoto.style.display = 'block';

        largePhoto.onclick = function () {
            openModal(largePhoto.src);
        };

        largePhotoContainer.appendChild(largePhoto);
        gridContainer.appendChild(largePhotoContainer);
    } 
    
    else if (!isGridEmpty && photo_id >= 2) {
        images.forEach((image, index) => {
            let photoContainer = document.createElement('div');
            photoContainer.classList.add('grid-item-small');

            let photo = document.createElement('img');
            photo.src = 'data:image/jpeg;base64,' + image;
            photo.alt = "Dynamic Photo " + (index + 1);
            photo.style.display = 'block';

            photo.onclick = function () {
                openModal(photo.src);
            };

            photoContainer.appendChild(photo);
            gridContainer.appendChild(photoContainer);
        });
    }
}


function clearGrid() {
    gridContainer.innerHTML = '';
}


function updateCircleStatus(photoId, status) {
    const circle = document.getElementById(`circle${photoId}`);
    if (circle) {
        if (status === 'OK') {
            circle.style.backgroundColor = '#84C950';
        } else if (status === 'Defect') {
            circle.style.backgroundColor = '#E6341C';
        } else {
            circle.style.backgroundColor = '#D0D9D9';
        }
    }
}


function resetCircles() {
    for (let i = 1; i <= 5; i++) {
        const circle = document.getElementById(`circle${i}`);
        if (circle) {
            circle.style.backgroundColor = '#D0D9D9';
        }
    }
}


function openModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    modal.style.display = 'flex';
    modalImage.src = imageSrc;


    modalImage.onclick = function() {
        closeModal();
    };
}


function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}


function resetIndicators() {
    for (let i = 1; i <= 5; i++) {
        document.getElementById(`photo-status-${i}`).style.backgroundColor = 'grey';
    }
}