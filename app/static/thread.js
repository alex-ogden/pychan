function showQuotedPost() {
    const quote = this;
    const parentParagraphId = quote.parentNode.id;
    const quotePreviewId = parentParagraphId.replace("-text", "-quotepreview");
    const quotePreviewImageId = parentParagraphId.replace("-text", "-quoteimage");
    const quotePreview = document.getElementById(quotePreviewId);
    const quotePreviewImage = document.getElementById(quotePreviewImageId);
    const quotedPostNum = quote.textContent.replace(">>", "");
    const quotedText = document.getElementById(`${quotedPostNum}-text`);
    const quotedImage = document.getElementById(quotedPostNum);
    const previewDivId = parentParagraphId.replace("-text", "-post-preview");
    const previewDiv = document.getElementById(previewDivId);

    if (quote.classList.contains("expanded")) {
        previewDiv.removeAttribute("style");
        previewDiv.style.display = "none";
        quotePreview.removeAttribute("style");
        quote.classList.remove("expanded");
        if (quotedImage) {
            quotePreviewImage.src = "//:0";
            quotePreviewImage.removeAttribute("style");
        }
    } else {
        previewDiv.removeAttribute("style");
        previewDiv.style.border = "1px solid black";
        previewDiv.style.backgroundColor = "#363636";
        previewDiv.style.boxShadow = "2px 2px 4px rgba(0, 0, 0, 0.5)";

        if (quotedImage) {
            quotePreviewImage.removeAttribute("style");
            quotePreviewImage.src = quotedImage.src;
            quotePreviewImage.style.padding = "20px";
            quotePreviewImage.style.display = "inline";
            quotePreviewImage.style.boxShadow = "none";
        }

        quotePreview.innerHTML = quotedText.innerHTML;
        quotePreview.style.display = "inline-block";
        quotePreview.style.padding = "20px";

        quote.classList.add("expanded");
    }
}

const quotes = document.querySelectorAll(".quotelink");
for (const quote of quotes) {
    quote.removeAttribute("href");
    quote.addEventListener("click", showQuotedPost);
}
