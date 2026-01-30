document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const loading = document.getElementById('loading');
    const resultCard = document.getElementById('result-card');
    const previewImg = document.getElementById('preview-img');
    const diagnosisText = document.getElementById('diagnosis-text');
    const confidenceVal = document.getElementById('confidence-val');
    const confidenceBar = document.getElementById('confidence-bar');
    const resetBtn = document.getElementById('reset-btn');

    // Click to upload
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    // Reset
    resetBtn.addEventListener('click', () => {
        resultCard.classList.add('hidden');
        dropZone.classList.remove('hidden');
        fileInput.value = '';
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        // Show preview immediately
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // UI State: Loading
        dropZone.classList.add('hidden');
        loading.classList.remove('hidden');
        resultCard.classList.add('hidden');

        // Prepare Upload
        const formData = new FormData();
        formData.append('file', file);

        // Send to Backend
        fetch('/detect', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                loading.classList.add('hidden');
                if (data.error) {
                    alert(data.error);
                    dropZone.classList.remove('hidden');
                    return;
                }
                showResult(data);
            })
            .catch(error => {
                console.error('Error:', error);
                loading.classList.add('hidden');
                dropZone.classList.remove('hidden');
                alert('An error occurred during proper processing.');
            });
    }

    function showResult(data) {
        resultCard.classList.remove('hidden');

        // Update Diagnosis
        diagnosisText.textContent = data.diagnosis;

        // Update Confidence
        const confPercent = Math.round(data.confidence * 100);
        confidenceVal.textContent = `${confPercent}%`;
        confidenceBar.style.width = `${confPercent}%`;

        // Optional: Color coding based on confidence
        // const badge = document.getElementById('diagnosis-badge');
        // badge.style.backgroundColor = confPercent > 80 ? '#d1fae5' : '#fee2e2';
        // badge.style.color = confPercent > 80 ? '#065f46' : '#991b1b';
    }
});
