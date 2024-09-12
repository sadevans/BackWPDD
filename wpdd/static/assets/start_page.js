let chatSocket;
let gridContainer = document.getElementById('photo-grid');

document.getElementById('start-button').addEventListener('click', function() {
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        console.log('WebSocket уже подключен');
        return;
    }

    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/')
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
        
        if (data.message == 'Success'){
            document.getElementById('start-button').style.display = 'none';
            document.getElementById('pallet-info').style.display = 'block';
        }

        else if (data.type == 'new_pallete_arrived'){
            console.log(data.message);
            
            clearAllPhotos();
            resetCircles();
            document.getElementById('pipelineAnswer').style.display = 'none';
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

            if (data.answer == 'Defect'){
                updatePalleteStatus(data.answer);
            }
            else if (data.photo_id == 5){
                updatePalleteStatus(data.answer);

            }
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

let imageWidth;
function addPhotosToGrid(photoData, photoId) {
    const imgElement = document.createElement('img');
    imgElement.src = `data:image/jpeg;base64,${photoData}`;
    
    if (photoId === 1) {
        imageWidth = imgElement.clientWidth;
        
        const container = document.getElementById('inImageContainer');
        container.innerHTML = ''; 
        container.appendChild(imgElement);
        
        document.getElementById('inImageContainer').style.display = 'flex'; 
        
    } else {
        
        const photoGrid = document.getElementById('photo-grid');
        photoGrid.style.display = 'grid'; 
        photoGrid.appendChild(imgElement);
    }
}


function clearAllPhotos() {
    const inImageContainer = document.getElementById('inImageContainer');
    inImageContainer.innerHTML = ''; 
    const photoGrid = document.getElementById('photo-grid');
    photoGrid.innerHTML = ''; 
    

}


function updateCircleStatus(photoId, status) {
    const circle = document.getElementById(`circle${photoId}`);
    if (circle) {
        if (status === 'OK') {
            circle.style.backgroundColor = '#84C950';
        } else if (status === 'Defect') {
            circle.style.backgroundColor = '#E6341C';}
        // } else {
        //     circle.style.backgroundColor = '#D0D9D9';
        // }
    }
}

function updatePalleteStatus(status) {
    const statusText = document.getElementById('pipelineAnswer');
    if (statusText) {
        if (status === 'OK') {
            statusText.style.backgroundColor = '#84C950';
            statusText.innerText = 'OK';  // Use innerText to update the text
        } else if (status === 'Defect') {
            statusText.style.backgroundColor = '#E6341C';
            statusText.innerText = 'Defect';  // Use innerText to update the text
        } else {
            statusText.style.backgroundColor = '#D0D9D9';
            statusText.innerText = '';  // Clear the text if no valid status
        }
    }
    statusText.style.display = 'block';  // Ensure the element is visible
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