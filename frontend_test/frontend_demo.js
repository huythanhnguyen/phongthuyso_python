// Cấu hình
const config = {
    apiUrl: localStorage.getItem('apiUrl') || 'http://localhost:8000',
    accessToken: () => localStorage.getItem('accessToken') || null
};

// Cập nhật URL API
function updateApiUrl() {
    const newUrl = document.getElementById('apiBaseUrl').value;
    if (newUrl) {
        localStorage.setItem('apiUrl', newUrl);
        config.apiUrl = newUrl;
        document.getElementById('configResponse').innerHTML = `<pre>API URL đã được cập nhật: ${newUrl}</pre>`;
    }
}

// Hàm helper để hiển thị kết quả
function displayResponse(containerId, response, error = false) {
    const container = document.getElementById(containerId);
    let content = '';
    
    if (error) {
        content = `<div class="alert alert-danger">${response}</div>`;
    } else {
        try {
            // Kiểm tra nếu response là string và có thể parse thành JSON
            if (typeof response === 'string' && response.trim().startsWith('{')) {
                const json = JSON.parse(response);
                content = `<pre>${JSON.stringify(json, null, 2)}</pre>`;
            } else if (typeof response === 'object') {
                content = `<pre>${JSON.stringify(response, null, 2)}</pre>`;
            } else {
                content = `<pre>${response}</pre>`;
            }
        } catch (e) {
            content = `<pre>${response}</pre>`;
        }
    }
    
    container.innerHTML = content;
}

// Hàm helper để gọi API
async function callApi(endpoint, method = 'GET', body = null, requiresAuth = false, formData = false) {
    try {
        const headers = {};
        
        if (!formData) {
            headers['Content-Type'] = 'application/json';
        }
        
        if (requiresAuth) {
            const token = config.accessToken();
            if (!token) {
                throw new Error('Bạn cần đăng nhập để thực hiện hành động này');
            }
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const options = {
            method,
            headers,
        };
        
        if (body) {
            if (formData) {
                options.body = body; // FormData đã được set
            } else {
                options.body = JSON.stringify(body);
            }
        }
        
        const response = await fetch(`${config.apiUrl}${endpoint}`, options);
        
        // Xử lý response
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            data = await response.text();
        }
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || 'Có lỗi xảy ra');
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

// Health Check
async function healthCheck() {
    try {
        const response = await callApi('/health');
        displayResponse('homeResponse', response);
    } catch (error) {
        displayResponse('homeResponse', error.message, true);
    }
}

// Lấy danh sách Agent
async function getAgents() {
    try {
        const response = await callApi('/agents');
        displayResponse('homeResponse', response);
    } catch (error) {
        displayResponse('homeResponse', error.message, true);
    }
}

// Phân tích số điện thoại
async function analyzeNumber() {
    try {
        const phoneNumber = document.getElementById('phoneNumber').value;
        const userDataStr = document.getElementById('userData').value;
        
        if (!phoneNumber) {
            throw new Error('Vui lòng nhập số điện thoại');
        }
        
        let userData = {};
        if (userDataStr) {
            try {
                userData = JSON.parse(userDataStr);
            } catch (e) {
                throw new Error('Dữ liệu người dùng không hợp lệ, cần phải là JSON');
            }
        }
        
        // Sử dụng query string để gửi yêu cầu đến endpoint GET /analyze_number
        let queryString = `?number=${encodeURIComponent(phoneNumber)}`;
        if (Object.keys(userData).length > 0) {
            queryString += `&user_data=${encodeURIComponent(JSON.stringify(userData))}`;
        }
        
        const response = await callApi(`/analyze_number${queryString}`, 'GET', null, config.accessToken() ? true : false);
        displayResponse('analyzeResponse', response);
    } catch (error) {
        displayResponse('analyzeResponse', error.message, true);
    }
}

// Phân tích số điện thoại với BatCucLinhSoAgent
async function analyzeBatCucLinhSo() {
    try {
        const phoneNumber = document.getElementById('phoneNumber').value;
        const userDataStr = document.getElementById('userData').value;
        
        if (!phoneNumber) {
            throw new Error('Vui lòng nhập số điện thoại');
        }
        
        let userData = {};
        if (userDataStr) {
            try {
                userData = JSON.parse(userDataStr);
            } catch (e) {
                throw new Error('Dữ liệu người dùng không hợp lệ, cần phải là JSON');
            }
        }
        
        const body = {
            phone_number: phoneNumber,
            request_type: "analysis",
            user_data: userData
        };
        
        const response = await callApi('/api/batcuclinh_so/analyze_phone', 'POST', body, config.accessToken() ? true : false);
        displayResponse('analyzeResponse', response);
    } catch (error) {
        displayResponse('analyzeResponse', error.message, true);
    }
}

// Lấy lịch sử phân tích số điện thoại
async function getPhoneAnalysisHistory() {
    try {
        if (!config.accessToken()) {
            throw new Error('Bạn cần đăng nhập để xem lịch sử');
        }
        
        const response = await callApi('/api/phone-analysis/history', 'GET', null, true);
        displayResponse('analyzeResponse', response);
    } catch (error) {
        displayResponse('analyzeResponse', error.message, true);
    }
}

// Lấy chi tiết phân tích số điện thoại
async function getPhoneAnalysisDetail() {
    try {
        const phoneNumber = document.getElementById('phoneDetailNumber').value;
        
        if (!phoneNumber) {
            throw new Error('Vui lòng nhập số điện thoại');
        }
        
        if (!config.accessToken()) {
            throw new Error('Bạn cần đăng nhập để xem chi tiết');
        }
        
        const response = await callApi(`/api/phone-analysis/${encodeURIComponent(phoneNumber)}`, 'GET', null, true);
        displayResponse('analyzeResponse', response);
    } catch (error) {
        displayResponse('analyzeResponse', error.message, true);
    }
}

// Chat
async function sendChat() {
    try {
        const message = document.getElementById('chatMessage').value;
        const contextStr = document.getElementById('chatContext').value;
        
        if (!message) {
            throw new Error('Vui lòng nhập tin nhắn');
        }
        
        let context = {};
        if (contextStr) {
            try {
                context = JSON.parse(contextStr);
            } catch (e) {
                throw new Error('Context không hợp lệ, cần phải là JSON');
            }
        }
        
        const body = {
            message,
            context
        };
        
        const response = await callApi('/api/chat', 'POST', body, config.accessToken() ? true : false);
        displayResponse('chatResponse', response);
    } catch (error) {
        displayResponse('chatResponse', error.message, true);
    }
}

// Lấy chat streaming
async function getChat() {
    try {
        const sessionId = document.getElementById('sessionId').value;
        const messageElement = document.getElementById('streamMessage');
        const message = messageElement ? messageElement.value : '';
        
        if (!sessionId) {
            throw new Error('Vui lòng nhập Session ID');
        }
        
        let queryString = `?session_id=${encodeURIComponent(sessionId)}`;
        if (message) {
            queryString += `&message=${encodeURIComponent(message)}`;
        }
        
        // Thông báo rằng đây là stream
        displayResponse('chatResponse', 'Đang nhận dữ liệu streaming...');
        
        // Sử dụng EventSource để nhận streaming response
        const eventSource = new EventSource(`${config.apiUrl}/api/chat${queryString}`);
        
        eventSource.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                displayResponse('chatResponse', data);
                
                // Nếu là response cuối cùng, đóng kết nối
                if (data.is_final) {
                    eventSource.close();
                }
            } catch (e) {
                displayResponse('chatResponse', `Lỗi khi xử lý dữ liệu: ${e.message}`, true);
                eventSource.close();
            }
        };
        
        eventSource.onerror = function(error) {
            displayResponse('chatResponse', `Lỗi kết nối stream: ${error.message || 'Unknown error'}`, true);
            eventSource.close();
        };
    } catch (error) {
        displayResponse('chatResponse', error.message, true);
    }
}

// Đăng ký
async function register() {
    try {
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const name = document.getElementById('registerFullName').value;
        const phoneElement = document.getElementById('registerPhone');
        const phoneNumber = phoneElement ? phoneElement.value : '';
        
        if (!email || !password || !name) {
            throw new Error('Vui lòng điền đủ thông tin');
        }
        
        const body = {
            name,
            email,
            password,
            phoneNumber
        };
        
        const response = await callApi('/api/user/register', 'POST', body);
        displayResponse('authResponse', response);
    } catch (error) {
        displayResponse('authResponse', error.message, true);
    }
}

// Đăng nhập
async function login() {
    try {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        if (!email || !password) {
            throw new Error('Vui lòng điền đủ thông tin');
        }
        
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await callApi('/api/user/token', 'POST', formData, false, true);
        
        if (response.access_token) {
            localStorage.setItem('accessToken', response.access_token);
            displayResponse('authResponse', { message: 'Đăng nhập thành công', ...response });
        } else {
            throw new Error('Đăng nhập thất bại');
        }
    } catch (error) {
        displayResponse('authResponse', error.message, true);
    }
}

// Đăng xuất
function logout() {
    localStorage.removeItem('accessToken');
    displayResponse('authResponse', 'Đã đăng xuất thành công');
}

// Lấy thông tin người dùng
async function getUserInfo() {
    try {
        const response = await callApi('/api/user/me', 'GET', null, true);
        displayResponse('userResponse', response);
    } catch (error) {
        displayResponse('userResponse', error.message, true);
    }
}

// Cập nhật thông tin người dùng
async function updateUser() {
    try {
        const fullname = document.getElementById('updateFullName').value;
        const emailElement = document.getElementById('updateEmail');
        const email = emailElement ? emailElement.value : '';
        const password = document.getElementById('updatePassword').value;
        
        if (!fullname && !password && !email) {
            throw new Error('Vui lòng nhập thông tin cần cập nhật');
        }
        
        const body = {};
        if (fullname) body.fullname = fullname;
        if (email) body.email = email;
        if (password) body.password = password;
        
        const response = await callApi('/api/user/me', 'PUT', body, true);
        displayResponse('userResponse', response);
    } catch (error) {
        displayResponse('userResponse', error.message, true);
    }
}

// Tạo API Key
async function createApiKey() {
    try {
        const name = document.getElementById('apiKeyName').value;
        
        if (!name) {
            throw new Error('Vui lòng nhập tên cho API Key');
        }
        
        const body = {
            name
        };
        
        const response = await callApi('/api/apikeys', 'POST', body, true);
        displayResponse('apikeyResponse', response);
    } catch (error) {
        displayResponse('apikeyResponse', error.message, true);
    }
}

// Lấy danh sách API Key
async function listApiKeys() {
    try {
        const response = await callApi('/api/apikeys', 'GET', null, true);
        displayResponse('apikeyResponse', response);
    } catch (error) {
        displayResponse('apikeyResponse', error.message, true);
    }
}

// Xóa API Key
async function deleteApiKey() {
    try {
        const keyId = document.getElementById('deleteApiKeyId').value;
        
        if (!keyId) {
            throw new Error('Vui lòng nhập API Key ID');
        }
        
        const response = await callApi(`/api/apikeys/${keyId}`, 'DELETE', null, true);
        displayResponse('apikeyResponse', response);
    } catch (error) {
        displayResponse('apikeyResponse', error.message, true);
    }
}

// Lấy danh sách các gói dịch vụ
async function listPlans() {
    try {
        const response = await callApi('/api/payment/plans', 'GET');
        displayResponse('paymentResponse', response);
    } catch (error) {
        displayResponse('paymentResponse', error.message, true);
    }
}

// Lấy thông tin gói dịch vụ
async function getPlan() {
    try {
        const planId = document.getElementById('planId').value;
        
        if (!planId) {
            throw new Error('Vui lòng nhập Plan ID');
        }
        
        const response = await callApi(`/api/payment/plans/${planId}`, 'GET');
        displayResponse('paymentResponse', response);
    } catch (error) {
        displayResponse('paymentResponse', error.message, true);
    }
}

// Tạo thanh toán
async function createPayment() {
    try {
        const planId = document.getElementById('paymentPlanId').value;
        const amount = document.getElementById('paymentAmount').value;
        const paymentMethod = document.getElementById('paymentMethod').value;
        
        if (!planId || !amount || !paymentMethod) {
            throw new Error('Vui lòng điền đủ thông tin thanh toán');
        }
        
        const body = {
            plan_id: planId,
            payment_method: paymentMethod,
            amount: parseFloat(amount),
            currency: "VND"
        };
        
        const response = await callApi('/api/payment', 'POST', body, true);
        
        // Kiểm tra nếu có URL thanh toán VNPay
        if (response.paymentUrl) {
            // Mở trang thanh toán trong cửa sổ mới
            window.open(response.paymentUrl, '_blank');
        }
        
        displayResponse('paymentResponse', response);
    } catch (error) {
        displayResponse('paymentResponse', error.message, true);
    }
}

// Lấy lịch sử thanh toán
async function getPaymentHistory() {
    try {
        const response = await callApi('/api/payment/history', 'GET', null, true);
        displayResponse('paymentResponse', response);
    } catch (error) {
        displayResponse('paymentResponse', error.message, true);
    }
}

// Lấy thông tin gói đăng ký
async function getSubscription() {
    try {
        const response = await callApi('/api/payment/subscription', 'GET', null, true);
        displayResponse('paymentResponse', response);
    } catch (error) {
        displayResponse('paymentResponse', error.message, true);
    }
}

// Upload file
async function uploadFile() {
    try {
        const fileInput = document.getElementById('uploadFile');
        const fileType = document.getElementById('fileType').value;
        const metadataStr = document.getElementById('fileMetadata').value;
        
        if (!fileInput.files || fileInput.files.length === 0) {
            throw new Error('Vui lòng chọn file');
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        if (fileType) {
            formData.append('type', fileType);
        }
        
        if (metadataStr) {
            try {
                JSON.parse(metadataStr); // Kiểm tra nếu là JSON hợp lệ
                formData.append('metadata', metadataStr);
            } catch (e) {
                throw new Error('Metadata không hợp lệ, cần phải là JSON');
            }
        }
        
        const response = await callApi('/api/upload', 'POST', formData, config.accessToken() ? true : false, true);
        displayResponse('uploadResponse', response);
    } catch (error) {
        displayResponse('uploadResponse', error.message, true);
    }
}

// Hiển thị cấu hình hiện tại khi tải trang
window.onload = function() {
    const apiUrl = config.apiUrl;
    document.getElementById('apiBaseUrl').value = apiUrl;
    document.getElementById('configResponse').innerHTML = `<pre>API URL hiện tại: ${apiUrl}</pre>`;
    
    // Kiểm tra nếu đã đăng nhập
    const token = config.accessToken();
    if (token) {
        const authStatusElement = document.getElementById('authStatus');
        if (authStatusElement) {
            authStatusElement.innerHTML = '<div class="alert alert-success">Đã đăng nhập</div>';
        }
    } else {
        const authStatusElement = document.getElementById('authStatus');
        if (authStatusElement) {
            authStatusElement.innerHTML = '<div class="alert alert-warning">Chưa đăng nhập</div>';
        }
    }
}; 