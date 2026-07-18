import os
import json
import hashlib
import markdown
import shutil

upload_page = """
<html>
    <head>
        <meta charset="utf-8">
        <title>文件上传 - boring_student</title>
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
                max-width: 600px;
                margin: 20px auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
                text-align: center;
            }}
            .form-group {{
                margin: 20px 0;
            }}
            label {{
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: bold;
            }}
            input[type="text"], input[type="password"], textarea {{
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                box-sizing: border-box;
                transition: border-color 0.3s;
            }}
            input[type="text"]:focus, input[type="password"]:focus, textarea:focus {{
                border-color: #2c82c9;
                outline: none;
            }}
            input[type="file"] {{
                width: 100%;
                padding: 10px;
                border: 2px dashed #ddd;
                border-radius: 8px;
                background: #f9f9f9;
                cursor: pointer;
                transition: all 0.3s;
            }}
            input[type="file"]:hover {{
                border-color: #2c82c9;
                background: #f0f8ff;
            }}
            .btn {{
                width: 100%;
                padding: 14px;
                background: #2c82c9;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
                margin-top: 10px;
            }}
            .btn:hover {{
                background: #1a5a8a;
            }}
            .btn-secondary {{
                background: #666;
            }}
            .btn-secondary:hover {{
                background: #444;
            }}
            .btn:disabled {{
                background: #ccc;
                cursor: not-allowed;
            }}
            .progress-bar {{
                width: 100%;
                height: 20px;
                background: #eee;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
                display: none;
            }}
            .progress-fill {{
                height: 100%;
                background: #2c82c9;
                width: 0%;
                transition: width 0.3s;
            }}
            .message {{
                padding: 12px;
                border-radius: 8px;
                margin: 10px 0;
                display: none;
            }}
            .message.success {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}
            .message.error {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}
            .back-link {{
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #2c82c9;
                text-decoration: none;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
            .upload-type {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}
            .upload-type label {{
                flex: 1;
                text-align: center;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 0;
                font-weight: normal;
            }}
            .upload-type input[type="radio"]:checked + label {{
                border-color: #2c82c9;
                background: #e8f4fc;
                color: #2c82c9;
                font-weight: bold;
            }}
            .upload-type input[type="radio"] {{
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📤 文件上传</h1>
            
            <div class="upload-type">
                <input type="radio" id="type-file" name="upload-type" value="file" checked>
                <label for="type-file">📁 上传文件</label>
                <input type="radio" id="type-text" name="upload-type" value="text">
                <label for="type-text">📝 创建文本</label>
            </div>

            <div class="form-group">
                <label for="file-input">选择文件</label>
                <input type="file" id="file-input" accept="*">
                <div id="file-name" style="margin-top: 8px; color: #666;"></div>
            </div>

            <div class="form-group" id="text-content-group" style="display: none;">
                <label for="text-content">文本内容</label>
                <textarea id="text-content" rows="8" placeholder="输入文本内容..."></textarea>
            </div>

            <div class="form-group">
                <label for="target-path">目标路径</label>
                <input type="text" id="target-path" placeholder="例如: docs/myfile.txt">
            </div>

            <div class="form-group">
                <label for="commit-msg">提交信息</label>
                <input type="text" id="commit-msg" placeholder="上传文件" value="上传文件 via upload">
            </div>

            <div class="form-group">
                <label for="github-token">GitHub PAT Token</label>
                <input type="password" id="github-token" placeholder="输入你的GitHub Personal Access Token">
                <small style="color: #666;">需要 repo 权限的PAT，不会被保存</small>
            </div>

            <div class="progress-bar" id="progress-bar">
                <div class="progress-fill" id="progress-fill"></div>
            </div>

            <div class="message" id="success-message">上传成功！页面将自动刷新...</div>
            <div class="message" id="error-message"></div>

            <button class="btn" id="upload-btn">开始上传</button>
            <button class="btn btn-secondary" id="cancel-btn">取消</button>

            <a href="index.html" class="back-link">⬅ 返回文件列表</a>
        </div>

        <script>
            const fileInput = document.getElementById('file-input');
            const fileName = document.getElementById('file-name');
            const textContentGroup = document.getElementById('text-content-group');
            const textContent = document.getElementById('text-content');
            const targetPath = document.getElementById('target-path');
            const commitMsg = document.getElementById('commit-msg');
            const githubToken = document.getElementById('github-token');
            const uploadBtn = document.getElementById('upload-btn');
            const cancelBtn = document.getElementById('cancel-btn');
            const progressBar = document.getElementById('progress-bar');
            const progressFill = document.getElementById('progress-fill');
            const successMessage = document.getElementById('success-message');
            const errorMessage = document.getElementById('error-message');
            const typeFile = document.getElementById('type-file');
            const typeText = document.getElementById('type-text');

            typeFile.addEventListener('change', () => {
                fileInput.style.display = 'block';
                textContentGroup.style.display = 'none';
            });

            typeText.addEventListener('change', () => {
                fileInput.style.display = 'none';
                textContentGroup.style.display = 'block';
            });

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    fileName.textContent = `已选择: ${e.target.files[0].name}`;
                    if (!targetPath.value) {
                        targetPath.value = e.target.files[0].name;
                    }
                } else {
                    fileName.textContent = '';
                }
            });

            function showError(msg) {
                errorMessage.textContent = msg;
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
                uploadBtn.disabled = false;
                progressBar.style.display = 'none';
            }

            function showSuccess() {
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';
                uploadBtn.disabled = false;
                progressBar.style.display = 'none';
            }

            async function uploadFile() {
                const token = githubToken.value.trim();
                const path = targetPath.value.trim();
                const message = commitMsg.value.trim() || '上传文件';

                if (!token) {
                    showError('请输入GitHub PAT Token');
                    return;
                }
                if (!path) {
                    showError('请输入目标路径');
                    return;
                }

                let contentBase64;

                if (typeFile.checked) {
                    if (!fileInput.files || fileInput.files.length === 0) {
                        showError('请选择要上传的文件');
                        return;
                    }
                    const file = fileInput.files[0];
                    progressBar.style.display = 'block';
                    progressFill.style.width = '10%';
                    
                    contentBase64 = await new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            const result = e.target.result;
                            resolve(result.split(',')[1]);
                        };
                        reader.onerror = reject;
                        reader.readAsDataURL(file);
                    });
                } else {
                    const text = textContent.value;
                    if (!text) {
                        showError('请输入文本内容');
                        return;
                    }
                    contentBase64 = btoa(unescape(encodeURIComponent(text)));
                }

                uploadBtn.disabled = true;
                progressFill.style.width = '30%';

                try {
                    const repoUrl = window.location.href;
                    const urlParts = repoUrl.split('/');
                    let owner = urlParts[3];
                    let repo = urlParts[4];
                    
                    if (repo.includes('.')) {
                        repo = repo.split('.')[0];
                    }

                    const apiUrl = `https://api.github.com/repos/${owner}/${repo}/actions/workflows/upload.yml/dispatches`;
                    
                    progressFill.style.width = '50%';

                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: {
                            'Authorization': `token ${token}`,
                            'Accept': 'application/vnd.github.v3+json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            ref: 'main',
                            inputs: {
                                file_path: path,
                                file_content: contentBase64,
                                commit_message: message
                            }
                        })
                    });

                    progressFill.style.width = '80%';

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(`HTTP ${response.status}: ${errorData.message || '上传失败'}`);
                    }

                    progressFill.style.width = '100%';
                    showSuccess();

                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 3000);

                } catch (error) {
                    showError(error.message);
                    console.error('Upload error:', error);
                }
            }

            uploadBtn.addEventListener('click', uploadFile);

            cancelBtn.addEventListener('click', () => {
                window.location.href = 'index.html';
            });
        </script>
    </body>
</html>
"""

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
            .upload-btn {{
                display: inline-block;
                padding: 10px 20px;
                background: #2c82c9;
                color: white;
                border-radius: 8px;
                text-decoration: none;
                margin: 10px 0;
                transition: background 0.3s;
            }}
            .upload-btn:hover {{
                background: #1a5a8a;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📁 {full_path}</h1>
            {info}
            <div style="margin: 20px 0;">
                <a href="../" style="font-size: 1.1em;">⬆ 上级目录</a>
                <a href="upload.html" class="upload-btn" style="margin-left: 20px;">📤 上传文件</a>
            </div>
            {content}
            <hr>
            <a style="text-decoration: none; color: #34495e; font-size: 15px; font-weight: 400;" href="https://beian.miit.gov.cn/#/Integrated/recordQuery" target="_blank">闽ICP备2025107306号-1</a>
        </div>
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

def generate_upload_page(output_dir):
    with open(os.path.join(output_dir, 'upload.html'), 'w', encoding='utf-8') as f:
        f.write(upload_page)

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
            if file_name not in ['index.html', 'info.json', 'info.md','build.py','favicon.ico','CNAME','404.html','upload.html']:
                file_path = os.path.join(root, file_name)
                file_size = format_size(os.path.getsize(file_path))
                content += file_template.format(
                    file_name=file_name,
                    size=file_size
                )

        info = {"files": [], "dirs": []}
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md','build.py','CNAME','404.html','upload.html']:
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

        index_content = template.format(
            full_path=full_path or 'Home',
            content=content,
            info=info_placeholder
        )
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_content)

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            with open(os.path.join(dir_path, 'upload.html'), 'w', encoding='utf-8') as f:
                f.write(upload_page)

if __name__ == "__main__":
    source_dir = '.'
    output_dir = 'build'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    copy_files(source_dir, output_dir)

    generate_upload_page(output_dir)

    generate_index_html(output_dir)