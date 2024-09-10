let chatSocket;

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
            'message': 'Пошел нахуй'
          };
          chatSocket.send(JSON.stringify(message));
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log('Сообщение получено: ', data);

        if (data.message == 'Success'){
            document.getElementById('start-button').style.display = 'none';
            // document.getElementById('inImagesContainer').style.display = 'block';
        }

        // if (data.type === 'image' && data.in_image_url) {
        //     document.getElementById('inImage').src = 'data:image/jpeg;base64,' + data.in_image_url;
        //     document.getElementById('inImage').style.display = 'block';
        // console.log(data.in_image_url)
        console.log(data.images)
        if (data.type === 'image_batch' && data.images){
            console.log('here');
            addPhotosToGrid(data.images);
            console.log('here');

        } else if (data.error) {
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


function addPhotosToGrid(images) {
    console.log('HERE');
    document.getElementById('inImageContainer').style.display = 'block';

    const gridContainer = document.getElementById('photo-grid');
    gridContainer.innerHTML = '';
    gridContainer.style.display = 'grid';

    console.log('Images to render:', images.length);

    
    if (images.length > 0) {
        let largePhotoContainer = document.createElement('div');
        largePhotoContainer.classList.add('grid-item-large');
        let largePhoto = document.createElement('img');
        largePhoto.src = 'data:image/jpeg;base64,' + images[0];
        largePhoto.alt = "Large Dynamic Photo";
        largePhoto.style.display = 'block';

        
        largePhoto.onclick = function() {
            openModal(largePhoto.src);
        };

        largePhotoContainer.appendChild(largePhoto);
        gridContainer.appendChild(largePhotoContainer);
    }

    
    images.slice(1, 5).forEach((image, index) => {
        console.log(`Adding small image ${index + 1}`);

        let smallPhotoContainer = document.createElement('div');
        smallPhotoContainer.classList.add('grid-item-small');

        let smallPhoto = document.createElement('img');
        smallPhoto.src = 'data:image/jpeg;base64,' + image;
        smallPhoto.alt = "Dynamic Photo " + (index + 1);
        smallPhoto.style.display = 'block';

        
        smallPhoto.onclick = function() {
            openModal(smallPhoto.src);
        };

        smallPhotoContainer.appendChild(smallPhoto);
        gridContainer.appendChild(smallPhotoContainer);
    });
}


function openModal(imageSrc) {
    console.log('Открытие изображения на весь экран:', imageSrc);
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