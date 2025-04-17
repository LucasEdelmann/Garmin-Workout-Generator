document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/create_fit/', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    if (response.ok) {
        document.getElementById('response').innerHTML = `FIT-Datei erstellt! <a href="/static/${result.fit_file_path}" download class="text-blue-500 hover:underline">Download</a>`;
    } else {
        document.getElementById('response').innerHTML = `Fehler: ${result.message}`;
    }
});

