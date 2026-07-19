import os
import shutil

STORAGE_REPO = os.environ.get('CLOUD', 'boringstudent/new-cloud')
REPO_OWNER = STORAGE_REPO.split('/')[0]
REPO_NAME = STORAGE_REPO.split('/')[1] if '/' in STORAGE_REPO else STORAGE_REPO
DEFAULT_BRANCH = os.environ.get('BRANCH', 'main')

template = """
<html>
    <head>
        <meta charset="utf-8">
        <title>{title} - boring_student</title>
        <link rel="icon" href="./favicon.ico" type="image/x-icon">
        <link rel="shortcut icon" href="./favicon.ico" type="image/x-icon">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                min-height: 100vh;
                background-size: cover;
                background-position: center;
            }}
            body {{
                background: url('https://www.loliapi.com/acg') fixed;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
            }}
            .entry {{
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
            }}
            .entry:hover {{
                transform: translateX(10px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                background: rgba(235, 245, 255, 0.9);
            }}
            .file-info {{
                display: flex;
                gap: 15px;
                color: #666;
                font-size: 0.9em;
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }}
            a {{
                color: #2c82c9;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .btn {{
                background: #2c82c9;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }}
            .btn:hover {{
                background: #1a5a8a;
            }}
            .btn:disabled {{
                background: #ccc;
                cursor: not-allowed;
            }}
            .modal-overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                justify-content: center;
                align-items: center;
            }}
            .modal-overlay.show {{
                display: flex;
            }}
            .modal-content {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
                width: 90%;
                max-width: 400px;
                box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
                position: relative;
            }}
            .modal-close {{
                position: absolute;
                top: 15px;
                right: 15px;
                font-size: 24px;
                cursor: pointer;
                color: #666;
            }}
            .modal-close:hover {{
                color: #333;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            .form-group label {{
                display: block;
                margin-bottom: 5px;
                color: #333;
            }}
            .form-group input[type="text"],
            .form-group input[type="password"],
            .form-group input[type="file"] {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-sizing: border-box;
                font-size: 14px;
            }}
            .form-group input[type="file"] {{
                padding: 5px;
            }}
            .progress-container {{
                margin: 15px 0;
            }}
            .progress-bar {{
                width: 100%;
                height: 20px;
                background: #eee;
                border-radius: 10px;
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                background: #2c82c9;
                width: 0%;
                transition: width 0.3s;
                border-radius: 10px;
            }}
            .progress-text {{
                text-align: center;
                margin-top: 5px;
                font-size: 14px;
                color: #666;
            }}
            .message {{
                margin-top: 15px;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }}
            .message.success {{
                background: #d4edda;
                color: #155724;
            }}
            .message.error {{
                background: #f8d7da;
                color: #721c24;
            }}
            .loading {{
                text-align: center;
                color: #666;
                padding: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 id="pageTitle">Home</h1>
            <div id="breadcrumbs" style="margin: 20px 0; font-size: 1.1em;"></div>
            <div id="fileListContainer" class="loading">加载中...</div>
        </div>
        <button class="btn" onclick="openUploadModal()" style="position: fixed; bottom: 30px; right: 30px; z-index: 100;">上传文件</button>

        <div id="uploadModal" class="modal-overlay">
            <div class="modal-content">
                <span class="modal-close" onclick="closeUploadModal()">&times;</span>
                <h2>上传文件</h2>
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" id="username" placeholder="请输入用户名">
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" id="password" placeholder="请输入密码">
                </div>
                <div class="form-group">
                    <label>选择文件</label>
                    <input type="file" id="fileInput">
                </div>
                <div class="progress-container" style="display: none;">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="progress-text" id="progressText">0%</div>
                </div>
                <button class="btn" onclick="uploadFile()" id="uploadBtn" style="width: 100%;">开始上传</button>
                <div id="uploadMessage" class="message"></div>
            </div>
        </div>

        <script>
            var REPO_OWNER = '{repo_owner}';
            var REPO_NAME = '{repo_name}';
            var DEFAULT_BRANCH = '{default_branch}';

            function openUploadModal() {{
                document.getElementById('uploadModal').classList.add('show');
            }}

            function closeUploadModal() {{
                document.getElementById('uploadModal').classList.remove('show');
                document.getElementById('uploadMessage').className = 'message';
                document.getElementById('uploadMessage').textContent = '';
                document.querySelector('.progress-container').style.display = 'none';
                document.getElementById('progressFill').style.width = '0%';
                document.getElementById('progressText').textContent = '0%';
            }}

            function showMessage(text, type) {{
                var msg = document.getElementById('uploadMessage');
                msg.className = 'message ' + type;
                msg.textContent = text;
            }}

            function formatSize(size) {{
                if (size === undefined || size === null) return '0B';
                for (var unit of ['B', 'KB', 'MB', 'GB', 'TB']) {{
                    if (size < 1024.0) {{
                        return size.toFixed(1) + unit;
                    }}
                    size /= 1024.0;
                }}
                return size.toFixed(1) + 'PB';
            }}

            function getCurrentPath() {{
                var path = window.location.pathname;
                if (path.endsWith('/')) {{
                    path = path.substring(0, path.length - 1);
                }}
                if (path === '') {{
                    return '';
                }}
                var parts = path.split('/');
                if (parts.length > 0 && parts[0] === REPO_NAME) {{
                    return parts.slice(1).join('/');
                }}
                return path.substring(1);
            }}

            function updateBreadcrumbs() {{
                var path = getCurrentPath();
                var crumbs = document.getElementById('breadcrumbs');
                crumbs.innerHTML = '';

                if (path === '') {{
                    var homeSpan = document.createElement('span');
                    homeSpan.style.color = '#666';
                    homeSpan.textContent = '当前位置:';
                    var homeStrong = document.createElement('strong');
                    homeStrong.textContent = ' Home';
                    homeSpan.appendChild(homeStrong);
                    crumbs.appendChild(homeSpan);
                    return;
                }}

                var parts = path.split('/');
                var labelSpan = document.createElement('span');
                labelSpan.style.color = '#666';
                labelSpan.textContent = '当前位置: ';
                crumbs.appendChild(labelSpan);

                var homeLink = document.createElement('a');
                homeLink.href = '/';
                homeLink.textContent = 'Home';
                crumbs.appendChild(homeLink);

                var currentPath = '';
                for (var i = 0; i < parts.length; i++) {{
                    currentPath += '/' + parts[i];
                    var separator = document.createElement('span');
                    separator.textContent = ' / ';
                    crumbs.appendChild(separator);

                    var link = document.createElement('a');
                    link.href = currentPath + '/';
                    link.textContent = parts[i];
                    crumbs.appendChild(link);
                }}
            }}

            function loadFileList() {{
                var path = getCurrentPath();
                var apiUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + path;

                var container = document.getElementById('fileListContainer');
                container.innerHTML = '<div class="loading">加载中...</div>';

                var xhr = new XMLHttpRequest();
                xhr.open('GET', apiUrl, true);

                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        try {{
                            var items = JSON.parse(xhr.responseText);
                            renderFileList(items);
                        }} catch (e) {{
                            container.innerHTML = '<div class="message error">解析文件列表失败</div>';
                        }}
                    }} else if (xhr.status === 403) {{
                        container.innerHTML = '<div class="message error">API请求受限，请稍后重试</div>';
                    }} else if (xhr.status === 404) {{
                        container.innerHTML = '<div class="message error">目录不存在</div>';
                    }} else {{
                        container.innerHTML = '<div class="message error">获取文件列表失败，状态码: ' + xhr.status + '</div>';
                    }}
                }};

                xhr.onerror = function() {{
                    container.innerHTML = '<div class="message error">网络错误，无法获取文件列表</div>';
                }};

                xhr.send();
            }}

            function renderFileList(items) {{
                var container = document.getElementById('fileListContainer');
                container.innerHTML = '';

                var dirs = items.filter(function(item) {{ return item.type === 'dir'; }});
                var files = items.filter(function(item) {{ return item.type === 'file'; }});

                dirs.sort(function(a, b) {{ return a.name.localeCompare(b.name); }});
                files.sort(function(a, b) {{ return a.name.localeCompare(b.name); }});

                var currentPath = getCurrentPath();
                var baseUrl = currentPath ? '/' + currentPath + '/' : '/';

                dirs.forEach(function(dir) {{
                    var entry = document.createElement('a');
                    entry.href = baseUrl + encodeURIComponent(dir.name) + '/';
                    entry.className = 'entry';
                    var nameSpan = document.createElement('span');
                    nameSpan.textContent = dir.name + '/';
                    var infoSpan = document.createElement('span');
                    infoSpan.className = 'file-info';
                    var sizeSpan = document.createElement('span');
                    sizeSpan.textContent = '-';
                    infoSpan.appendChild(sizeSpan);
                    entry.appendChild(nameSpan);
                    entry.appendChild(infoSpan);
                    container.appendChild(entry);
                }});

                files.forEach(function(file) {{
                    if (file.name === 'index.html' || file.name === 'info.json' || file.name === 'info.md') {{
                        return;
                    }}
                    var entry = document.createElement('a');
                    entry.href = 'https://raw.githubusercontent.com/' + REPO_OWNER + '/' + REPO_NAME + '/' + DEFAULT_BRANCH + '/' + encodeURI(file.path);
                    entry.target = '_blank';
                    entry.className = 'entry';
                    var nameSpan = document.createElement('span');
                    nameSpan.textContent = file.name;
                    var infoSpan = document.createElement('span');
                    infoSpan.className = 'file-info';
                    var sizeSpan = document.createElement('span');
                    sizeSpan.textContent = formatSize(file.size);
                    infoSpan.appendChild(sizeSpan);
                    entry.appendChild(nameSpan);
                    entry.appendChild(infoSpan);
                    container.appendChild(entry);
                }});

                if (dirs.length === 0 && files.length === 0) {{
                    container.innerHTML = '<div class="loading">此目录为空</div>';
                }}
            }}

            function uploadFile() {{
                var username = document.getElementById('username').value;
                var password = document.getElementById('password').value;
                var fileInput = document.getElementById('fileInput');
                var uploadBtn = document.getElementById('uploadBtn');

                if (!username || !password) {{
                    showMessage('请输入用户名和密码', 'error');
                    return;
                }}

                if (!fileInput.files || fileInput.files.length === 0) {{
                    showMessage('请选择要上传的文件', 'error');
                    return;
                }}

                var file = fileInput.files[0];
                uploadBtn.disabled = true;

                showMessage('正在获取授权...', 'success');

                var params = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password);
                var keyUrl = 'https://api.boring-student.cn/?' + params;

                var xhr = new XMLHttpRequest();
                xhr.open('GET', keyUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        try {{
                            var response = JSON.parse(xhr.responseText);
                            if (response.success && response.key) {{
                                uploadToGitHub(response.key, file);
                            }} else {{
                                showMessage('获取授权失败', 'error');
                                uploadBtn.disabled = false;
                            }}
                        }} catch (e) {{
                            showMessage('解析授权响应失败', 'error');
                            uploadBtn.disabled = false;
                        }}
                    }} else {{
                        showMessage('获取授权失败，状态码: ' + xhr.status, 'error');
                        uploadBtn.disabled = false;
                    }}
                }};
                xhr.onerror = function() {{
                    showMessage('网络错误，无法获取授权', 'error');
                    uploadBtn.disabled = false;
                }};
                xhr.send();
            }}

            function uploadToGitHub(key, file) {{
                var reader = new FileReader();
                reader.onload = function(e) {{
                    var base64Content = e.target.result.split(',')[1];
                    var currentPath = getCurrentPath();
                    var filePath = currentPath ? currentPath + '/' + file.name : file.name;

                    var data = {{
                        message: 'Upload file: ' + file.name,
                        content: base64Content
                    }};

                    var uploadXhr = new XMLHttpRequest();
                    var uploadUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + filePath;
                    uploadXhr.open('PUT', uploadUrl, true);
                    uploadXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                    uploadXhr.setRequestHeader('Content-Type', 'application/json');

                    var progressContainer = document.querySelector('.progress-container');
                    progressContainer.style.display = 'block';
                    showMessage('正在上传...', 'success');

                    uploadXhr.upload.onprogress = function(e) {{
                        if (e.lengthComputable) {{
                            var percent = Math.round((e.loaded / e.total) * 100);
                            document.getElementById('progressFill').style.width = percent + '%';
                            document.getElementById('progressText').textContent = percent + '%';
                        }}
                    }};

                    uploadXhr.onload = function() {{
                        if (uploadXhr.status === 200 || uploadXhr.status === 201) {{
                            showMessage('上传成功！', 'success');
                            setTimeout(function() {{
                                closeUploadModal();
                                loadFileList();
                            }}, 1500);
                        }} else {{
                            try {{
                                var error = JSON.parse(uploadXhr.responseText);
                                showMessage('上传失败: ' + (error.message || '未知错误'), 'error');
                            }} catch (e) {{
                                showMessage('上传失败，状态码: ' + uploadXhr.status, 'error');
                            }}
                            document.getElementById('uploadBtn').disabled = false;
                        }}
                    }};

                    uploadXhr.onerror = function() {{
                        showMessage('网络错误，上传失败', 'error');
                        document.getElementById('uploadBtn').disabled = false;
                    }};

                    uploadXhr.send(JSON.stringify(data));
                }};
                reader.readAsDataURL(file);
            }}

            document.addEventListener('DOMContentLoaded', function() {{
                updateBreadcrumbs();
                loadFileList();
            }});
        </script>
    </body>
</html>
"""

def copy_static_files(output_dir):
    static_files = ['404.html', 'favicon.ico', 'CNAME']
    for filename in static_files:
        src = os.path.join('.', filename)
        dst = os.path.join(output_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)

if __name__ == "__main__":
    output_dir = 'build'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    copy_static_files(output_dir)

    index_content = template.format(
        title='Home',
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        default_branch=DEFAULT_BRANCH
    )
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f'Build completed. Storage repo: {REPO_OWNER}/{REPO_NAME}')
