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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
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
            .delete-btn {{
                background: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin-left: 10px;
                transition: background 0.3s;
            }}
            .delete-btn:hover {{
                background: #c82333;
            }}
            .menu-btn {{
                background: transparent;
                color: #666;
                border: none;
                padding: 5px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                margin-left: 10px;
                transition: all 0.3s;
            }}
            .menu-btn:hover {{
                background: rgba(0,0,0,0.1);
            }}
            .context-menu {{
                display: none;
                position: absolute;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 2000;
                min-width: 120px;
            }}
            .context-menu.show {{
                display: block;
            }}
            .context-menu-item {{
                padding: 8px 12px;
                cursor: pointer;
                font-size: 14px;
                color: #333;
            }}
            .context-menu-item:hover {{
                background: #f0f0f0;
            }}
            .context-menu-item.danger {{
                color: #dc3545;
            }}
            .preview-modal-content {{
                max-width: 700px;
                max-height: 80vh;
                overflow-y: auto;
            }}
            .preview-audio, .preview-video {{
                width: 100%;
                max-width: 640px;
                margin: 10px 0;
            }}
            .preview-text {{
                width: 100%;
                height: 300px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-family: monospace;
                font-size: 14px;
                resize: none;
                background: #f8f8f8;
            }}
            .prop-table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .prop-table td {{
                padding: 10px 8px;
                border-bottom: 1px solid #eee;
                font-size: 14px;
            }}
            .prop-table td:first-child {{
                color: #666;
                width: 70px;
                white-space: nowrap;
            }}
            .prop-table td:last-child {{
                word-break: break-all;
            }}
            .folder-size {{
                font-style: italic;
                color: #999;
            }}
            .drop-zone {{
                border: 3px dashed #444;
                border-radius: 12px;
                padding: 40px 20px;
                text-align: center;
                color: #888;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 16px;
                background: #1a1a2e;
            }}
            .drop-zone:hover, .drop-zone.active {{
                border-color: #58a6ff;
                color: #58a6ff;
                background: rgba(88, 166, 255, 0.05);
            }}
            .drop-zone .dz-icon {{
                font-size: 48px;
                display: block;
                margin-bottom: 12px;
            }}
            .drop-zone .dz-text {{
                font-size: 16px;
                margin-bottom: 4px;
            }}
            .drop-zone .dz-hint {{
                font-size: 12px;
                color: #666;
            }}
            .upload-actions {{
                display: flex;
                gap: 12px;
                margin: 16px 0 12px;
            }}
            .upload-actions .btn {{
                flex: 1;
                font-size: 14px;
                padding: 12px 20px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
                background: #21262d;
                border: 1px solid #30363d;
                color: #c9d1d9;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .upload-actions .btn:hover {{
                background: #30363d;
                border-color: #58a6ff;
                color: #58a6ff;
            }}
            .folder-preview-list {{
                max-height: 350px;
                overflow-y: auto;
                background: #0d1117;
                border-radius: 8px;
                padding: 8px;
            }}
            .folder-preview-item {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 13px;
                color: #c9d1d9;
            }}
            .folder-preview-item:hover {{
                background: #161b22;
            }}
            .folder-preview-item .fp-icon {{
                font-size: 16px;
                width: 20px;
                text-align: center;
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
            <div class="modal-content" style="max-width: 560px;">
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
                <div class="drop-zone" id="dropZone">
                    <span class="dz-icon">&#128193;</span>
                    <div class="dz-text">拖拽文件或文件夹到此处</div>
                    <div class="dz-hint">或点击下方按钮选择文件</div>
                </div>
                <div class="upload-actions">
                    <input type="file" id="fileInput" multiple style="display:none;">
                    <input type="file" id="folderInput" webkitdirectory style="display:none;">
                    <button class="btn" onclick="document.getElementById('fileInput').click()">&#128196; 选择文件</button>
                    <button class="btn" onclick="document.getElementById('folderInput').click()">&#128193; 选择文件夹</button>
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

        <div id="deleteModal" class="modal-overlay">
            <div class="modal-content">
                <span class="modal-close" onclick="closeDeleteModal()">&times;</span>
                <h2 id="deleteModalTitle">删除</h2>
                <p style="color: #666; margin-bottom: 15px;" id="deleteConfirmText">确定要删除 <strong id="deleteFileName"></strong> 吗？此操作不可撤销。</p>
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" id="deleteUsername" placeholder="请输入用户名">
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" id="deletePassword" placeholder="请输入密码">
                </div>
                <button class="btn" onclick="confirmDelete()" id="deleteBtn" style="width: 100%;">确认删除</button>
                <div id="deleteMessage" class="message"></div>
            </div>
        </div>

        <div id="previewModal" class="modal-overlay">
            <div class="modal-content preview-modal-content">
                <span class="modal-close" onclick="closePreviewModal()">&times;</span>
                <h2 id="previewTitle">预览文件</h2>
                <div id="previewContent"></div>
                <div id="previewActions" style="margin-top: 15px; display: none;">
                    <button class="btn" onclick="savePreviewFile()" id="savePreviewBtn" style="width: 100%;">保存修改</button>
                    <div id="previewMessage" class="message"></div>
                </div>
            </div>
        </div>

        <div id="propertiesModal" class="modal-overlay">
            <div class="modal-content">
                <span class="modal-close" onclick="closePropertiesModal()">&times;</span>
                <h2>属性</h2>
                <div id="propertiesContent"></div>
            </div>
        </div>

        <div id="renameModal" class="modal-overlay">
            <div class="modal-content">
                <span class="modal-close" onclick="closeRenameModal()">&times;</span>
                <h2 id="renameTitle">重命名</h2>
                <div class="form-group">
                    <label>新名称</label>
                    <input type="text" id="renameInput" placeholder="请输入新名称">
                </div>
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" id="renameUsername" placeholder="请输入用户名">
                </div>
                <div class="form-group">
                    <label>密码</label>
                    <input type="password" id="renamePassword" placeholder="请输入密码">
                </div>
                <button class="btn" onclick="confirmRename()" id="renameBtn" style="width: 100%;">确认重命名</button>
                <div id="renameMessage" class="message"></div>
            </div>
        </div>

        <div id="contextMenu" class="context-menu">
            <div class="context-menu-item" id="ctx-preview" onclick="handleMenuAction('preview')">预览</div>
            <div class="context-menu-item" id="ctx-edit" onclick="handleMenuAction('edit')">重命名</div>
            <div class="context-menu-item" id="ctx-download" onclick="handleMenuAction('download')">下载</div>
            <div class="context-menu-item" id="ctx-properties" onclick="handleMenuAction('properties')">属性</div>
            <div class="context-menu-item danger" id="ctx-delete" onclick="handleMenuAction('delete')">删除</div>
        </div>

        <script>
            var REPO_OWNER = '{repo_owner}';
            var REPO_NAME = '{repo_name}';
            var DEFAULT_BRANCH = '{default_branch}';

            var menuFileInfo = {{}};
            var previewFileInfo = {{}};

            setInterval(function() {{
                loadFileList();
            }}, 60000);

            function openUploadModal() {{
                document.getElementById('uploadModal').classList.add('show');
                uploadFileList = [];
                initDropZone();
            }}

            function closeUploadModal() {{
                document.getElementById('uploadModal').classList.remove('show');
                document.getElementById('uploadMessage').className = 'message';
                document.getElementById('uploadMessage').textContent = '';
                document.querySelector('.progress-container').style.display = 'none';
                document.getElementById('progressFill').style.width = '0%';
                document.getElementById('progressText').textContent = '0%';
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('fileInput').value = '';
                document.getElementById('folderInput').value = '';
                uploadFileList = [];
            }}

            var uploadFileList = [];

            function initDropZone() {{
                var dz = document.getElementById('dropZone');
                if (!dz) return;
                dz.ondragover = function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    dz.classList.add('active');
                }};
                dz.ondragleave = function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    dz.classList.remove('active');
                }};
                dz.ondrop = function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    dz.classList.remove('active');
                    handleDroppedItems(e.dataTransfer.items);
                }};
                dz.onclick = function() {{
                    document.getElementById('fileInput').click();
                }};
            }}

            function handleDroppedItems(items) {{
                var entries = [];
                for (var i = 0; i < items.length; i++) {{
                    var entry = items[i].webkitGetAsEntry ? items[i].webkitGetAsEntry() : null;
                    if (entry) {{
                        entries.push(entry);
                    }}
                }}
                if (entries.length === 0) return;
                processEntries(entries);
            }}

            function processEntries(entries) {{
                entries.forEach(function(entry) {{
                    if (entry.isDirectory) {{
                        readDirectory(entry, '');
                    }} else if (entry.isFile) {{
                        entry.file(function(file) {{
                            addToUploadList(file, file.name);
                        }});
                    }}
                }});
            }}

            function readDirectory(dirEntry, path) {{
                var reader = dirEntry.createReader();
                reader.readEntries(function(entries) {{
                    entries.forEach(function(entry) {{
                        var fullPath = path ? path + '/' + entry.name : entry.name;
                        if (entry.isDirectory) {{
                            readDirectory(entry, fullPath);
                        }} else if (entry.isFile) {{
                            entry.file(function(file) {{
                                file._folderPath = fullPath;
                                addToUploadList(file, fullPath);
                            }});
                        }}
                    }});
                }});
            }}

            function addToUploadList(file, displayPath) {{
                var exists = uploadFileList.some(function(f) {{ return f._displayPath === displayPath && f.size === file.size; }});
                if (exists) return;
                file._displayPath = displayPath;
                uploadFileList.push(file);
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

            var deleteFilePath = '';
            var deleteFileSha = '';
            var deleteFileType = 'file';

            function openDeleteModal(filePath, fileSha, fileName, type) {{
                deleteFilePath = filePath;
                deleteFileSha = fileSha;
                deleteFileType = type || 'file';
                document.getElementById('deleteFileName').textContent = fileName;
                document.getElementById('deleteModalTitle').textContent = type === 'dir' ? '删除文件夹' : '删除文件';
                document.getElementById('deleteConfirmText').innerHTML = type === 'dir' ? '确定要删除文件夹 <strong>' + fileName + '</strong> 及其所有内容吗？此操作不可撤销。' : '确定要删除文件 <strong>' + fileName + '</strong> 吗？此操作不可撤销。';
                document.getElementById('deleteModal').classList.add('show');
            }}

            function closeDeleteModal() {{
                document.getElementById('deleteModal').classList.remove('show');
                document.getElementById('deleteMessage').className = 'message';
                document.getElementById('deleteMessage').textContent = '';
                document.getElementById('deleteUsername').value = '';
                document.getElementById('deletePassword').value = '';
            }}

            function showDeleteMessage(text, type) {{
                var msg = document.getElementById('deleteMessage');
                msg.className = 'message ' + type;
                msg.textContent = text;
            }}

            function openContextMenu(e, fileInfo) {{
                e.stopPropagation();
                e.preventDefault();
                menuFileInfo = fileInfo;
                
                var isDir = fileInfo.type === 'dir';
                document.getElementById('ctx-preview').style.display = '';
                document.getElementById('ctx-edit').style.display = '';
                document.getElementById('ctx-download').style.display = '';
                document.getElementById('ctx-properties').style.display = '';
                document.getElementById('ctx-delete').style.display = '';
                
                var menu = document.getElementById('contextMenu');
                var rect = e.target.getBoundingClientRect();
                
                menu.style.left = rect.right + 'px';
                menu.style.top = rect.top + 'px';
                menu.classList.add('show');
                
                document.addEventListener('click', closeContextMenuHandler);
            }}

            function closeContextMenu() {{
                var menu = document.getElementById('contextMenu');
                menu.classList.remove('show');
                document.removeEventListener('click', closeContextMenuHandler);
            }}

            function closeContextMenuHandler(e) {{
                var menu = document.getElementById('contextMenu');
                if (!menu.contains(e.target)) {{
                    closeContextMenu();
                }}
            }}

            function handleMenuAction(action) {{
                closeContextMenu();
                var filePath = menuFileInfo.path;
                var fileSha = menuFileInfo.sha;
                var fileName = menuFileInfo.name;
                var fileType = menuFileInfo.type || 'file';
                
                if (fileType === 'dir') {{
                    if (action === 'preview') {{
                        previewFolder(filePath, fileName);
                    }} else if (action === 'edit') {{
                        showRenameModal(filePath, fileName, 'dir');
                    }} else if (action === 'download') {{
                        downloadFolderAsZip(filePath, fileName);
                    }} else if (action === 'properties') {{
                        showProperties(filePath, fileName, fileType, fileSha);
                    }} else if (action === 'delete') {{
                        openDeleteModal(filePath, fileSha, fileName, 'dir');
                    }}
                }} else {{
                    if (action === 'preview') {{
                        previewFile(filePath, fileName);
                    }} else if (action === 'edit') {{
                        showRenameModal(filePath, fileName, 'file');
                    }} else if (action === 'download') {{
                        downloadFile(filePath, fileName);
                    }} else if (action === 'properties') {{
                        showProperties(filePath, fileName, fileType, fileSha);
                    }} else if (action === 'delete') {{
                        openDeleteModal(filePath, fileSha, fileName, 'file');
                    }}
                }}
            }}

            function downloadFile(filePath, fileName) {{
                var url = 'https://raw.githubusercontent.com/' + REPO_OWNER + '/' + REPO_NAME + '/' + DEFAULT_BRANCH + '/' + encodeURI(filePath);
                var link = document.createElement('a');
                link.href = url;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }}

            function getFileExtension(fileName) {{
                var parts = fileName.split('.');
                return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
            }}

            function previewFile(filePath, fileName) {{
                var ext = getFileExtension(fileName);
                var previewUrl = 'https://raw.githubusercontent.com/' + REPO_OWNER + '/' + REPO_NAME + '/' + DEFAULT_BRANCH + '/' + encodeURI(filePath);
                
                previewFileInfo = {{
                    path: filePath,
                    name: fileName,
                    ext: ext
                }};
                
                document.getElementById('previewTitle').textContent = '预览: ' + fileName;
                var content = document.getElementById('previewContent');
                content.innerHTML = '';
                var loadingDiv = document.createElement('div');
                loadingDiv.className = 'loading';
                loadingDiv.textContent = '加载中...';
                content.appendChild(loadingDiv);
                document.getElementById('previewModal').classList.add('show');
                document.getElementById('previewActions').style.display = 'none';
                document.getElementById('previewMessage').className = 'message';
                document.getElementById('previewMessage').textContent = '';
                
                if (['mp3', 'wav', 'ogg', 'aac', 'flac'].indexOf(ext) !== -1) {{
                    content.innerHTML = '';
                    var audio = document.createElement('audio');
                    audio.src = previewUrl;
                    audio.controls = true;
                    audio.className = 'preview-audio';
                    content.appendChild(audio);
                }} else if (['mp4', 'webm', 'ogg', 'avi', 'mov'].indexOf(ext) !== -1) {{
                    content.innerHTML = '';
                    var video = document.createElement('video');
                    video.src = previewUrl;
                    video.controls = true;
                    video.className = 'preview-video';
                    content.appendChild(video);
                }} else if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].indexOf(ext) !== -1) {{
                    content.innerHTML = '';
                    var img = document.createElement('img');
                    img.src = previewUrl;
                    img.alt = fileName;
                    img.style.maxWidth = '100%';
                    img.style.maxHeight = '60vh';
                    img.style.borderRadius = '8px';
                    content.appendChild(img);
                }} else {{
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', previewUrl, true);
                    xhr.onload = function() {{
                        if (xhr.status === 200) {{
                            var textarea = document.createElement('textarea');
                            textarea.className = 'preview-text';
                            textarea.value = xhr.responseText;
                            textarea.readOnly = true;
                            content.innerHTML = '';
                            content.appendChild(textarea);
                        }} else {{
                            content.innerHTML = '';
                            var msgDiv = document.createElement('div');
                            msgDiv.className = 'message error';
                            msgDiv.textContent = '无法加载文件内容';
                            content.appendChild(msgDiv);
                        }}
                    }};
                    xhr.onerror = function() {{
                        content.innerHTML = '';
                        var msgDiv = document.createElement('div');
                        msgDiv.className = 'message error';
                        msgDiv.textContent = '网络错误，无法加载文件';
                        content.appendChild(msgDiv);
                    }};
                    xhr.send();
                }}
            }}

            function editFile(filePath, fileName) {{
                var ext = getFileExtension(fileName);
                var previewUrl = 'https://raw.githubusercontent.com/' + REPO_OWNER + '/' + REPO_NAME + '/' + DEFAULT_BRANCH + '/' + encodeURI(filePath);
                
                previewFileInfo = {{
                    path: filePath,
                    name: fileName,
                    ext: ext
                }};
                
                document.getElementById('previewTitle').textContent = '编辑: ' + fileName;
                var content = document.getElementById('previewContent');
                content.innerHTML = '';
                var loadingDiv = document.createElement('div');
                loadingDiv.className = 'loading';
                loadingDiv.textContent = '加载中...';
                content.appendChild(loadingDiv);
                document.getElementById('previewModal').classList.add('show');
                document.getElementById('previewActions').style.display = 'none';
                document.getElementById('previewMessage').className = 'message';
                document.getElementById('previewMessage').textContent = '';
                
                var xhr = new XMLHttpRequest();
                xhr.open('GET', previewUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        var textarea = document.createElement('textarea');
                        textarea.className = 'preview-text';
                        textarea.value = xhr.responseText;
                        textarea.readOnly = false;
                        content.innerHTML = '';
                        content.appendChild(textarea);
                        document.getElementById('previewActions').style.display = 'block';
                    }} else {{
                        content.innerHTML = '';
                        var msgDiv = document.createElement('div');
                        msgDiv.className = 'message error';
                        msgDiv.textContent = '无法加载文件内容';
                        content.appendChild(msgDiv);
                    }}
                }};
                xhr.onerror = function() {{
                    content.innerHTML = '';
                    var msgDiv = document.createElement('div');
                    msgDiv.className = 'message error';
                    msgDiv.textContent = '网络错误，无法加载文件';
                    content.appendChild(msgDiv);
                }};
                xhr.send();
            }}

            function closePreviewModal() {{
                document.getElementById('previewModal').classList.remove('show');
            }}

            function showPreviewMessage(text, type) {{
                var msg = document.getElementById('previewMessage');
                msg.className = 'message ' + type;
                msg.textContent = text;
            }}

            function savePreviewFile() {{
                var textarea = document.querySelector('.preview-text');
                if (!textarea) return;
                
                var newContent = textarea.value;
                var saveBtn = document.getElementById('savePreviewBtn');
                
                saveBtn.disabled = true;
                showPreviewMessage('正在获取授权...', 'success');
                
                var username = prompt('请输入用户名:');
                var password = prompt('请输入密码:');
                
                if (!username || !password) {{
                    showPreviewMessage('请输入用户名和密码', 'error');
                    saveBtn.disabled = false;
                    return;
                }}
                
                var params = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password);
                var keyUrl = 'https://api.boring-student.cn/?' + params;
                
                var xhr = new XMLHttpRequest();
                xhr.open('GET', keyUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        try {{
                            var response = JSON.parse(xhr.responseText);
                            if (response.success && response.key) {{
                                updateFileOnGitHub(response.key, previewFileInfo.path, newContent);
                            }} else {{
                                showPreviewMessage('获取授权失败', 'error');
                                saveBtn.disabled = false;
                            }}
                        }} catch (e) {{
                            showPreviewMessage('解析授权响应失败', 'error');
                            saveBtn.disabled = false;
                        }}
                    }} else {{
                        showPreviewMessage('获取授权失败，状态码: ' + xhr.status, 'error');
                        saveBtn.disabled = false;
                    }}
                }};
                xhr.onerror = function() {{
                    showPreviewMessage('网络错误，无法获取授权', 'error');
                    saveBtn.disabled = false;
                }};
                xhr.send();
            }}

            function updateFileOnGitHub(key, filePath, newContent) {{
                var shaUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath);
                var shaXhr = new XMLHttpRequest();
                shaXhr.open('GET', shaUrl, true);
                shaXhr.onload = function() {{
                    if (shaXhr.status === 200) {{
                        try {{
                            var fileInfo = JSON.parse(shaXhr.responseText);
                            var sha = fileInfo.sha;
                            var base64Content = btoa(unescape(encodeURIComponent(newContent)));
                            
                            var data = {{
                                message: 'Update file: ' + filePath,
                                content: base64Content,
                                sha: sha
                            }};
                            
                            var updateXhr = new XMLHttpRequest();
                            var updateUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath);
                            updateXhr.open('PUT', updateUrl, true);
                            updateXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                            updateXhr.setRequestHeader('Content-Type', 'application/json');
                            
                            updateXhr.onload = function() {{
                                if (updateXhr.status === 200 || updateXhr.status === 201) {{
                                    showPreviewMessage('保存成功！', 'success');
                                    setTimeout(function() {{
                                        closePreviewModal();
                                        loadFileList();
                                    }}, 1500);
                                }} else {{
                                    try {{
                                        var error = JSON.parse(updateXhr.responseText);
                                        showPreviewMessage('保存失败: ' + (error.message || '未知错误'), 'error');
                                    }} catch (e) {{
                                        showPreviewMessage('保存失败，状态码: ' + updateXhr.status, 'error');
                                    }}
                                    document.getElementById('savePreviewBtn').disabled = false;
                                }}
                            }};
                            
                            updateXhr.onerror = function() {{
                                showPreviewMessage('网络错误，保存失败', 'error');
                                document.getElementById('savePreviewBtn').disabled = false;
                            }};
                            
                            updateXhr.send(JSON.stringify(data));
                        }} catch (e) {{
                            showPreviewMessage('获取文件信息失败', 'error');
                            document.getElementById('savePreviewBtn').disabled = false;
                        }}
                    }} else {{
                        showPreviewMessage('获取文件信息失败，状态码: ' + shaXhr.status, 'error');
                        document.getElementById('savePreviewBtn').disabled = false;
                    }}
                }};
                shaXhr.onerror = function() {{
                    showPreviewMessage('网络错误，无法获取文件信息', 'error');
                    document.getElementById('savePreviewBtn').disabled = false;
                }};
                shaXhr.send();
            }}

            function confirmDelete() {{
                var username = document.getElementById('deleteUsername').value;
                var password = document.getElementById('deletePassword').value;
                var deleteBtn = document.getElementById('deleteBtn');

                if (!username || !password) {{
                    showDeleteMessage('请输入用户名和密码', 'error');
                    return;
                }}

                deleteBtn.disabled = true;
                showDeleteMessage('正在获取授权...', 'success');

                var params = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password);
                var keyUrl = 'https://api.boring-student.cn/?' + params;

                var xhr = new XMLHttpRequest();
                xhr.open('GET', keyUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        try {{
                            var response = JSON.parse(xhr.responseText);
                            if (response.success && response.key) {{
                                if (deleteFileType === 'dir') {{
                                    deleteFolderItems(response.key, deleteFilePath);
                                }} else {{
                                    deleteFile(response.key, deleteFilePath, deleteFileSha);
                                }}
                            }} else {{
                                showDeleteMessage('获取授权失败', 'error');
                                deleteBtn.disabled = false;
                            }}
                        }} catch (e) {{
                            showDeleteMessage('解析授权响应失败', 'error');
                            deleteBtn.disabled = false;
                        }}
                    }} else {{
                        showDeleteMessage('获取授权失败，状态码: ' + xhr.status, 'error');
                        deleteBtn.disabled = false;
                    }}
                }};
                xhr.onerror = function() {{
                    showDeleteMessage('网络错误，无法获取授权', 'error');
                    deleteBtn.disabled = false;
                }};
                xhr.send();
            }}

            function deleteFile(key, filePath, sha) {{
                showDeleteMessage('正在删除...', 'success');

                var data = {{
                    message: 'Delete file: ' + filePath,
                    sha: sha
                }};

                var deleteXhr = new XMLHttpRequest();
                var deleteUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath);
                deleteXhr.open('DELETE', deleteUrl, true);
                deleteXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                deleteXhr.setRequestHeader('Content-Type', 'application/json');

                deleteXhr.onload = function() {{
                    if (deleteXhr.status === 200 || deleteXhr.status === 201) {{
                        showDeleteMessage('删除成功！', 'success');
                        setTimeout(function() {{
                            closeDeleteModal();
                            loadFileList();
                        }}, 1500);
                    }} else {{
                        try {{
                            var error = JSON.parse(deleteXhr.responseText);
                            showDeleteMessage('删除失败: ' + (error.message || '未知错误'), 'error');
                        }} catch (e) {{
                            showDeleteMessage('删除失败，状态码: ' + deleteXhr.status, 'error');
                        }}
                        document.getElementById('deleteBtn').disabled = false;
                    }}
                }};

                deleteXhr.onerror = function() {{
                    showDeleteMessage('网络错误，删除失败', 'error');
                    document.getElementById('deleteBtn').disabled = false;
                }};

                deleteXhr.send(JSON.stringify(data));
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
                    link.textContent = decodeURIComponent(parts[i]);
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
                            var currentPath = getCurrentPath();
                            var pageTitle = document.getElementById('pageTitle');
                            if (currentPath === '') {{
                                pageTitle.textContent = 'Home';
                            }} else {{
                                var pathParts = currentPath.split('/');
                                pageTitle.textContent = decodeURIComponent(pathParts[pathParts.length - 1]);
                            }}
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
                    entry.setAttribute('data-path', dir.path);
                    var nameSpan = document.createElement('span');
                    nameSpan.textContent = dir.name + '/';
                    var infoSpan = document.createElement('span');
                    infoSpan.className = 'file-info';
                    var sizeSpan = document.createElement('span');
                    sizeSpan.className = 'folder-size';
                    sizeSpan.textContent = '...';
                    
                    var menuBtn = document.createElement('button');
                    menuBtn.className = 'menu-btn';
                    menuBtn.textContent = '⋮';
                    menuBtn.onclick = function(e) {{
                        e.stopPropagation();
                        e.preventDefault();
                        openContextMenu(e, {{
                            path: dir.path,
                            sha: dir.sha,
                            name: dir.name,
                            type: 'dir'
                        }});
                    }};
                    
                    infoSpan.appendChild(sizeSpan);
                    infoSpan.appendChild(menuBtn);
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
                    
                    var menuBtn = document.createElement('button');
                    menuBtn.className = 'menu-btn';
                    menuBtn.textContent = '⋮';
                    menuBtn.onclick = function(e) {{
                        e.stopPropagation();
                        e.preventDefault();
                        openContextMenu(e, {{
                            path: file.path,
                            sha: file.sha,
                            name: file.name,
                            type: 'file',
                            _fileSize: file.size
                        }});
                    }};
                    
                    infoSpan.appendChild(sizeSpan);
                    infoSpan.appendChild(menuBtn);
                    entry.appendChild(nameSpan);
                    entry.appendChild(infoSpan);
                    container.appendChild(entry);
                }});

                if (dirs.length === 0 && files.length === 0) {{
                    container.innerHTML = '<div class="loading">此目录为空</div>';
                }} else {{
                    calculateFolderSizes(dirs);
                }}
            }}

            var treeCache = null;
            var treeCacheTime = 0;

            function calculateFolderSizes(dirs) {{
                if (dirs.length === 0) return;
                
                var now = Date.now();
                if (treeCache && (now - treeCacheTime) < 300000) {{
                    updateFolderSizeDisplay(treeCache, dirs);
                    return;
                }}
                
                var branchXhr = new XMLHttpRequest();
                branchXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/branches/' + DEFAULT_BRANCH, true);
                branchXhr.onload = function() {{
                    if (branchXhr.status === 200) {{
                        var branchInfo = JSON.parse(branchXhr.responseText);
                        var treeSha = branchInfo.commit.commit.tree.sha;
                        
                        var treeXhr = new XMLHttpRequest();
                        treeXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/git/trees/' + treeSha + '?recursive=1', true);
                        treeXhr.onload = function() {{
                            if (treeXhr.status === 200) {{
                                var treeData = JSON.parse(treeXhr.responseText);
                                if (treeData.tree) {{
                                    treeCache = treeData.tree;
                                    treeCacheTime = Date.now();
                                    updateFolderSizeDisplay(treeData.tree, dirs);
                                }}
                            }}
                        }};
                        treeXhr.send();
                    }}
                }};
                branchXhr.send();
            }}

            function updateFolderSizeDisplay(tree, dirs) {{
                var sizeMap = {{}};
                tree.forEach(function(item) {{
                    if (item.type === 'blob' && item.size) {{
                        var parts = item.path.split('/');
                        if (parts.length > 1) {{
                            var parentDir = parts.slice(0, parts.length - 1).join('/');
                            if (!sizeMap[parentDir]) sizeMap[parentDir] = 0;
                            sizeMap[parentDir] += item.size;
                        }}
                    }}
                }});
                
                dirs.forEach(function(dir) {{
                    var totalSize = 0;
                    tree.forEach(function(item) {{
                        if (item.type === 'blob' && item.size && item.path.indexOf(dir.path + '/') === 0) {{
                            totalSize += item.size;
                        }}
                    }});
                    var span = document.querySelector('.entry[data-path="' + dir.path.replace(/"/g, '\\"') + '"] .folder-size');
                    if (span) {{
                        span.textContent = totalSize > 0 ? formatSize(totalSize) : '0B';
                    }}
                }});
            }}

            function showProperties(filePath, fileName, fileType, fileSha) {{
                var content = document.getElementById('propertiesContent');
                var html = '<table class="prop-table">';
                html += '<tr><td>名称</td><td>' + fileName + '</td></tr>';
                html += '<tr><td>路径</td><td>' + filePath + '</td></tr>';
                html += '<tr><td>类型</td><td>' + (fileType === 'dir' ? '文件夹' : '文件') + '</td></tr>';
                
                if (fileType === 'dir') {{
                    var dirSize = 0;
                    var fileCount = 0;
                    if (treeCache) {{
                        treeCache.forEach(function(item) {{
                            if (item.path.indexOf(filePath + '/') === 0) {{
                                if (item.type === 'blob') {{
                                    dirSize += (item.size || 0);
                                    fileCount++;
                                }}
                            }}
                        }});
                    }}
                    html += '<tr><td>大小</td><td>' + (treeCache ? formatSize(dirSize) : '获取中...') + '</td></tr>';
                    html += '<tr><td>包含</td><td>' + fileCount + ' 个文件</td></tr>';
                }} else {{
                    html += '<tr><td>大小</td><td>' + formatSize(menuFileInfo._fileSize || 0) + '</td></tr>';
                    html += '<tr><td>SHA</td><td style="font-size:12px;">' + (fileSha || '-') + '</td></tr>';
                }}
                
                html += '</table>';
                content.innerHTML = html;
                document.getElementById('propertiesModal').classList.add('show');
            }}

            function closePropertiesModal() {{
                document.getElementById('propertiesModal').classList.remove('show');
            }}

            function deleteFolderItems(key, folderPath) {{
                if (!treeCache) {{
                    showDeleteMessage('正在获取文件列表...', 'success');
                    var branchXhr = new XMLHttpRequest();
                    branchXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/branches/' + DEFAULT_BRANCH, true);
                    branchXhr.onload = function() {{
                        if (branchXhr.status === 200) {{
                            var branchInfo = JSON.parse(branchXhr.responseText);
                            var treeSha = branchInfo.commit.commit.tree.sha;
                            var treeXhr = new XMLHttpRequest();
                            treeXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/git/trees/' + treeSha + '?recursive=1', true);
                            treeXhr.onload = function() {{
                                if (treeXhr.status === 200) {{
                                    var treeData = JSON.parse(treeXhr.responseText);
                                    if (treeData.tree) {{
                                        treeCache = treeData.tree;
                                        treeCacheTime = Date.now();
                                        deleteFolderProcess(key, folderPath, treeData.tree);
                                    }}
                                }} else {{
                                    showDeleteMessage('获取文件列表失败', 'error');
                                    document.getElementById('deleteBtn').disabled = false;
                                }}
                            }};
                            treeXhr.onerror = function() {{
                                showDeleteMessage('网络错误', 'error');
                                document.getElementById('deleteBtn').disabled = false;
                            }};
                            treeXhr.send();
                        }} else {{
                            showDeleteMessage('获取分支信息失败', 'error');
                            document.getElementById('deleteBtn').disabled = false;
                        }}
                    }};
                    branchXhr.onerror = function() {{
                        showDeleteMessage('网络错误', 'error');
                        document.getElementById('deleteBtn').disabled = false;
                    }};
                    branchXhr.send();
                }} else {{
                    deleteFolderProcess(key, folderPath, treeCache);
                }}
            }}

            function deleteFolderProcess(key, folderPath, tree) {{
                var files = [];
                tree.forEach(function(item) {{
                    if (item.type === 'blob' && item.path.indexOf(folderPath + '/') === 0) {{
                        var innerParts = item.path.split('/');
                        var innerName = innerParts[innerParts.length - 1];
                        files.push({{ path: item.path, name: innerName, sha: item.sha }});
                    }}
                }});
                
                if (files.length === 0) {{
                    showDeleteMessage('文件夹为空或不存在', 'error');
                    document.getElementById('deleteBtn').disabled = false;
                    return;
                }}
                
                var total = files.length;
                var completed = 0;
                var failed = 0;
                
                showDeleteMessage('正在删除 ' + total + ' 个文件 (0/' + total + ')...', 'success');
                
                function deleteNext(index) {{
                    if (index >= files.length) {{
                        if (failed === 0) {{
                            showDeleteMessage('删除成功！共删除 ' + completed + ' 个文件', 'success');
                            setTimeout(function() {{
                                closeDeleteModal();
                                treeCache = null;
                                treeCacheTime = 0;
                                loadFileList();
                            }}, 1500);
                        }} else {{
                            showDeleteMessage('删除完成，成功 ' + completed + ' 个，失败 ' + failed + ' 个', 'error');
                            document.getElementById('deleteBtn').disabled = false;
                        }}
                        return;
                    }}
                    
                    var f = files[index];
                    showDeleteMessage('正在删除 (' + (completed + failed + 1) + '/' + total + '): ' + f.name + '...', 'success');
                    
                    var data = {{ message: 'Delete: ' + f.path, sha: f.sha }};
                    var delXhr = new XMLHttpRequest();
                    delXhr.open('DELETE', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(f.path), true);
                    delXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                    delXhr.setRequestHeader('Content-Type', 'application/json');
                    delXhr.onload = function() {{
                        if (delXhr.status === 200) {{
                            completed++;
                        }} else {{
                            failed++;
                        }}
                        deleteNext(index + 1);
                    }};
                    delXhr.onerror = function() {{
                        failed++;
                        deleteNext(index + 1);
                    }};
                    delXhr.send(JSON.stringify(data));
                }}
                
                deleteNext(0);
            }}

            function previewFolder(filePath, fileName) {{
                document.getElementById('previewTitle').textContent = '文件夹: ' + fileName;
                var content = document.getElementById('previewContent');
                content.innerHTML = '<div class="loading">加载中...</div>';
                document.getElementById('previewModal').classList.add('show');
                document.getElementById('previewActions').style.display = 'none';
                document.getElementById('previewMessage').className = 'message';
                document.getElementById('previewMessage').textContent = '';
                
                var apiUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath) + '?ref=' + DEFAULT_BRANCH;
                var xhr = new XMLHttpRequest();
                xhr.open('GET', apiUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        var items = JSON.parse(xhr.responseText);
                        var html = '<div class="folder-preview-list">';
                        var dirs = items.filter(function(i) {{ return i.type === 'dir'; }});
                        var files = items.filter(function(i) {{ return i.type === 'file'; }});
                        dirs.sort(function(a, b) {{ return a.name.localeCompare(b.name); }});
                        files.sort(function(a, b) {{ return a.name.localeCompare(b.name); }});
                        
                        if (dirs.length + files.length === 0) {{
                            html += '<div style="color:#666;text-align:center;padding:20px;">空文件夹</div>';
                        }}
                        
                        dirs.forEach(function(d) {{
                            html += '<div class="folder-preview-item"><span class="fp-icon">&#128193;</span>' + d.name + '/</div>';
                        }});
                        files.forEach(function(f) {{
                            html += '<div class="folder-preview-item"><span class="fp-icon">&#128196;</span>' + f.name + ' <span style="color:#8b949e;font-size:11px;">' + formatSize(f.size) + '</span></div>';
                        }});
                        html += '</div>';
                        content.innerHTML = html;
                    }} else if (xhr.status === 404) {{
                        content.innerHTML = '<div class="message error">文件夹不存在</div>';
                    }} else {{
                        content.innerHTML = '<div class="message error">无法获取文件夹内容</div>';
                    }}
                }};
                xhr.onerror = function() {{
                    content.innerHTML = '<div class="message error">网络错误</div>';
                }};
                xhr.send();
            }}

            function downloadFolderAsZip(folderPath, folderName) {{
                if (typeof JSZip === 'undefined') {{
                    alert('正在加载压缩库，请稍后重试...');
                    return;
                }}
                
                if (!treeCache) {{
                    showDownloadToast('正在获取文件列表...');
                    var branchXhr = new XMLHttpRequest();
                    branchXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/branches/' + DEFAULT_BRANCH, true);
                    branchXhr.onload = function() {{
                        if (branchXhr.status === 200) {{
                            var branchInfo = JSON.parse(branchXhr.responseText);
                            var treeSha = branchInfo.commit.commit.tree.sha;
                            var treeXhr = new XMLHttpRequest();
                            treeXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/git/trees/' + treeSha + '?recursive=1', true);
                            treeXhr.onload = function() {{
                                if (treeXhr.status === 200) {{
                                    var treeData = JSON.parse(treeXhr.responseText);
                                    if (treeData.tree) {{
                                        treeCache = treeData.tree;
                                        treeCacheTime = Date.now();
                                        buildZipAndDownload(folderPath, folderName, treeData.tree);
                                    }}
                                }} else {{
                                    showDownloadToast('获取文件列表失败');
                                }}
                            }};
                            treeXhr.onerror = function() {{ showDownloadToast('网络错误'); }};
                            treeXhr.send();
                        }}
                    }};
                    branchXhr.onerror = function() {{ showDownloadToast('网络错误'); }};
                    branchXhr.send();
                }} else {{
                    buildZipAndDownload(folderPath, folderName, treeCache);
                }}
            }}

            function showDownloadToast(msg) {{
                var toast = document.createElement('div');
                toast.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#1f6feb;color:white;padding:10px 24px;border-radius:8px;z-index:9999;font-size:14px;';
                toast.textContent = msg;
                document.body.appendChild(toast);
                setTimeout(function() {{ document.body.removeChild(toast); }}, 3000);
            }}

            function buildZipAndDownload(folderPath, folderName, tree) {{
                var files = [];
                tree.forEach(function(item) {{
                    if (item.type === 'blob' && item.path.indexOf(folderPath + '/') === 0) {{
                        files.push(item.path);
                    }}
                }});
                
                if (files.length === 0) {{
                    showDownloadToast('文件夹为空');
                    return;
                }}
                
                var zip = new JSZip();
                var baseUrl = 'https://raw.githubusercontent.com/' + REPO_OWNER + '/' + REPO_NAME + '/' + DEFAULT_BRANCH + '/';
                var completed = 0;
                var total = files.length;
                showDownloadToast('正在打包 ' + total + ' 个文件 (0/' + total + ')...');
                
                files.forEach(function(filePath) {{
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', baseUrl + encodeURI(filePath), true);
                    xhr.responseType = 'blob';
                    xhr.onload = function() {{
                        if (xhr.status === 200) {{
                            var innerPath = filePath.substring(folderPath.length + 1);
                            zip.file(innerPath, xhr.response);
                        }}
                        completed++;
                        if (completed < total) {{
                            showDownloadToast('正在打包 (' + completed + '/' + total + ')...');
                        }} else {{
                            showDownloadToast('正在生成压缩包...');
                            zip.generateAsync({{ type: 'blob' }}).then(function(content) {{
                                var url = URL.createObjectURL(content);
                                var a = document.createElement('a');
                                a.href = url;
                                a.download = (folderName || 'download') + '.zip';
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                                showDownloadToast('下载完成！');
                            }});
                        }}
                    }};
                    xhr.onerror = function() {{
                        completed++;
                    }};
                    xhr.send();
                }});
            }}

            var renameInfo = {{}};

            function showRenameModal(filePath, fileName, type) {{
                renameInfo = {{ path: filePath, name: fileName, type: type || 'file' }};
                document.getElementById('renameTitle').textContent = type === 'dir' ? '重命名文件夹' : '重命名文件';
                document.getElementById('renameInput').value = fileName;
                document.getElementById('renameMessage').className = 'message';
                document.getElementById('renameMessage').textContent = '';
                document.getElementById('renameModal').classList.add('show');
            }}

            function closeRenameModal() {{
                document.getElementById('renameModal').classList.remove('show');
                document.getElementById('renameUsername').value = '';
                document.getElementById('renamePassword').value = '';
            }}

            function confirmRename() {{
                var newName = document.getElementById('renameInput').value.trim();
                var username = document.getElementById('renameUsername').value;
                var password = document.getElementById('renamePassword').value;
                var renameBtn = document.getElementById('renameBtn');
                
                if (!newName) {{
                    showRenameMessage('请输入新名称', 'error');
                    return;
                }}
                if (newName === renameInfo.name) {{
                    showRenameMessage('新名称与当前名称相同', 'error');
                    return;
                }}
                if (!username || !password) {{
                    showRenameMessage('请输入用户名和密码', 'error');
                    return;
                }}
                
                renameBtn.disabled = true;
                showRenameMessage('正在获取授权...', 'success');
                
                var params = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password);
                var keyUrl = 'https://api.boring-student.cn/?' + params;
                
                var xhr = new XMLHttpRequest();
                xhr.open('GET', keyUrl, true);
                xhr.onload = function() {{
                    if (xhr.status === 200) {{
                        try {{
                            var response = JSON.parse(xhr.responseText);
                            if (response.success && response.key) {{
                                if (renameInfo.type === 'dir') {{
                                    renameFolderMove(response.key, renameInfo.path, newName);
                                }} else {{
                                    renameFile(response.key, renameInfo.path, newName);
                                }}
                            }} else {{
                                showRenameMessage('获取授权失败', 'error');
                                renameBtn.disabled = false;
                            }}
                        }} catch (e) {{
                            showRenameMessage('解析授权响应失败', 'error');
                            renameBtn.disabled = false;
                        }}
                    }} else {{
                        showRenameMessage('获取授权失败，状态码: ' + xhr.status, 'error');
                        renameBtn.disabled = false;
                    }}
                }};
                xhr.onerror = function() {{
                    showRenameMessage('网络错误', 'error');
                    renameBtn.disabled = false;
                }};
                xhr.send();
            }}

            function showRenameMessage(text, type) {{
                var msg = document.getElementById('renameMessage');
                msg.className = 'message ' + type;
                msg.textContent = text;
            }}

            function renameFile(key, filePath, newName) {{
                var parts = filePath.split('/');
                parts[parts.length - 1] = newName;
                var newPath = parts.join('/');
                
                showRenameMessage('正在获取文件内容...', 'success');
                
                var getXhr = new XMLHttpRequest();
                getXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath) + '?ref=' + DEFAULT_BRANCH, true);
                getXhr.onload = function() {{
                    if (getXhr.status === 200) {{
                        var fileData = JSON.parse(getXhr.responseText);
                        var content = fileData.content;
                        
                        showRenameMessage('正在创建新文件...', 'success');
                        
                        var createUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(newPath);
                        var createData = {{ message: 'Rename: ' + filePath + ' -> ' + newPath, content: content }};
                        
                        var createXhr = new XMLHttpRequest();
                        createXhr.open('PUT', createUrl, true);
                        createXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                        createXhr.setRequestHeader('Content-Type', 'application/json');
                        createXhr.onload = function() {{
                            if (createXhr.status === 201) {{
                                showRenameMessage('正在删除旧文件...', 'success');
                                var delData = {{ message: 'Delete old: ' + filePath, sha: fileData.sha }};
                                var delXhr = new XMLHttpRequest();
                                delXhr.open('DELETE', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(filePath), true);
                                delXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                                delXhr.setRequestHeader('Content-Type', 'application/json');
                                delXhr.onload = function() {{
                                    if (delXhr.status === 200) {{
                                        showRenameMessage('重命名成功！', 'success');
                                        setTimeout(function() {{
                                            closeRenameModal();
                                            loadFileList();
                                        }}, 1500);
                                    }} else {{
                                        showRenameMessage('新文件已创建但旧文件删除失败', 'error');
                                        document.getElementById('renameBtn').disabled = false;
                                    }}
                                }};
                                delXhr.onerror = function() {{
                                    showRenameMessage('新文件已创建但旧文件删除失败(网络错误)', 'error');
                                    document.getElementById('renameBtn').disabled = false;
                                }};
                                delXhr.send(JSON.stringify(delData));
                            }} else {{
                                try {{
                                    var err = JSON.parse(createXhr.responseText);
                                    showRenameMessage('创建新文件失败: ' + (err.message || '未知错误'), 'error');
                                }} catch(e) {{ showRenameMessage('创建新文件失败', 'error'); }}
                                document.getElementById('renameBtn').disabled = false;
                            }}
                        }};
                        createXhr.onerror = function() {{
                            showRenameMessage('网络错误', 'error');
                            document.getElementById('renameBtn').disabled = false;
                        }};
                        createXhr.send(JSON.stringify(createData));
                    }} else {{
                        showRenameMessage('获取文件内容失败', 'error');
                        document.getElementById('renameBtn').disabled = false;
                    }}
                }};
                getXhr.onerror = function() {{
                    showRenameMessage('网络错误', 'error');
                    document.getElementById('renameBtn').disabled = false;
                }};
                getXhr.send();
            }}

            function renameFolderMove(key, folderPath, newName) {{
                if (!treeCache) {{
                    var branchXhr = new XMLHttpRequest();
                    branchXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/branches/' + DEFAULT_BRANCH, true);
                    branchXhr.onload = function() {{
                        if (branchXhr.status === 200) {{
                            var branchInfo = JSON.parse(branchXhr.responseText);
                            var treeSha = branchInfo.commit.commit.tree.sha;
                            var treeXhr = new XMLHttpRequest();
                            treeXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/git/trees/' + treeSha + '?recursive=1', true);
                            treeXhr.onload = function() {{
                                if (treeXhr.status === 200) {{
                                    var treeData = JSON.parse(treeXhr.responseText);
                                    if (treeData.tree) {{
                                        treeCache = treeData.tree;
                                        treeCacheTime = Date.now();
                                        renameFolderProcess(key, folderPath, newName, treeData.tree);
                                    }}
                                }} else {{
                                    showRenameMessage('获取文件列表失败', 'error');
                                    document.getElementById('renameBtn').disabled = false;
                                }}
                            }};
                            treeXhr.onerror = function() {{
                                showRenameMessage('网络错误', 'error');
                                document.getElementById('renameBtn').disabled = false;
                            }};
                            treeXhr.send();
                        }}
                    }};
                    branchXhr.onerror = function() {{
                        showRenameMessage('网络错误', 'error');
                        document.getElementById('renameBtn').disabled = false;
                    }};
                    branchXhr.send();
                }} else {{
                    renameFolderProcess(key, folderPath, newName, treeCache);
                }}
            }}

            function renameFolderProcess(key, folderPath, newName, tree) {{
                var parts = folderPath.split('/');
                parts[parts.length - 1] = newName;
                var newFolderPath = parts.join('/');
                
                var files = [];
                tree.forEach(function(item) {{
                    if (item.type === 'blob' && item.path.indexOf(folderPath + '/') === 0) {{
                        files.push({{
                            oldPath: item.path,
                            newPath: newFolderPath + '/' + item.path.substring(folderPath.length + 1),
                            sha: item.sha
                        }});
                    }}
                }});
                
                if (files.length === 0) {{
                    showRenameMessage('文件夹为空，无需重命名（Git 不追踪空文件夹）', 'error');
                    document.getElementById('renameBtn').disabled = false;
                    return;
                }}
                
                var total = files.length * 2;
                var completed = 0;
                var failed = 0;
                var step = 0;
                
                showRenameMessage('正在复制文件 (' + completed + '/' + total + ')...', 'success');
                
                function processNext() {{
                    if (step === 2 || fileIndex >= files.length) {{
                        if (failed === 0) {{
                            showRenameMessage('重命名成功！', 'success');
                            setTimeout(function() {{
                                closeRenameModal();
                                treeCache = null;
                                treeCacheTime = 0;
                                loadFileList();
                            }}, 1500);
                        }} else {{
                            showRenameMessage('部分完成，成功 ' + (files.length * 2 - failed) + ' 个操作', 'error');
                            document.getElementById('renameBtn').disabled = false;
                        }}
                        return;
                    }}
                    
                    var f = files[fileIndex];
                    var url, data;
                    
                    if (step === 0) {{
                        showRenameMessage('正在复制 (' + (completed + 1) + '/' + total + '): ' + f.oldPath + '...', 'success');
                        var getXhr = new XMLHttpRequest();
                        getXhr.open('GET', 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(f.oldPath) + '?ref=' + DEFAULT_BRANCH, true);
                        getXhr.onload = function() {{
                            if (getXhr.status === 200) {{
                                var fileData = JSON.parse(getXhr.responseText);
                                f.content = fileData.content;
                                step = 1;
                                completed++;
                                processNext();
                            }} else {{
                                failed++;
                                fileIndex++;
                                progressNext();
                            }}
                        }};
                        getXhr.onerror = function() {{
                            failed++;
                            fileIndex++;
                            progressNext();
                        }};
                        getXhr.send();
                        return;
                    }}
                    
                    if (step === 1) {{
                        var createUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(f.newPath);
                        var createData = {{ message: 'Rename folder: ' + folderPath + ' -> ' + newFolderPath, content: f.content }};
                        var createXhr = new XMLHttpRequest();
                        createXhr.open('PUT', createUrl, true);
                        createXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                        createXhr.setRequestHeader('Content-Type', 'application/json');
                        createXhr.onload = function() {{
                            if (createXhr.status === 201) {{
                                completed++;
                                var delUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + encodeURI(f.oldPath);
                                var delData = {{ message: 'Delete old: ' + f.oldPath, sha: f.sha }};
                                var delXhr = new XMLHttpRequest();
                                delXhr.open('DELETE', delUrl, true);
                                delXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                                delXhr.setRequestHeader('Content-Type', 'application/json');
                                delXhr.onload = function() {{
                                    completed++;
                                    if (delXhr.status !== 200) failed++;
                                    fileIndex++;
                                    progressNext();
                                }};
                                delXhr.onerror = function() {{
                                    failed++; completed++;
                                    fileIndex++;
                                    progressNext();
                                }};
                                showRenameMessage('正在删除旧文件 (' + completed + '/' + total + ')...', 'success');
                                delXhr.send(JSON.stringify(delData));
                            }} else {{
                                failed++;
                                fileIndex++;
                                progressNext();
                            }}
                        }};
                        createXhr.onerror = function() {{
                            failed++;
                            fileIndex++;
                            progressNext();
                        }};
                        createXhr.send(JSON.stringify(createData));
                    }}
                }}
                
                function progressNext() {{
                    step = 0;
                    processNext();
                }}
                
                var fileIndex = 0;
                processNext();
            }}

            function uploadFile() {{
                var username = document.getElementById('username').value;
                var password = document.getElementById('password').value;
                var fileInput = document.getElementById('fileInput');
                var folderInput = document.getElementById('folderInput');
                var uploadBtn = document.getElementById('uploadBtn');

                if (!username || !password) {{
                    showMessage('请输入用户名和密码', 'error');
                    return;
                }}

                var allFiles = [];
                if (fileInput.files) {{
                    for (var i = 0; i < fileInput.files.length; i++) {{
                        var f = fileInput.files[i];
                        f._displayPath = f.name;
                        allFiles.push(f);
                    }}
                }}
                if (folderInput.files) {{
                    for (var i = 0; i < folderInput.files.length; i++) {{
                        var f = folderInput.files[i];
                        f._displayPath = f.webkitRelativePath || f.name;
                        allFiles.push(f);
                    }}
                }}
                if (uploadFileList.length > 0) {{
                    allFiles = allFiles.concat(uploadFileList);
                }}

                if (allFiles.length === 0) {{
                    showMessage('请选择要上传的文件', 'error');
                    return;
                }}

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
                                uploadMultipleFiles(response.key, allFiles);
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

            function uploadMultipleFiles(key, fileList) {{
                var total = fileList.length;
                var completed = 0;
                var failed = 0;
                var progressContainer = document.querySelector('.progress-container');
                progressContainer.style.display = 'block';
                
                showMessage('正在上传 (0/' + total + ')...', 'success');
                
                function uploadNext(index) {{
                    if (index >= fileList.length) {{
                        if (failed === 0) {{
                            showMessage('全部上传成功！共 ' + completed + ' 个文件', 'success');
                            setTimeout(function() {{
                                closeUploadModal();
                                loadFileList();
                            }}, 1500);
                        }} else {{
                            showMessage('上传完成：成功 ' + completed + ' 个，失败 ' + failed + ' 个', 'error');
                            document.getElementById('uploadBtn').disabled = false;
                        }}
                        return;
                    }}
                    
                    var file = fileList[index];
                    var displayPath = file._displayPath || file.name;
                    showMessage('正在上传 (' + (index + 1) + '/' + total + '): ' + displayPath + '...', 'success');
                    document.getElementById('progressFill').style.width = Math.round((index / total) * 100) + '%';
                    document.getElementById('progressText').textContent = Math.round((index / total) * 100) + '%';
                    
                    var reader = new FileReader();
                    reader.onload = function(e) {{
                        var base64Content = e.target.result.split(',')[1];
                        var currentPath = getCurrentPath();
                        var filePath = currentPath ? currentPath + '/' + displayPath : displayPath;

                        var data = {{
                            message: 'Upload: ' + displayPath,
                            content: base64Content
                        }};

                        var uploadXhr = new XMLHttpRequest();
                        var uploadUrl = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + filePath;
                        uploadXhr.open('PUT', uploadUrl, true);
                        uploadXhr.setRequestHeader('Authorization', 'Bearer ' + key);
                        uploadXhr.setRequestHeader('Content-Type', 'application/json');
                        uploadXhr.onload = function() {{
                            if (uploadXhr.status === 200 || uploadXhr.status === 201) {{
                                completed++;
                            }} else {{
                                failed++;
                            }}
                            uploadNext(index + 1);
                        }};
                        uploadXhr.onerror = function() {{
                            failed++;
                            uploadNext(index + 1);
                        }};
                        uploadXhr.send(JSON.stringify(data));
                    }};
                    reader.readAsDataURL(file);
                }}
                
                uploadNext(0);
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
                
                var fi = document.getElementById('fileInput');
                if (fi) {{
                    fi.addEventListener('change', function() {{
                        if (fi.files) {{
                            for (var i = 0; i < fi.files.length; i++) {{
                                var f = fi.files[i];
                                f._displayPath = f.name;
                                addToUploadList(f, f.name);
                            }}
                            fi.value = '';
                        }}
                    }});
                }}
                
                var foldi = document.getElementById('folderInput');
                if (foldi) {{
                    foldi.addEventListener('change', function() {{
                        if (foldi.files) {{
                            for (var i = 0; i < foldi.files.length; i++) {{
                                var f = foldi.files[i];
                                f._displayPath = f.webkitRelativePath || f.name;
                                addToUploadList(f, f._displayPath);
                            }}
                            foldi.value = '';
                        }}
                    }});
                }}
            }});
        </script>
    </body>
</html>
"""

def copy_static_files(output_dir):
    static_files = ['favicon.ico', 'CNAME']
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

    with open('404.html', 'r', encoding='utf-8') as f:
        template_404 = f.read()
    html_404 = template_404.format(
        title='404 - 页面未找到',
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        default_branch=DEFAULT_BRANCH
    )
    with open(os.path.join(output_dir, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html_404)

    print(f'Build completed. Storage repo: {REPO_OWNER}/{REPO_NAME}')
