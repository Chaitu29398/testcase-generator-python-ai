let selectedProduct = 'PAM';
let uploadedFile = null;

// Product selection
document.querySelectorAll('.product-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.product-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedProduct = btn.dataset.product;
  });
});

// File upload
const fileInput   = document.getElementById('fileInput');
const uploadZone  = document.getElementById('uploadZone');
const fileInfo    = document.getElementById('fileInfo');
const fileNameEl  = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadedFile = file;
  fileNameEl.textContent = '📎 ' + file.name;
  fileInfo.classList.remove('hidden');
});

removeFileBtn.addEventListener('click', () => {
  uploadedFile = null;
  fileInput.value = '';
  fileInfo.classList.add('hidden');
});

// Drag and drop
uploadZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
  uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) {
    uploadedFile = file;
    fileNameEl.textContent = '📎 ' + file.name;
    fileInfo.classList.remove('hidden');
  }
});

// Generate
document.getElementById('generateBtn').addEventListener('click', async () => {
  const feature = document.getElementById('featureInput').value.trim();

  if (!feature) {
    alert('Please describe the feature or module in Step 3');
    return;
  }

  const formData = new FormData();
  formData.append('product',    selectedProduct);
  formData.append('feature',    feature);
  formData.append('test_type',  document.getElementById('testType').value);
  formData.append('count',      document.getElementById('tcCount').value);
  formData.append('priority',   document.getElementById('priority').value);

  if (uploadedFile) {
    formData.append('file', uploadedFile);
  }

  // UI state
  const generateBtn = document.getElementById('generateBtn');
  const statusBar   = document.getElementById('statusBar');
  const statusText  = document.getElementById('statusText');
  const errorBar    = document.getElementById('errorBar');
  const resultCard  = document.getElementById('resultCard');

  generateBtn.disabled = true;
  statusBar.classList.remove('hidden');
  errorBar.classList.add('hidden');
  resultCard.classList.add('hidden');
  statusText.textContent = uploadedFile
    ? 'Reading document and generating test cases...'
    : 'Generating test cases with AI...';

  try {
    const res  = await fetch('/generate', { method: 'POST', body: formData });
    const data = await res.json();

    if (!data.success) throw new Error(data.error);

    // Update result card
    document.getElementById('resultTitle').textContent =
      `${data.count} Test Cases — ${selectedProduct}`;
    document.getElementById('resultMeta').textContent =
      `Generated on ${new Date().toLocaleDateString('en-IN', {day:'numeric', month:'short', year:'numeric'})}`;

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.href = data.download_url;
    downloadBtn.setAttribute('download', '');

    // Render preview
    renderPreview(data.preview, data.count);

    resultCard.classList.remove('hidden');
    statusBar.classList.add('hidden');

  } catch (err) {
    statusBar.classList.add('hidden');
    document.getElementById('errorText').textContent = err.message;
    errorBar.classList.remove('hidden');
  }

  generateBtn.disabled = false;
});

function renderPreview(cases, total) {
  const tbody = document.getElementById('previewBody');

  tbody.innerHTML = cases.map(tc => `
    <tr>
      <td class="tc-id">${tc.tc_id || ''}</td>
      <td>${tc.objective || ''}</td>
      <td style="font-size:11px;">${(tc.steps || '').slice(0, 120)}${tc.steps && tc.steps.length > 120 ? '...' : ''}</td>
      <td style="font-size:11px;">${(tc.expected_result || '').slice(0, 100)}${tc.expected_result && tc.expected_result.length > 100 ? '...' : ''}</td>
      <td><span class="type-badge type-${(tc.type || 'functional').toLowerCase()}">${tc.type || ''}</span></td>
      <td><span class="type-badge prio-${(tc.priority || 'medium').toLowerCase()}">${tc.priority || ''}</span></td>
    </tr>
  `).join('');

  document.getElementById('previewNote').textContent =
    `Showing 3 of ${total} test cases — download Excel to see all`;
}