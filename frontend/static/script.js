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
        const downloadLink = document.getElementById('download-link');
        downloadLink.href = `/static/${result.tcx_file_path}`;  // Korrekte URL zur Datei
        downloadLink.classList.remove('hidden');
        document.getElementById('response').innerHTML = `TCX-Datei erstellt! <a href="${downloadLink.href}" download class="text-blue-500 hover:underline">Download</a>`;
    } else {
        document.getElementById('response').innerHTML = `Fehler: ${result.message}`;
    }
});
