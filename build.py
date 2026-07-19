import os
import json
import hashlib
import markdown
import shutil

# 读取模板内容
template = """
<html>
    <head>
        <meta charset="utf-8">
        <title>{full_path} - boring_student </title>
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{full_path}</h1>
            {info}
            <div style="margin: 20px 0;">
                <a href="../" style="font-size: 1.1em;">⬆ 上级目录</a>
            </div>
            {content}
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
                    var repoOwner = 'boringstudent';
                    var repoName = 'new-cloud';
                    var filePath = 'build/' + file.name;

                    var data = {{
                        message: 'Upload file: ' + file.name,
                        content: base64Content
                    }};

                    var uploadXhr = new XMLHttpRequest();
                    var uploadUrl = 'https://api.github.com/repos/' + repoOwner + '/' + repoName + '/contents/' + filePath;
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
                                location.reload();
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
        </script>
    </body>
</html>
"""

dir_template = """
<a href="{dir_name}/index.html" class="entry">
    <span>{dir_name}/</span>
    <span class="file-info">
        <span>{size}</span>
    </span>
</a>
"""

file_template = """
<a href="{file_name}" class="entry">
    <span>{file_name}</span>
    <span class="file-info">
        <span>{size}</span>
    </span>
</a>
"""

def get_dir_size(start_path):  # 新增目录大小计算函数
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
    """将非隐藏文件/目录复制到output目录"""
    exclude_dir = os.path.basename(output_dir)  # 获取要排除的目录名
    exclude_files = {'build.py', 'upload.yml'}
    for root, dirs, files in os.walk(source_dir):
        # 排除隐藏目录和输出目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != exclude_dir]
        # 排除隐藏文件和指定文件
        files = [f for f in files if not f.startswith('.') and f not in exclude_files]

        # 计算目标路径
        rel_path = os.path.relpath(root, source_dir)
        dest_dir = os.path.join(output_dir, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        # 复制文件
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy2(src, dst)

def generate_index_html(root_dir):
    """在指定目录生成索引文件"""
    for root, dirs, files in os.walk(root_dir):
        # 忽略隐藏文件和目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # 计算路径信息
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

        # 生成info.json
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

        # 写入info.json
        with open(os.path.join(root, 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=4)

        # 处理info.md
        info_md_path = os.path.join(root, 'info.md')
        info_placeholder = ''
        if os.path.exists(info_md_path):
            with open(info_md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                info_html = markdown.markdown(md_content)
                info_placeholder = f'<div>{info_html}</div>'

        # 生成index.html
        index_content = template.format(
            full_path=full_path or 'Home',
            content=content,
            info=info_placeholder
        )
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_content)

if __name__ == "__main__":
    source_dir = '.'  # 源目录
    output_dir = 'build'  # 输出目录

    # 创建output目录前先删除已存在的目录（关键修复）
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 复制文件到output目录
    copy_files(source_dir, output_dir)

    # 生成索引文件
    generate_index_html(output_dir)
