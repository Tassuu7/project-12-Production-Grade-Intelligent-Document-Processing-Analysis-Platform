/* Drag & Drop Multi-file Uploader */

function initUploader(dropzoneId, fileInputId, fileListId, uploadBtnId) {
    const dropzone = document.getElementById(dropzoneId);
    const fileInput = document.getElementById(fileInputId);
    const fileList = document.getElementById(fileListId);
    const uploadBtn = document.getElementById(uploadBtnId);

    if (!dropzone || !fileInput) return;

    let selectedFiles = [];

    dropzone.addEventListener('click', () => fileInput.click());
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    });

    fileInput.addEventListener('change', () => {
        const files = Array.from(fileInput.files);
        handleFiles(files);
    });

    function handleFiles(files) {
        selectedFiles = [...selectedFiles, ...files];
        renderFileList();
    }

    function renderFileList() {
        if (!fileList) return;
        fileList.innerHTML = '';
        
        selectedFiles.forEach((file, index) => {
            const row = document.createElement('div');
            row.className = 'card';
            row.style.marginBottom = '0.5rem';
            row.style.padding = '0.75rem 1rem';
            row.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${file.name}</strong>
                        <span style="color: var(--slate-500); font-size: 0.8rem; margin-left: 0.5rem;">
                            (${(file.size / 1024).toFixed(1)} KB)
                        </span>
                    </div>
                    <button type="button" class="btn btn-sm btn-secondary" onclick="removeFile(${index})">Remove</button>
                </div>
            `;
            fileList.appendChild(row);
        });

        if (uploadBtn) {
            uploadBtn.disabled = selectedFiles.length === 0;
        }
    }

    window.removeFile = (index) => {
        selectedFiles.splice(index, 1);
        renderFileList();
    };

    if (uploadBtn) {
        uploadBtn.addEventListener('click', async () => {
            if (selectedFiles.length === 0) return;
            
            uploadBtn.disabled = true;
            uploadBtn.innerText = 'Uploading...';

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });

            try {
                const res = await API.request('/api/v1/documents/upload', {
                    method: 'POST',
                    body: formData
                });

                showToast(`Successfully uploaded ${selectedFiles.length} documents! Processing queued.`, 'success');
                selectedFiles = [];
                renderFileList();
                setTimeout(() => {
                    const u = API.getCurrentUser();
                    if (u && u.role === 'admin') {
                        window.location.href = '/admin/documents';
                    } else {
                        window.location.href = '/dashboard';
                    }
                }, 800);
            } catch (err) {
                showToast(err.message, 'error');
                uploadBtn.disabled = false;
                uploadBtn.innerText = 'Upload Selected Documents';
            }
        });
    }
}
