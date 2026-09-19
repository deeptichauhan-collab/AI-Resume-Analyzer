```javascript
document.addEventListener("DOMContentLoaded", function () {

    const resumeInput = document.querySelector(
        'input[name="resume"]'
    );

    const form = document.querySelector("form");

    const submitBtn = document.querySelector(
        'button[type="submit"]'
    );

    // File Validation

    if (resumeInput) {

        resumeInput.addEventListener("change", function () {

            const file = this.files[0];

            if (!file) return;

            const allowedTypes = [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ];

            if (!allowedTypes.includes(file.type)) {

                alert(
                    "Please upload only PDF or DOCX files."
                );

                this.value = "";

                return;
            }

            console.log(
                "Selected File:",
                file.name
            );
        });

    }

    // Loading Animation

    if (form && submitBtn) {

        form.addEventListener("submit", function () {

            submitBtn.disabled = true;

            submitBtn.innerHTML =
                "Analyzing Resume...";

        });

    }

});
```
