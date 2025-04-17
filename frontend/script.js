document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const responseBox = document.getElementById('response');
    responseBox.innerHTML = `
        <div class="flex justify-center items-center space-x-2">
            <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
            <span>FIT-Datei wird erstellt...</span>
        </div>
    `;

    try {
        const response = await fetch('/create_fit', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
        if (response.ok) {
            responseBox.innerHTML = `
                FIT-Datei erstellt! 
                <a href="/static/${result.fit_file_path}" download class="text-blue-500 hover:underline">Download</a>
            `;
        } else {
            responseBox.innerHTML = `Fehler: ${result.message}`;
        }
    } catch (error) {
        responseBox.innerHTML = `Fehler: ${error.message}`;
    }
});
