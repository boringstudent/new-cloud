import os
import json
import hashlib
import markdown
import shutil

GITHUB_APIKEY = os.environ.get('APIKEY', '')
ADMIN_CREDENTIALS = os.environ.get('ADMIN', '')
ADMIN_USER = ''
ADMIN_PASS = ''
if ':' in ADMIN_CREDENTIALS:
    ADMIN_USER, ADMIN_PASS = ADMIN_CREDENTIALS.split(':', 1)

REPO_NAME = os.environ.get('REPO_NAME', '')

GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY', '')
REPO_OWNER = ''
if '/' in GITHUB_REPOSITORY:
    REPO_OWNER = GITHUB_REPOSITORY.split('/')[0]

template = """
<html>
    <head>
        <meta charset="utf-8">
        <title>FULLPATH - boring_student </title>
        <link rel="icon" href="./favicon.ico" type="image/x-icon">
        <link rel="shortcut icon" href="./favicon.ico" type="image/x-icon">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                min-height: 100vh;
                background-size: cover;
                background-position: center;
            }
            body {
                background: url('https://www.loliapi.com/acg') fixed;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 20px auto;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
            }
            .entry {
                text-decoration: none !important;
                color: #333 !important;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                margin: 8px 0;
                background: rgba(245, 245, 245, 0.9);
                border-radius: 8px;
                transition: all 0.3s;
            }
            .entry:hover {
                transform: translateX(10px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                background: rgba(235, 245, 255, 0.9);
            }
            .file-info {
                display: flex;
                gap: 15px;
                color: #666;
                font-size: 0.9em;
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }
            a {
                color: #2c82c9;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .upload-btn {
                display: inline-block;
                padding: 10px 20px;
                background: #2c82c9;
                color: white;
                border-radius: 8px;
                text-decoration: none;
                margin: 10px 0;
                transition: background 0.3s;
            }
            .upload-btn:hover {
                background: #1a5a8a;
            }
            .modal-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal-overlay.show {
                display: flex;
            }
            .modal-content {
                max-width: 600px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
                position: relative;
            }
            .modal-close {
                position: absolute;
                top: 15px;
                right: 15px;
                font-size: 24px;
                cursor: pointer;
                color: #666;
                text-decoration: none;
            }
            .modal-close:hover {
                color: #333;
            }
            .form-group {
                margin: 20px 0;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: bold;
            }
            input[type="text"], input[type="password"], textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                box-sizing: border-box;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus, input[type="password"]:focus, textarea:focus {
                border-color: #2c82c9;
                outline: none;
            }
            input[type="file"] {
                width: 100%;
                padding: 10px;
                border: 2px dashed #ddd;
                border-radius: 8px;
                background: rgba(245, 245, 245, 0.9);
                cursor: pointer;
                transition: all 0.3s;
            }
            input[type="file"]:hover {
                border-color: #2c82c9;
                background: rgba(235, 245, 255, 0.9);
            }
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background: #2c82c9;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
                text-decoration: none;
            }
            .btn:hover {
                background: #1a5a8a;
            }
            .btn-secondary {
                background: #666;
                margin-left: 10px;
            }
            .btn-secondary:hover {
                background: #444;
            }
            .btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .progress-bar {
                width: 100%;
                height: 20px;
                background: #eee;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
                display: none;
            }
            .progress-fill {
                height: 100%;
                background: #2c82c9;
                width: 0%;
                transition: width 0.1s linear;
            }
            .progress-text {
                text-align: center;
                color: #666;
                font-size: 14px;
                margin-top: 5px;
            }
            .message {
                padding: 12px;
                border-radius: 8px;
                margin: 10px 0;
                display: none;
            }
            .message.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .message.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .upload-type {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            .upload-type label {
                flex: 1;
                text-align: center;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 0;
                font-weight: normal;
            }
            .upload-type input[type="radio"]:checked + label {
                border-color: #2c82c9;
                background: rgba(235, 245, 255, 0.9);
                color: #2c82c9;
                font-weight: bold;
            }
            .upload-type input[type="radio"] {
                display: none;
            }
            .login-section {
                background: rgba(245, 245, 245, 0.9);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .login-section h3 {
                margin-top: 0;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FULLPATH</h1>
            INFOCONTENT
            <div style="margin: 20px 0;">
                <a href="../" style="font-size: 1.1em;">上级目录</a>
                <button class="upload-btn" id="open-upload-btn" style="margin-left: 20px; border: none;">上传文件</button>
            </div>
            FILECONTENT
            <hr>
            <a style="text-decoration: none; color: #34495e; font-size: 15px; font-weight: 400;" href="https://beian.miit.gov.cn/#/Integrated/recordQuery" target="_blank">闽ICP备2025107306号-1</a>
        </div>

        <div class="modal-overlay" id="upload-modal">
            <div class="modal-content">
                <a href="#" class="modal-close" id="modal-close">&times;</a>
                <h1>文件上传</h1>
                
                <div class="login-section" id="login-section">
                    <h3>管理员登录</h3>
                    <div class="form-group">
                        <label for="admin-user">用户名</label>
                        <input type="text" id="admin-user" placeholder="输入管理员用户名">
                    </div>
                    <div class="form-group">
                        <label for="admin-pass">密码</label>
                        <div style="position: relative;">
                            <input type="password" id="admin-pass" placeholder="输入管理员密码">
                            <button type="button" id="toggle-pass" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #666;">显示</button>
                        </div>
                    </div>
                    <button class="btn" id="login-btn">登录</button>
                    <div class="message" id="login-error"></div>
                </div>

                <div id="upload-form" style="display: none;">
                    <div class="form-group">
                        <label for="file-input">选择文件</label>
                        <input type="file" id="file-input" accept="*">
                        <div id="file-name" style="margin-top: 8px; color: #666;"></div>
                    </div>

                    <div class="form-group">
                        <label for="target-path">目标路径</label>
                        <input type="text" id="target-path" placeholder="例如: docs/myfile.txt">
                    </div>

                    <div class="form-group">
                        <label for="commit-msg">提交信息</label>
                        <input type="text" id="commit-msg" placeholder="上传文件" value="上传文件 via upload">
                    </div>

                    <div class="progress-bar" id="progress-bar">
                        <div class="progress-fill" id="progress-fill"></div>
                    </div>
                    <div class="progress-text" id="progress-text"></div>

                    <div class="message" id="success-message">上传成功！页面将自动刷新...</div>
                    <div class="message" id="error-message"></div>

                    <button class="btn" id="upload-btn">开始上传</button>
                    <button class="btn btn-secondary" id="cancel-btn">取消</button>
                </div>
            </div>
        </div>

        <script>
            const ADMIN_USER = '__ADMIN_USER__';
            const ADMIN_PASS = '__ADMIN_PASS__';
            const GITHUB_APIKEY = '__GITHUB_APIKEY__';
            const REPO_OWNER = '__REPO_OWNER__';
            const REPO_NAME = '__REPO_NAME__';

            console.log('=== 系统配置信息 ===');
            console.log('ADMIN_USER:', ADMIN_USER || '未配置');
            console.log('ADMIN_PASS:', ADMIN_PASS ? '已配置' : '未配置');
            console.log('GITHUB_APIKEY:', GITHUB_APIKEY ? '已配置 (' + GITHUB_APIKEY.substring(0, 8) + '...)' : '未配置');
            console.log('REPO_OWNER:', REPO_OWNER || '未配置');
            console.log('REPO_NAME:', REPO_NAME || '未配置');
            console.log('=== 配置检查 ===');
            console.log('配置完整:', !!(ADMIN_USER && ADMIN_PASS && GITHUB_APIKEY && REPO_OWNER && REPO_NAME));

            const modalOverlay = document.getElementById('upload-modal');
            const openUploadBtn = document.getElementById('open-upload-btn');
            const modalClose = document.getElementById('modal-close');

            const loginSection = document.getElementById('login-section');
            const uploadForm = document.getElementById('upload-form');
            const adminUser = document.getElementById('admin-user');
            const adminPass = document.getElementById('admin-pass');
            const togglePass = document.getElementById('toggle-pass');
            const loginBtn = document.getElementById('login-btn');
            const loginError = document.getElementById('login-error');

            const fileInput = document.getElementById('file-input');
            const fileName = document.getElementById('file-name');
            const targetPath = document.getElementById('target-path');
            const commitMsg = document.getElementById('commit-msg');
            const uploadBtn = document.getElementById('upload-btn');
            const cancelBtn = document.getElementById('cancel-btn');
            const progressBar = document.getElementById('progress-bar');
            const progressFill = document.getElementById('progress-fill');
            const progressText = document.getElementById('progress-text');
            const successMessage = document.getElementById('success-message');
            const errorMessage = document.getElementById('error-message');

            function openModal() {
                modalOverlay.classList.add('show');
                document.body.style.overflow = 'hidden';
            }

            function closeModal() {
                modalOverlay.classList.remove('show');
                document.body.style.overflow = '';
                loginSection.style.display = 'block';
                uploadForm.style.display = 'none';
                adminUser.value = '';
                adminPass.value = '';
                hideLoginError();
                resetForm();
            }

            openUploadBtn.addEventListener('click', openModal);
            modalClose.addEventListener('click', function(e) {
                e.preventDefault();
                closeModal();
            });
            modalOverlay.addEventListener('click', function(e) {
                if (e.target === modalOverlay) {
                    closeModal();
                }
            });

            function showLoginError(msg) {
                loginError.textContent = msg;
                loginError.className = 'message error';
                loginError.style.display = 'block';
            }

            function hideLoginError() {
                loginError.style.display = 'none';
            }

            loginBtn.addEventListener('click', function() {
                const user = adminUser.value.trim();
                const pass = adminPass.value.trim();

                if (user === ADMIN_USER && pass === ADMIN_PASS) {
                    hideLoginError();
                    loginSection.style.display = 'none';
                    uploadForm.style.display = 'block';
                } else {
                    showLoginError('用户名或密码错误');
                }
            });

            togglePass.addEventListener('click', function() {
                const type = adminPass.type === 'password' ? 'text' : 'password';
                adminPass.type = type;
                togglePass.textContent = type === 'password' ? '显示' : '隐藏';
            });

            fileInput.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    fileName.textContent = '已选择: ' + e.target.files[0].name;
                    if (!targetPath.value) {
                        targetPath.value = e.target.files[0].name;
                    }
                } else {
                    fileName.textContent = '';
                }
            });

            function resetForm() {
                fileInput.value = '';
                fileName.textContent = '';
                targetPath.value = '';
                commitMsg.value = '上传文件 via upload';
                progressBar.style.display = 'none';
                progressFill.style.width = '0%';
                progressText.textContent = '';
                successMessage.style.display = 'none';
                errorMessage.style.display = 'none';
                uploadBtn.disabled = false;
            }

            function showError(msg) {
                errorMessage.textContent = msg;
                errorMessage.className = 'message error';
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
                uploadBtn.disabled = false;
                progressBar.style.display = 'none';
                progressText.textContent = '';
            }

            function showSuccess() {
                successMessage.className = 'message success';
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                uploadBtn.disabled = false;
            }

            function updateProgress(percent, text) {
                progressFill.style.width = percent + '%';
                progressText.textContent = text;
            }

            function getFileSha(path, callback) {
                const url = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + path;
                const xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.setRequestHeader('Authorization', 'token ' + GITHUB_APIKEY);
                xhr.setRequestHeader('Accept', 'application/vnd.github.v3+json');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            const data = JSON.parse(xhr.responseText);
                            callback(null, data.sha);
                        } else {
                            callback(null, null);
                        }
                    }
                };
                xhr.onerror = function() {
                    callback(null, null);
                };
                xhr.send();
            }

            function uploadFile() {
                const path = targetPath.value.trim();
                const message = commitMsg.value.trim() || '上传文件';

                if (!path) {
                    showError('请输入目标路径');
                    return;
                }

                if (!fileInput.files || fileInput.files.length === 0) {
                    showError('请选择要上传的文件');
                    return;
                }

                if (!GITHUB_APIKEY || !REPO_OWNER || !REPO_NAME) {
                    var missing = [];
                    if (!GITHUB_APIKEY) missing.push('APIKEY');
                    if (!REPO_OWNER) missing.push('REPO_OWNER');
                    if (!REPO_NAME) missing.push('REPO_NAME');
                    showError('系统配置未完成：缺少 ' + missing.join(', ') + '。请检查 GitHub Secrets 配置。');
                    return;
                }

                const file = fileInput.files[0];
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    const contentBase64 = e.target.result.split(',')[1];
                    startUpload(path, message, contentBase64);
                };
                reader.onerror = function() {
                    showError('文件读取失败');
                };
                reader.readAsDataURL(file);
            }

            function startUpload(path, message, contentBase64) {
                uploadBtn.disabled = true;
                progressBar.style.display = 'block';
                updateProgress(5, '正在准备上传...');

                getFileSha(path, function(error, sha) {
                    if (error) {
                        showError('获取文件信息失败');
                        return;
                    }

                    updateProgress(20, '正在连接服务器...');

                    const url = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + path;
                    
                    const body = {
                        message: message,
                        content: contentBase64,
                        branch: 'main'
                    };

                    if (sha) {
                        body.sha = sha;
                    }

                    const xhr = new XMLHttpRequest();
                    xhr.open('PUT', url, true);
                    xhr.setRequestHeader('Authorization', 'token ' + GITHUB_APIKEY);
                    xhr.setRequestHeader('Accept', 'application/vnd.github.v3+json');
                    xhr.setRequestHeader('Content-Type', 'application/json');

                    xhr.upload.onprogress = function(e) {
                        if (e.lengthComputable) {
                            const percent = Math.round((e.loaded / e.total) * 100);
                            const displayedPercent = 20 + (percent * 0.6);
                            updateProgress(Math.min(displayedPercent, 90), '正在上传: ' + percent + '%');
                        }
                    };

                    xhr.upload.onload = function() {
                        updateProgress(95, '上传完成，处理中...');
                    };

                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 201 || xhr.status === 200) {
                                updateProgress(100, '上传成功！');
                                showSuccess();
                                setTimeout(function() {
                                    window.location.reload();
                                }, 2000);
                            } else {
                                let errorMsg = '上传失败';
                                try {
                                    const data = JSON.parse(xhr.responseText);
                                    errorMsg = 'HTTP ' + xhr.status + ': ' + (data.message || errorMsg);
                                } catch (e) {
                                    errorMsg = 'HTTP ' + xhr.status + ': ' + errorMsg;
                                }
                                showError(errorMsg);
                            }
                        }
                    };

                    xhr.onerror = function() {
                        showError('网络连接失败');
                    };

                    xhr.ontimeout = function() {
                        showError('请求超时');
                    };

                    xhr.send(JSON.stringify(body));
                });
            }

            uploadBtn.addEventListener('click', uploadFile);

            cancelBtn.addEventListener('click', closeModal);
        </script>
    </body>
</html>
"""

dir_template = """
<a href="{dir_name}/index.html" class="entry">
    <span>📂 {dir_name}</span>
    <span class="file-info">
        <span>{size}</span>
    </span>
</a>
"""

file_template = """
<a href="{file_name}" class="entry">
    <span>📄 {file_name}</span>
    <span class="file-info">
        <span>{size}</span>
    </span>
</a>
"""

def get_dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}PB"

def copy_files(source_dir, output_dir):
    exclude_dir = os.path.basename(output_dir)
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != exclude_dir]
        files = [f for f in files if not f.startswith('.')]

        rel_path = os.path.relpath(root, source_dir)
        dest_dir = os.path.join(output_dir, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy2(src, dst)

def generate_index_html(root_dir):
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        rel_path = os.path.relpath(root, root_dir)
        full_path = rel_path if rel_path != '.' else ''

        content = ''
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            dir_size = format_size(get_dir_size(dir_path))
            content += dir_template.format(dir_name=dir_name, size=dir_size)
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md','build.py','favicon.ico','CNAME','404.html']:
                file_path = os.path.join(root, file_name)
                file_size = format_size(os.path.getsize(file_path))
                content += file_template.format(
                    file_name=file_name,
                    size=file_size
                )

        info = {"files": [], "dirs": []}
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md','build.py','CNAME','404.html']:
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path)
                with open(file_path, 'rb') as f:
                    sha256_hash = hashlib.sha256(f.read()).hexdigest()
                info["files"].append({
                    "name": file_name,
                    "sha256": sha256_hash,
                    "size": file_size
                })
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            dir_size = get_dir_size(dir_path)
            info["dirs"].append({
                "name": dir_name,
                "size": dir_size
            })

        with open(os.path.join(root, 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4)

        info_md_path = os.path.join(root, 'info.md')
        info_placeholder = ''
        if os.path.exists(info_md_path):
            with open(info_md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                info_html = markdown.markdown(md_content)
                info_placeholder = f'<div>{info_html}</div>'

        index_content = template
        index_content = index_content.replace('FULLPATH', full_path or 'Home')
        index_content = index_content.replace('INFOCONTENT', info_placeholder)
        index_content = index_content.replace('FILECONTENT', content)

        index_content = index_content.replace('__ADMIN_USER__', ADMIN_USER)
        index_content = index_content.replace('__ADMIN_PASS__', ADMIN_PASS)
        index_content = index_content.replace('__GITHUB_APIKEY__', GITHUB_APIKEY)
        index_content = index_content.replace('__REPO_OWNER__', REPO_OWNER)
        index_content = index_content.replace('__REPO_NAME__', REPO_NAME)

        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_content)

if __name__ == "__main__":
    source_dir = '.'
    output_dir = 'build'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    copy_files(source_dir, output_dir)

    generate_index_html(output_dir)