document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('file-upload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/create_fit', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            document.getElementById('response').innerHTML = `❌ Fehler: ${errorText}`;
            return;
        }

        // Blob für FIT-Datei erhalten
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'workout.fit';
        a.click();

        document.getElementById('response').innerHTML = `✅ FIT-Datei wurde erfolgreich erstellt und heruntergeladen.`;

    } catch (error) {
        document.getElementById('response').innerHTML = `❌ Upload-Fehler: ${error.message}`;
    }
});
