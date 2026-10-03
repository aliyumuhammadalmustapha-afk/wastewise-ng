/**
 * scanner.js — WasteWise NG Waste Scanner
 * Clean editorial UI controller for upload, live camera, AI classification, item selection, and result rendering
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const uploadTabBtn = document.getElementById('tab-upload-btn');
    const cameraTabBtn = document.getElementById('tab-camera-btn');
    const uploadPanel = document.getElementById('upload-panel');
    const cameraPanel = document.getElementById('camera-panel');
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('dropzone-file');
    const previewCard = document.getElementById('preview-card');
    const previewImage = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const removePreviewBtn = document.getElementById('remove-preview-btn');
    const classifyBtn = document.getElementById('classify-btn');
    const loadingState = document.getElementById('loading-state');
    const statusMessageBox = document.getElementById('scan-status-message');
    const categoryResult = document.getElementById('category-result');
    const detectedCategoryEl = document.getElementById('detected-category');
    const confidenceBadgeEl = document.getElementById('confidence-badge');
    const itemSelectionGrid = document.getElementById('itemSelectionGrid') || document.getElementById('item-selection-grid');
    const resultCard = document.getElementById('result-card');

    // Camera elements
    const startCameraBtn = document.getElementById('start-camera-btn');
    const captureCameraBtn = document.getElementById('capture-camera-btn');
    const cameraVideo = document.getElementById('camera-video');
    const cameraCanvas = document.getElementById('camera-canvas');
    const cameraPlaceholder = document.getElementById('camera-placeholder');

    let currentFile = null;
    let cameraStream = null;
    let classifiedCategory = null;
    let classifiedConfidence = 0;
    let isClassifying = false;

    // Helper: Get CSRF token
    function getCsrfToken() {
        const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (input && input.value) return input.value;
        const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[2]) : '';
    }

    // Helper: Show status message
    function showStatus(message, type = 'info') {
        if (!statusMessageBox) return;
        if (!message) {
            statusMessageBox.style.display = 'none';
            statusMessageBox.innerHTML = '';
            return;
        }
        statusMessageBox.style.display = 'block';
        const badgeClass = type === 'error' ? 'badge-hazardous' : type === 'success' ? 'badge-safe' : 'badge-category';
        statusMessageBox.innerHTML = `<div class="badge ${badgeClass}" style="width:100%;padding:10px 14px;border-radius:10px;justify-content:center;text-transform:none;letter-spacing:normal;font-size:13px;">${message}</div>`;
        if (window.lucide) lucide.createIcons();
    }

    // Tab Switching
    function setTab(mode) {
        if (mode === 'upload') {
            uploadTabBtn.className = 'btn-primary';
            cameraTabBtn.className = 'btn-secondary';
            uploadPanel.style.display = 'block';
            cameraPanel.style.display = 'none';
            stopCamera();
        } else {
            uploadTabBtn.className = 'btn-secondary';
            cameraTabBtn.className = 'btn-primary';
            uploadPanel.style.display = 'none';
            cameraPanel.style.display = 'block';
        }
        if (window.lucide) lucide.createIcons();
    }

    if (uploadTabBtn) uploadTabBtn.addEventListener('click', () => setTab('upload'));
    if (cameraTabBtn) cameraTabBtn.addEventListener('click', () => setTab('camera'));

    // File Handling
    function handleFile(file) {
        if (!file) return;
        if (!file.type.match(/^image\/(jpeg|png|jpg|webp)$/i)) {
            showStatus('Please select a JPG or PNG image file.', 'error');
            return;
        }
        if (file.size > 8 * 1024 * 1024) {
            showStatus('Image file is too large (maximum 8MB).', 'error');
            return;
        }

        currentFile = file;
        showStatus('');

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewFilename.textContent = file.name || 'Captured Waste Photo';
            dropzone.style.display = 'none';
            previewCard.style.display = 'block';
            categoryResult.style.display = 'none';
            resultCard.style.display = 'none';
            if (window.lucide) lucide.createIcons();
        };
        reader.readAsDataURL(file);
    }

    // Drag & Drop
    if (dropzone) {
        ['dragenter', 'dragover'].forEach(name => {
            dropzone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(name => {
            dropzone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove('dragover');
            });
        });

        dropzone.addEventListener('drop', (e) => {
            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        dropzone.addEventListener('click', () => {
            fileInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files.length > 0) {
                handleFile(fileInput.files[0]);
            }
        });
    }

    if (removePreviewBtn) {
        removePreviewBtn.addEventListener('click', () => {
            currentFile = null;
            fileInput.value = '';
            previewImage.src = '';
            previewCard.style.display = 'none';
            dropzone.style.display = 'block';
            categoryResult.style.display = 'none';
            resultCard.style.display = 'none';
            showStatus('');
        });
    }

    // Camera Handling
    async function startCamera() {
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
                audio: false
            });
            cameraVideo.srcObject = cameraStream;
            cameraVideo.style.display = 'block';
            cameraPlaceholder.style.display = 'none';
            startCameraBtn.style.display = 'none';
            captureCameraBtn.style.display = 'inline-flex';
            showStatus('Camera active. Tap the shutter button to take a photo.');
            if (window.lucide) lucide.createIcons();
        } catch (err) {
            console.error('Camera error:', err);
            showStatus('Camera access denied or unavailable on this device. Please upload an image instead.', 'error');
        }
    }

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        if (cameraVideo) {
            cameraVideo.srcObject = null;
            cameraVideo.style.display = 'none';
        }
        if (cameraPlaceholder) cameraPlaceholder.style.display = 'block';
        if (startCameraBtn) startCameraBtn.style.display = 'inline-flex';
        if (captureCameraBtn) captureCameraBtn.style.display = 'none';
    }

    if (startCameraBtn) startCameraBtn.addEventListener('click', startCamera);

    if (captureCameraBtn) {
        captureCameraBtn.addEventListener('click', () => {
            if (!cameraVideo || !cameraVideo.videoWidth) {
                showStatus('Camera is not ready yet. Please wait a moment.', 'error');
                return;
            }
            cameraCanvas.width = cameraVideo.videoWidth;
            cameraCanvas.height = cameraVideo.videoHeight;
            const ctx = cameraCanvas.getContext('2d');
            ctx.drawImage(cameraVideo, 0, 0, cameraCanvas.width, cameraCanvas.height);
            cameraCanvas.toBlob((blob) => {
                if (blob) {
                    const capturedFile = new File([blob], `waste-camera-${Date.now()}.jpg`, { type: 'image/jpeg' });
                    stopCamera();
                    setTab('upload');
                    handleFile(capturedFile);
                }
            }, 'image/jpeg', 0.92);
        });
    }

    // Classification Request
    async function classifyImage() {
        if (!currentFile) {
            showStatus('Please choose or capture an image first.', 'error');
            return;
        }
        if (isClassifying) return;

        isClassifying = true;
        loadingState.style.display = 'block';
        categoryResult.style.display = 'none';
        resultCard.style.display = 'none';
        showStatus('');

        const formData = new FormData();
        formData.append('image', currentFile);

        try {
            const response = await fetch('/api/classify/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                body: formData
            });

            const contentType = response.headers.get('content-type') || '';
            let data;
            if (contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                if (response.status === 403) {
                    throw new Error('CSRF or permission verification failed. Please refresh the page.');
                } else if (response.status === 401) {
                    throw new Error('You must be logged in to classify images.');
                } else {
                    throw new Error(`Server returned status ${response.status}. Please check server logs.`);
                }
            }

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to classify the image.');
            }

            classifiedCategory = data.class;
            classifiedConfidence = parseFloat(data.confidence) || 0;

            displayCategorySelection(classifiedCategory, classifiedConfidence);
        } catch (error) {
            console.error('Classification error:', error);
            showStatus(error.message || 'Error occurred while analyzing image. Please try again.', 'error');
        } finally {
            isClassifying = false;
            loadingState.style.display = 'none';
        }
    }

    if (classifyBtn) classifyBtn.addEventListener('click', classifyImage);

    // Display Step 2: Category Result + Item Selection Grid
    function displayCategorySelection(category, confidence) {
        if (detectedCategoryEl) detectedCategoryEl.textContent = category;
        if (confidenceBadgeEl) {
            confidenceBadgeEl.textContent = `${confidence.toFixed(1)}% match`;
            confidenceBadgeEl.className = confidence >= 70 ? 'badge badge-safe' : 'badge badge-moderate';
        }

        const items = (window.categoryItems && window.categoryItems[category]) || [];
        const grid = itemSelectionGrid || document.getElementById('item-selection-grid');

        if (grid) {
            if (items.length > 0) {
                grid.innerHTML = items.map(item => `
                    <button type="button" class="item-btn" data-item-id="${item.id}" data-category="${category}">
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                            <div class="category-icon" style="width:36px;height:36px;">
                                <i data-lucide="${item.icon || 'package'}" style="width:18px;height:18px;"></i>
                            </div>
                            ${item.nigerian ? '<span class="badge badge-ng">NG</span>' : ''}
                        </div>
                        <p style="font-weight:600;color:#111827;font-size:14px;margin-bottom:2px;">${item.name}</p>
                        <p style="font-size:12px;color:#6B7280;line-height:1.4;">${item.description}</p>
                    </button>
                `).join('');

                grid.querySelectorAll('.item-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        grid.querySelectorAll('.item-btn').forEach(b => b.classList.remove('selected'));
                        btn.classList.add('selected');
                        const itemId = btn.dataset.itemId;
                        const cat = btn.dataset.category;
                        selectItem(itemId, cat);
                    });
                });
            } else {
                // Direct category fallback
                selectItem(null, category);
            }
        }

        categoryResult.style.display = 'block';
        if (window.lucide) lucide.createIcons();

        // If items exist, automatically trigger the first one or prompt user
        categoryResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Step 3: Item Selected -> Render Full Result Card
    function selectItem(itemId, category) {
        const itemInfo = (itemId && window.specificItemInfo && window.specificItemInfo[itemId])
            ? window.specificItemInfo[itemId]
            : (window.WASTE_KNOWLEDGE && window.WASTE_KNOWLEDGE[category])
                ? window.WASTE_KNOWLEDGE[category]
                : null;

        if (!itemInfo) return;

        populateResultCard(itemInfo, category, classifiedConfidence);

        // Send scan record to backend
        saveScanRecord({
            waste_class: category,
            confidence: classifiedConfidence,
            specific_item: itemId || '',
            specific_item_name: itemInfo.name || category
        });
    }

    function populateResultCard(info, category, confidence) {
        // Badges & Header
        const catBadge = document.getElementById('result-category-badge');
        if (catBadge) catBadge.textContent = category;

        const dangerBadge = document.getElementById('result-danger-badge');
        const dangerCard = document.getElementById('result-danger-card');
        const dangerText = document.getElementById('result-danger-text');

        const dangerLevel = info.danger_level || info.danger || 'Safe';
        const isHazardous = /hazardous|high/i.test(dangerLevel);
        const isModerate = /moderate/i.test(dangerLevel);

        if (dangerBadge) {
            dangerBadge.textContent = `${dangerLevel} Danger`;
            dangerBadge.className = isHazardous ? 'badge badge-hazardous' : isModerate ? 'badge badge-moderate' : 'badge badge-safe';
        }

        if (dangerCard) {
            dangerCard.className = `danger-card ${isHazardous ? 'danger-hazardous' : isModerate ? 'danger-moderate' : 'danger-safe'}`;
        }

        if (dangerText) {
            dangerText.textContent = `${dangerLevel} – ${info.danger_note || (isHazardous ? 'Exercise extreme caution.' : isModerate ? 'Follow sensible handling measures.' : 'Safe for domestic sorting.')}`;
        }

        const confEl = document.getElementById('result-confidence');
        if (confEl) confEl.textContent = confidence.toFixed(1);

        const nameEl = document.getElementById('result-name');
        if (nameEl) nameEl.textContent = info.name || category;

        const matEl = document.getElementById('result-material');
        if (matEl) matEl.textContent = info.material || info.about || '';

        const decompEl = document.getElementById('result-decomp');
        if (decompEl) decompEl.textContent = info.decomposition_time || info.decomposition || 'Varies';

        const matGridEl = document.getElementById('result-material-grid');
        if (matGridEl) matGridEl.textContent = info.category || category;

        const impactEl = document.getElementById('result-impact');
        if (impactEl) impactEl.textContent = info.environmental_impact || info.impact || '';

        const disposalEl = document.getElementById('result-disposal');
        if (disposalEl) {
            const steps = Array.isArray(info.disposal_steps)
                ? info.disposal_steps
                : (typeof info.disposal === 'string' ? info.disposal.split('. ').filter(s => s.trim()) : []);
            if (steps.length > 0) {
                disposalEl.innerHTML = steps.map(step => `<li>${step.replace(/^\d+\.\s*/, '')}</li>`).join('');
            } else {
                disposalEl.innerHTML = `<li>${info.disposal || 'Follow local municipal waste management guidelines.'}</li>`;
            }
        }

        const recyclingEl = document.getElementById('result-recycling');
        if (recyclingEl) recyclingEl.textContent = info.recycling_tips || info.recycling || 'No specific recycling guidance.';

        const reuseEl = document.getElementById('result-reuse');
        if (reuseEl) reuseEl.textContent = info.reuse_ideas || info.reuse || 'Consider repurposing before discarding.';

        // Fertilizer section
        const fertilizerSection = document.getElementById('result-fertilizer-section');
        const fertilizerEl = document.getElementById('result-fertilizer');
        const fertUse = info.fertilizer_use || info.agriculture;
        if (fertilizerSection && fertilizerEl) {
            if (fertUse && fertUse !== 'Not applicable.' && !fertUse.toLowerCase().includes('not suitable')) {
                fertilizerEl.textContent = fertUse;
                fertilizerSection.style.display = 'block';
            } else {
                fertilizerSection.style.display = 'none';
            }
        }

        // Fun fact
        const funFactEl = document.getElementById('result-funfact');
        if (funFactEl) funFactEl.textContent = info.fun_fact || info.fact || 'Sorting waste at source dramatically cuts drainage blockages across Nigeria.';

        resultCard.style.display = 'block';
        if (window.lucide) lucide.createIcons();
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Save scan to backend
    async function saveScanRecord(payload) {
        try {
            const res = await fetch('/api/save-scan/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.status === 'success') {
                console.log('Scan saved with ID:', data.scan_id);
            }
        } catch (e) {
            console.warn('Could not auto-save scan record:', e);
        }
    }

    // Reset scanner
    window.resetScanner = function () {
        currentFile = null;
        if (fileInput) fileInput.value = '';
        if (previewImage) previewImage.src = '';
        if (previewCard) previewCard.style.display = 'none';
        if (dropzone) dropzone.style.display = 'block';
        if (categoryResult) categoryResult.style.display = 'none';
        if (resultCard) resultCard.style.display = 'none';
        stopCamera();
        setTab('upload');
        showStatus('');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.addEventListener('beforeunload', stopCamera);
});
