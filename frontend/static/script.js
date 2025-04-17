document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/create_tcx/', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    if (response.ok) {
        document.getElementById('response').innerHTML = `TCX-Datei erstellt! <a href="/static/${result.tcx_file_path}" download class="text-blue-500 hover:underline">Download</a>`;
    } else {
        document.getElementById('response').innerHTML = `Fehler: ${result.message}`;
    }
});
