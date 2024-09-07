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
        }
        // if (data.type === 'image_batch' && data.images) {
        //     // Добавление нескольких фото в сетку
        //     console.log('here')
        //     addPhotosToGrid(data.images);

        // } 
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



// Функция для динамического добавления фотографий в сетку
function addPhotosToGrid(images) {
    document.getElementById('inImageContainer').style.display = 'block';

    const gridContainer = document.getElementById('photo-grid');
    gridContainer.style.display = 'block';
    images.forEach((image, index) => {
        if (index >= 5) return; // Ограничиваем до 5 фото

        let gridItem = document.createElement('div');
        gridItem.classList.add('grid-item');

        let img = document.createElement('img');
        img.src = 'data:image/jpeg;base64,' + image;
        img.alt = "Dynamic Photo " + (index + 1);
        img.style.display = 'block';

        // Добавляем событие на увеличение фото
        img.onclick = function() {
            openModal(img.src);
        };

        gridItem.appendChild(img);
        gridContainer.appendChild(gridItem);
    });
}


// Функции для модального окна (увеличение фото)
function openModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    modal.style.display = 'flex';
    modalImg.src = imageSrc;
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

function addPhotosToGrid(images) {
    const photoGrid = document.getElementById('photo-grid');

    // Clear previous photos
    photoGrid.innerHTML = '';

    // Define the layout structure
    const layout = ['single', 'double', 'double'];

    // Add photos according to the layout
    let imageIndex = 0;

    for (const section of layout) {
        if (section === 'single' && imageIndex < images.length) {
            // Add single photo spanning full width
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${images[imageIndex]}`;
            img.className = 'single-image';
            photoGrid.appendChild(img);
            imageIndex++;
        } else if (section === 'double' && imageIndex < images.length) {
            // Add two photos in one row
            for (let i = 0; i < 2; i++) {
                if (imageIndex < images.length) {
                    const img = document.createElement('img');
                    img.src = `data:image/jpeg;base64,${images[imageIndex]}`;
                    img.className = 'double-image';
                    photoGrid.appendChild(img);
                    imageIndex++;
                }
            }
        }
    }
}

