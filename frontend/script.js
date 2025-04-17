document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Ladebalken anzeigen
    document.getElementById('loading').classList.remove('hidden');
    
    const response = await fetch('/create_tcx/', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    
    // Ladebalken verstecken und Fortschritt auf 100% setzen
    document.getElementById('progress-bar').style.width = '100%';
    setTimeout(() => {
        document.getElementById('loading').classList.add('hidden');
    }, 500);

    if (response.ok) {
        document.getElementById('response').innerHTML = `TCX-Datei erstellt! <a href="/static/${result.tcx_file_path}" download class="text-blue-500 hover:underline">Download</a>`;
    } else {
        document.getElementById('response').innerHTML = `Fehler: ${result.message}`;
    }
});
