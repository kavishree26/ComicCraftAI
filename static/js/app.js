/* ============================================================
   COMICCRAFT AI - MAIN JAVASCRIPT
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    console.log("ComicCraft AI JavaScript loaded successfully.");

    const form = document.querySelector("form");

    if (!form) {
        return;
    }

    const submitButton =
        form.querySelector('button[type="submit"]');

    /* --------------------------------------------------------
       Create loading message
       -------------------------------------------------------- */

    const loading = document.createElement("div");

    loading.className = "loading";

    loading.textContent =
        "Creating your comic... Please wait.";

    form.appendChild(loading);

    /* --------------------------------------------------------
       Create error message
       -------------------------------------------------------- */

    const errorBox = document.createElement("div");

    errorBox.className = "error";

    form.appendChild(errorBox);

    /* --------------------------------------------------------
       Form submit
       -------------------------------------------------------- */

    form.addEventListener("submit", function () {

        errorBox.classList.remove("active");
        errorBox.textContent = "";

        loading.classList.add("active");

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Generating...";
        }
    });

});


/* ============================================================
   IMAGE ERROR HANDLING
   ============================================================ */

document.addEventListener(
    "error",
    function (event) {

        const element = event.target;

        if (
            element &&
            element.tagName &&
            element.tagName.toLowerCase() === "img"
        ) {
            console.warn(
                "Comic image could not be loaded:",
                element.src
            );

            element.alt = "Image unavailable";
        }
    },
    true
);


/* ============================================================
   DOWNLOAD BUTTONS
   ============================================================ */

document.addEventListener("click", function (event) {

    const button =
        event.target.closest("[data-download]");

    if (!button) {
        return;
    }

    const url = button.getAttribute("data-download");

    if (!url) {
        return;
    }

    const link = document.createElement("a");

    link.href = url;
    link.download = "";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
});


/* ============================================================
   TEST CONNECTION
   ============================================================ */

async function testImageGenerator() {

    try {

        const response =
            await fetch("/test-image");

        if (!response.ok) {
            throw new Error(
                "Image generator test failed."
            );
        }

        const data =
            await response.json();

        console.log(
            "Image generator test:",
            data
        );

        return data;

    } catch (error) {

        console.error(
            "Image generator error:",
            error
        );

        return null;
    }
}