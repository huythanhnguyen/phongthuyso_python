// Cấu hình API 
let API_URL = localStorage.getItem('apiBaseUrl') || 'http://localhost:8000';
let accessToken = localStorage.getItem('accessToken') || '';

// Helper functions
function displayResponse(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    element.innerHTML = '';
    
    try {
        const formattedJson = JSON.stringify(data, null, 2);
        const pre = document.createElement('pre');
        
        if (isError) {
            pre.style.color = 'red';
        }
        
        pre.textContent = formattedJson;
        element.appendChild(pre);
    } catch (error) {
        element.textContent = typeof data === 'string' ? data : 'Lỗi hiển thị dữ liệu';
    }
}

// Khi trang web được tải, đặt giá trị API URL vào input
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('apiBaseUrl').value = API_URL;
    displayResponse('configResponse', { 
        current_api_url: API_URL,
        access_token_status: accessToken ? 'Đã có' : 'Chưa đăng nhập'
    });
});

// Hàm cập nhật API URL
function updateApiUrl() {
    const newApiUrl = document.getElementById('apiBaseUrl').value.trim();
    
    if (!newApiUrl) {
        displayResponse('configResponse', { error: 'Vui lòng nhập API URL' }, true);
        return;
    }
    
    // Kiểm tra URL có hợp lệ không
    try {
        new URL(newApiUrl);
    } catch (e) {
        displayResponse('configResponse', { error: 'URL không hợp lệ' }, true);
        return;
    }
    
    // Lưu URL mới
    API_URL = newApiUrl;
    localStorage.setItem('apiBaseUrl', API_URL);
    
    displayResponse('configResponse', { 
        message: 'API URL đã được cập nhật',
        current_api_url: API_URL
    });
}

async function fetchAPI(endpoint, options = {}) {
    try {
        // Thêm access token nếu có
        if (accessToken && !endpoint.includes('/api/user/token') && !endpoint.includes('/api/user/register')) {
            options.headers = options.headers || {};
            options.headers['Authorization'] = `Bearer ${accessToken}`;
        }
        
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw data;
        }
        
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        return { error: error.detail || error.message || 'Lỗi không xác định' };
    }
}

// API Functions

// Home Tab
async function healthCheck() {
    const response = await fetchAPI('/health');
    displayResponse('homeResponse', response);
}

async function getAgents() {
    const response = await fetchAPI('/agents');
    displayResponse('homeResponse', response);
}

// Analyze Tab
async function analyzeNumber() {
    const number = document.getElementById('phoneNumber').value;
    if (!number) {
        displayResponse('analyzeResponse', { error: 'Vui lòng nhập số điện thoại' }, true);
        return;
    }
    
    let endpoint = `/analyze_number?number=${encodeURIComponent(number)}`;
    
    const userData = document.getElementById('userData').value;
    if (userData) {
        try {
            JSON.parse(userData); // Kiểm tra JSON hợp lệ
            endpoint += `&user_data=${encodeURIComponent(userData)}`;
        } catch (e) {
            displayResponse('analyzeResponse', { error: 'Dữ liệu người dùng không phải là JSON hợp lệ' }, true);
            return;
        }
    }
    
    const response = await fetchAPI(endpoint);
    displayResponse('analyzeResponse', response);
}

// Chat Tab
async function sendChat() {
    const message = document.getElementById('chatMessage').value;
    if (!message) {
        displayResponse('chatResponse', { error: 'Vui lòng nhập tin nhắn' }, true);
        return;
    }
    
    let context = {};
    const contextValue = document.getElementById('chatContext').value;
    if (contextValue) {
        try {
            context = JSON.parse(contextValue);
        } catch (e) {
            displayResponse('chatResponse', { error: 'Context không phải là JSON hợp lệ' }, true);
            return;
        }
    }
    
    const requestBody = {
        message: message,
        context: context
    };
    
    const response = await fetchAPI('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    
    displayResponse('chatResponse', response);
    
    // Nếu có session_id, tự động điền vào ô input
    if (response.metadata && response.metadata.session_id) {
        document.getElementById('sessionId').value = response.metadata.session_id;
    }
}

let eventSource = null;

async function getChat() {
    const sessionId = document.getElementById('sessionId').value;
    if (!sessionId) {
        displayResponse('chatResponse', { error: 'Vui lòng nhập Session ID' }, true);
        return;
    }
    
    // Đóng kết nối EventSource cũ nếu có
    if (eventSource) {
        eventSource.close();
    }
    
    // Lưu trữ dữ liệu nhận được
    const chatResponseElement = document.getElementById('chatResponse');
    chatResponseElement.innerHTML = '<div>Đang kết nối...</div>';
    
    try {
        eventSource = new EventSource(`${API_URL}/api/chat?session_id=${encodeURIComponent(sessionId)}`);
        
        eventSource.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                displayResponse('chatResponse', data);
                
                if (data.is_final) {
                    eventSource.close();
                    eventSource = null;
                }
            } catch (error) {
                console.error('Error parsing event data:', error);
            }
        };
        
        eventSource.onerror = function(error) {
            console.error('EventSource error:', error);
            eventSource.close();
            eventSource = null;
            displayResponse('chatResponse', { error: 'Lỗi kết nối stream' }, true);
        };
    } catch (error) {
        console.error('Error setting up EventSource:', error);
        displayResponse('chatResponse', { error: 'Không thể thiết lập kết nối stream' }, true);
    }
}

// Auth Tab
async function register() {
    const email = document.getElementById('registerEmail').value;
    const fullname = document.getElementById('registerFullname').value;
    const password = document.getElementById('registerPassword').value;
    
    if (!email || !fullname || !password) {
        displayResponse('authResponse', { error: 'Vui lòng điền đầy đủ thông tin' }, true);
        return;
    }
    
    const requestBody = {
        email: email,
        fullname: fullname,
        password: password
    };
    
    const response = await fetchAPI('/api/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    
    displayResponse('authResponse', response);
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        displayResponse('authResponse', { error: 'Vui lòng điền đầy đủ thông tin' }, true);
        return;
    }
    
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetchAPI('/api/user/token', {
        method: 'POST',
        body: formData
    });
    
    if (response.access_token) {
        accessToken = response.access_token;
        localStorage.setItem('accessToken', accessToken);
    }
    
    displayResponse('authResponse', response);
}

// User Tab
async function getUserInfo() {
    if (!accessToken) {
        displayResponse('userResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const response = await fetchAPI('/api/user/me');
    displayResponse('userResponse', response);
}

async function updateUser() {
    if (!accessToken) {
        displayResponse('userResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const email = document.getElementById('updateEmail').value;
    const fullname = document.getElementById('updateFullname').value;
    const password = document.getElementById('updatePassword').value;
    
    const requestBody = {};
    if (email) requestBody.email = email;
    if (fullname) requestBody.fullname = fullname;
    if (password) requestBody.password = password;
    
    if (Object.keys(requestBody).length === 0) {
        displayResponse('userResponse', { error: 'Vui lòng nhập ít nhất một thông tin để cập nhật' }, true);
        return;
    }
    
    const response = await fetchAPI('/api/user/me', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    
    displayResponse('userResponse', response);
}

// API Key Tab
async function createApiKey() {
    if (!accessToken) {
        displayResponse('apikeyResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const name = document.getElementById('apikeyName').value;
    if (!name) {
        displayResponse('apikeyResponse', { error: 'Vui lòng nhập tên API Key' }, true);
        return;
    }
    
    const requestBody = {
        name: name
    };
    
    const response = await fetchAPI('/api/apikeys', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    
    displayResponse('apikeyResponse', response);
}

async function listApiKeys() {
    if (!accessToken) {
        displayResponse('apikeyResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const response = await fetchAPI('/api/apikeys');
    displayResponse('apikeyResponse', response);
}

async function deleteApiKey() {
    if (!accessToken) {
        displayResponse('apikeyResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const apiKeyId = document.getElementById('deleteApiKeyId').value;
    if (!apiKeyId) {
        displayResponse('apikeyResponse', { error: 'Vui lòng nhập ID API Key' }, true);
        return;
    }
    
    const response = await fetchAPI(`/api/apikeys/${encodeURIComponent(apiKeyId)}`, {
        method: 'DELETE'
    });
    
    displayResponse('apikeyResponse', response);
}

// Payment Tab
async function listPlans() {
    const response = await fetchAPI('/api/payment/plans');
    displayResponse('paymentResponse', response);
}

async function getPlan() {
    const planId = document.getElementById('planId').value;
    if (!planId) {
        displayResponse('paymentResponse', { error: 'Vui lòng nhập ID gói dịch vụ' }, true);
        return;
    }
    
    const response = await fetchAPI(`/api/payment/plans/${encodeURIComponent(planId)}`);
    displayResponse('paymentResponse', response);
}

async function createPayment() {
    if (!accessToken) {
        displayResponse('paymentResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const planId = document.getElementById('paymentPlanId').value;
    const paymentMethod = document.getElementById('paymentMethod').value;
    const amount = document.getElementById('paymentAmount').value;
    
    if (!planId || !paymentMethod || !amount) {
        displayResponse('paymentResponse', { error: 'Vui lòng điền đầy đủ thông tin' }, true);
        return;
    }
    
    const requestBody = {
        plan_id: planId,
        payment_method: paymentMethod,
        amount: parseFloat(amount),
        currency: 'VND'
    };
    
    const response = await fetchAPI('/api/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    
    displayResponse('paymentResponse', response);
}

async function getPaymentHistory() {
    if (!accessToken) {
        displayResponse('paymentResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const response = await fetchAPI('/api/payment/history');
    displayResponse('paymentResponse', response);
}

async function getSubscription() {
    if (!accessToken) {
        displayResponse('paymentResponse', { error: 'Vui lòng đăng nhập trước' }, true);
        return;
    }
    
    const response = await fetchAPI('/api/payment/subscription');
    displayResponse('paymentResponse', response);
}

// Upload Tab
async function uploadFile() {
    const fileInput = document.getElementById('uploadFile');
    const file = fileInput.files[0];
    
    if (!file) {
        displayResponse('uploadResponse', { error: 'Vui lòng chọn file để upload' }, true);
        return;
    }
    
    const fileType = document.getElementById('fileType').value;
    let metadata = document.getElementById('fileMetadata').value;
    
    if (metadata) {
        try {
            JSON.parse(metadata); // Kiểm tra JSON hợp lệ
        } catch (e) {
            displayResponse('uploadResponse', { error: 'Metadata không phải là JSON hợp lệ' }, true);
            return;
        }
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', fileType);
    if (metadata) {
        formData.append('metadata', metadata);
    }
    
    const response = await fetchAPI('/api/upload', {
        method: 'POST',
        body: formData
    });
    
    displayResponse('uploadResponse', response);
} 