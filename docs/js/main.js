// Othello CV Demo - Interactive JavaScript
// ==========================================

// Tab Switching
function switchTab(tabName) {
    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });

    // Remove active state from all buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('text-gamescrafters-blue', 'border-gamescrafters-blue');
        button.classList.add('text-gray-600', 'border-transparent');
    });

    // Show selected tab content
    document.getElementById(`demo-${tabName}`).classList.remove('hidden');

    // Add active state to selected button
    const activeButton = document.getElementById(`tab-${tabName}`);
    activeButton.classList.remove('text-gray-600', 'border-transparent');
    activeButton.classList.add('text-gamescrafters-blue', 'border-gamescrafters-blue');

    // If switching to video tab, ensure video is loaded
    if (tabName === 'video') {
        const video = document.getElementById('demo-video-player');
        if (video) {
            video.load(); // Reload the video to ensure it's ready
        }
    }
}

// Sample Data - Real test results from Othello CV processing
const sampleData = {
    '4x4-early': {
        boardSize: 4,
        state: '-----BW-BWB-W---',
        grid: [
            ['-', '-', '-', '-'],
            ['-', '-', 'B', 'W'],
            ['-', 'B', 'W', 'B'],
            ['-', 'W', '-', '-']
        ],
        processingTime: 0.03,
        pieceCount: { black: 3, white: 3, empty: 10 },
        description: '4x4 GamesmanUni - Early Game'
    },
    '8x8-opening': {
        boardSize: 8,
        state: '---------------------------WB------BW---------------------------',
        grid: [
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'W', 'B', '-', '-', '-'],
            ['-', '-', '-', 'B', 'W', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-']
        ],
        processingTime: 0.05,
        pieceCount: { black: 2, white: 2, empty: 60 },
        description: '8x8 Standard - Opening Position'
    },
    '4x4-complex': {
        boardSize: 4,
        state: 'W-WBWWB-WWBBWBW-',
        grid: [
            ['W', '-', 'W', 'B'],
            ['W', 'W', 'B', '-'],
            ['W', 'W', 'B', 'B'],
            ['W', 'B', 'W', '-']
        ],
        processingTime: 0.04,
        pieceCount: { black: 5, white: 9, empty: 2 },
        description: '4x4 GamesmanUni - Late Game'
    }
};

// Load Sample
function loadSample(sampleId) {
    const data = sampleData[sampleId];
    if (!data) return;

    // Highlight selected sample
    document.querySelectorAll('.sample-btn').forEach(btn => {
        btn.classList.remove('border-gamescrafters-blue', 'bg-blue-50');
        btn.classList.add('border-gray-300');
    });
    event.target.closest('.sample-btn').classList.add('border-gamescrafters-blue', 'bg-blue-50');
    event.target.closest('.sample-btn').classList.remove('border-gray-300');

    // Display results
    displayResults(data);
}

// Display Results
function displayResults(data) {
    const resultsDiv = document.getElementById('results-display');

    const html = `
        <div class="space-y-4">
            <!-- Processing Info -->
            <div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                <div class="flex items-center">
                    <i class="fas fa-check-circle text-green-500 text-2xl mr-3"></i>
                    <div>
                        <div class="font-semibold text-gray-900">Processing Complete</div>
                        <div class="text-sm text-gray-600">${data.processingTime}s processing time</div>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-2xl font-bold text-gray-900">${data.boardSize}x${data.boardSize}</div>
                    <div class="text-xs text-gray-600">Board Size</div>
                </div>
            </div>

            <!-- Board State -->
            <div class="p-4 bg-gray-900 rounded-lg">
                <div class="text-xs text-gray-400 uppercase tracking-wide mb-2">Board State String</div>
                <div class="font-mono text-sm text-green-400 break-all">${data.state}</div>
            </div>

            <!-- Piece Count -->
            <div class="grid grid-cols-3 gap-3">
                <div class="p-4 bg-gray-900 text-white rounded-lg text-center">
                    <div class="text-2xl font-bold">${data.pieceCount.black}</div>
                    <div class="text-xs text-gray-400">Black</div>
                </div>
                <div class="p-4 bg-gray-100 text-gray-900 rounded-lg text-center">
                    <div class="text-2xl font-bold">${data.pieceCount.white}</div>
                    <div class="text-xs text-gray-600">White</div>
                </div>
                <div class="p-4 bg-blue-50 text-blue-900 rounded-lg text-center">
                    <div class="text-2xl font-bold">${data.pieceCount.empty}</div>
                    <div class="text-xs text-blue-600">Empty</div>
                </div>
            </div>

            ${data.grid ? `
            <!-- Visual Board -->
            <div class="p-4 bg-white border-2 border-gray-200 rounded-lg">
                <div class="text-xs text-gray-600 uppercase tracking-wide mb-3">Visual Board</div>
                <div class="grid grid-cols-${data.boardSize} gap-1 max-w-xs mx-auto">
                    ${data.grid.map(row => row.map(cell => `
                        <div class="aspect-square ${
                            cell === 'B' ? 'bg-gray-900' :
                            cell === 'W' ? 'bg-gray-100 border border-gray-300' :
                            'bg-green-600'
                        } rounded flex items-center justify-center text-xs font-bold ${
                            cell === 'B' ? 'text-white' :
                            cell === 'W' ? 'text-gray-900' :
                            'text-green-800'
                        }">${cell === '-' ? '' : cell}</div>
                    `).join('')).join('')}
                </div>
            </div>
            ` : ''}

            <!-- JSON Output -->
            <div class="p-4 bg-gray-900 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                    <div class="text-xs text-gray-400 uppercase tracking-wide">JSON Output</div>
                    <button onclick="copyJSON(this)" class="text-xs text-gray-400 hover:text-white transition">
                        <i class="fas fa-copy mr-1"></i> Copy
                    </button>
                </div>
                <pre class="font-mono text-xs text-green-400 overflow-x-auto max-h-48">${JSON.stringify({
                    board_size: data.boardSize,
                    state: data.state,
                    processing_time: data.processingTime,
                    piece_count: data.pieceCount
                }, null, 2)}</pre>
            </div>
        </div>
    `;

    resultsDiv.innerHTML = html;
}

// Copy JSON
function copyJSON(button) {
    const jsonText = button.closest('.p-4').querySelector('pre').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check mr-1"></i> Copied!';
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    });
}

// Gallery Filter
function filterGallery(category) {
    const items = document.querySelectorAll('.gallery-item');
    const buttons = document.querySelectorAll('.gallery-filter');

    // Update active button
    buttons.forEach(btn => {
        btn.classList.remove('bg-gamescrafters-blue', 'text-white');
        btn.classList.add('bg-gray-200', 'text-gray-700');
    });
    event.target.classList.remove('bg-gray-200', 'text-gray-700');
    event.target.classList.add('bg-gamescrafters-blue', 'text-white');

    // Filter items
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Copy Code Example
function copyCode() {
    const code = document.getElementById('code-example').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Code copied to clipboard!');
    });
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('nav');
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.classList.add('shadow-lg');
    } else {
        navbar.classList.remove('shadow-lg');
    }

    lastScroll = currentScroll;
});

// Live Upload Functionality
const API_URL = 'http://localhost:5000/api';
let backendAvailable = false;

// Check backend health on load
async function checkBackend() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            backendAvailable = true;
            const statusEl = document.getElementById('backend-status');
            if (statusEl) {
                statusEl.className = 'mt-6 p-4 bg-green-50 border border-green-200 rounded-lg';
                statusEl.innerHTML = `
                    <div class="flex items-start space-x-2">
                        <i class="fas fa-check-circle text-green-600 mt-0.5"></i>
                        <div class="text-sm">
                            <p class="font-semibold text-green-900">Backend Connected</p>
                            <p class="text-green-700 mt-1">Ready to process your uploads!</p>
                        </div>
                    </div>
                `;
            }
        }
    } catch (error) {
        backendAvailable = false;
    }
}

// Handle file upload
async function handleLiveUpload(file) {
    if (!backendAvailable) {
        alert('Backend server is not running. Please start the server first.');
        return;
    }

    const boardSize = document.getElementById('live-board-size').value;
    const annotate = document.getElementById('live-annotate').checked;

    // Show progress
    document.getElementById('live-progress').classList.remove('hidden');
    document.getElementById('live-results').innerHTML = `
        <div class="text-center text-gray-400 py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gamescrafters-blue mx-auto mb-4"></div>
            <p>Processing ${file.name}...</p>
        </div>
    `;

    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    formData.append('board_size', boardSize);
    formData.append('annotate', annotate);

    try {
        const response = await fetch(`${API_URL}/process`, {
            method: 'POST',
            body: formData
        });

        document.getElementById('live-progress').classList.add('hidden');

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Processing failed');
        }

        const result = await response.json();
        displayLiveResults(result);

    } catch (error) {
        document.getElementById('live-progress').classList.add('hidden');
        document.getElementById('live-results').innerHTML = `
            <div class="bg-red-50 border-2 border-red-200 rounded-lg p-6">
                <div class="flex items-start space-x-3">
                    <i class="fas fa-exclamation-triangle text-red-500 text-2xl"></i>
                    <div>
                        <div class="font-semibold text-red-900 mb-2">Processing Error</div>
                        <div class="text-sm text-red-700">${error.message}</div>
                    </div>
                </div>
            </div>
        `;
    }
}

// Display live upload results
function displayLiveResults(data) {
    let html = '';

    if (data.type === 'image') {
        html = `
            <div class="space-y-4">
                <!-- Success Header -->
                <div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div class="flex items-center">
                        <i class="fas fa-check-circle text-green-500 text-2xl mr-3"></i>
                        <div>
                            <div class="font-semibold text-gray-900">Processing Complete</div>
                            <div class="text-sm text-gray-600">${data.processing_time.toFixed(3)}s processing time</div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-2xl font-bold text-gray-900">${data.board_size}x${data.board_size}</div>
                        <div class="text-xs text-gray-600">Board Size</div>
                    </div>
                </div>

                <!-- Board State -->
                <div class="p-4 bg-gray-900 rounded-lg">
                    <div class="text-xs text-gray-400 uppercase tracking-wide mb-2">Board State String</div>
                    <div class="font-mono text-sm text-green-400 break-all">${data.state}</div>
                </div>

                <!-- Piece Count -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="p-4 bg-gray-900 text-white rounded-lg text-center">
                        <div class="text-2xl font-bold">${data.piece_count.black}</div>
                        <div class="text-xs text-gray-400">Black</div>
                    </div>
                    <div class="p-4 bg-gray-100 text-gray-900 rounded-lg text-center">
                        <div class="text-2xl font-bold">${data.piece_count.white}</div>
                        <div class="text-xs text-gray-600">White</div>
                    </div>
                    <div class="p-4 bg-blue-50 text-blue-900 rounded-lg text-center">
                        <div class="text-2xl font-bold">${data.piece_count.empty}</div>
                        <div class="text-xs text-blue-600">Empty</div>
                    </div>
                </div>

                <!-- JSON Output -->
                <div class="p-4 bg-gray-900 rounded-lg">
                    <div class="flex items-center justify-between mb-2">
                        <div class="text-xs text-gray-400 uppercase tracking-wide">JSON Output</div>
                        <button onclick="copyLiveJSON(this)" class="text-xs text-gray-400 hover:text-white transition">
                            <i class="fas fa-copy mr-1"></i> Copy
                        </button>
                    </div>
                    <pre class="font-mono text-xs text-green-400 overflow-x-auto max-h-48">${JSON.stringify(data, null, 2)}</pre>
                </div>
            </div>
        `;
    } else if (data.type === 'video') {
        html = `
            <div class="space-y-4">
                <!-- Success Header -->
                <div class="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div class="flex items-center">
                        <i class="fas fa-check-circle text-green-500 text-2xl mr-3"></i>
                        <div>
                            <div class="font-semibold text-gray-900">Video Processed</div>
                            <div class="text-sm text-gray-600">${data.total_moves} moves detected</div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-2xl font-bold text-gray-900">${data.processing_time.toFixed(1)}s</div>
                        <div class="text-xs text-gray-600">Total Time</div>
                    </div>
                </div>

                <!-- Moves List -->
                <div class="p-4 bg-gray-50 rounded-lg max-h-96 overflow-y-auto">
                    <div class="text-xs text-gray-600 uppercase tracking-wide mb-3">Detected Moves</div>
                    <div class="space-y-2 font-mono text-sm">
                        ${data.moves.slice(0, 10).map((move, i) => `
                            <div class="flex items-start space-x-3">
                                <span class="bg-${move.player === 1 ? 'blue' : 'red'}-500 text-white rounded px-2 py-1 text-xs">P${move.player}</span>
                                <span class="text-gray-700">${move.state}</span>
                            </div>
                        `).join('')}
                        ${data.moves.length > 10 ? `<div class="text-xs text-gray-500 mt-3">...and ${data.moves.length - 10} more moves</div>` : ''}
                    </div>
                </div>

                <!-- JSON Output -->
                <div class="p-4 bg-gray-900 rounded-lg">
                    <div class="flex items-center justify-between mb-2">
                        <div class="text-xs text-gray-400 uppercase tracking-wide">JSON Output</div>
                        <button onclick="copyLiveJSON(this)" class="text-xs text-gray-400 hover:text-white transition">
                            <i class="fas fa-copy mr-1"></i> Copy
                        </button>
                    </div>
                    <pre class="font-mono text-xs text-green-400 overflow-x-auto max-h-48">${JSON.stringify(data, null, 2)}</pre>
                </div>
            </div>
        `;
    }

    document.getElementById('live-results').innerHTML = html;
}

// Copy JSON from live results
function copyLiveJSON(button) {
    const jsonText = button.closest('.p-4').querySelector('pre').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check mr-1"></i> Copied!';
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Othello CV Demo | GamesCrafters at UC Berkeley');
    console.log('GitHub: https://github.com/mananb77/gamescrafters-othello-cv');

    // Check backend status
    checkBackend();

    // Setup file upload handlers
    const uploadArea = document.getElementById('live-upload-area');
    const fileInput = document.getElementById('live-file-input');

    if (uploadArea && fileInput) {
        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // File selected
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                handleLiveUpload(file);
            }
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('bg-blue-50');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('bg-blue-50');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('bg-blue-50');
            const file = e.dataTransfer.files[0];
            if (file) {
                handleLiveUpload(file);
            }
        });
    }
});
