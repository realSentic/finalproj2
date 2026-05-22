document.addEventListener('DOMContentLoaded', () => {
    const csvImportBtn = document.getElementById('csvImportBtn');
    const csvFileInput = document.getElementById('csvFileInput');

    if (csvImportBtn && csvFileInput) {
        csvImportBtn.addEventListener('click', function () {
            csvFileInput.click();
        });

        csvFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                document.getElementById('csvImportForm').submit();
            }
        });
    }
});