window.addEventListener('DOMContentLoaded', function() {

    // ── Modal Elements ──────────────────────────────────
    var modal     = document.getElementById('cf-modal');
    var closeBtn  = document.getElementById('cf-close');
    var modalImg  = document.getElementById('cf-img');
    var modalName = document.getElementById('cf-name');
    var modalCat  = document.getElementById('cf-cat');
    var modalDesc = document.getElementById('cf-desc');
    var modalPrice= document.getElementById('cf-price');
    var modalBuy  = document.getElementById('cf-buy');
    var thumbs    = document.getElementById('cf-thumbs');

    if (!modal) return;

    // ── Close modal ──────────────────────────────────────
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Close button
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeModal();
        });
    }

    // Click outside modal box
    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });

    // ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeModal();
    });

    // ── Open modal ───────────────────────────────────────
    function openModal(id) {
        var nameEl  = document.getElementById('pname-'  + id);
        var catEl   = document.getElementById('pcat-'   + id);
        var descEl  = document.getElementById('pdesc-'  + id);
        var priceEl = document.getElementById('pprice-' + id);
        var imgEl   = document.getElementById('pimg-'   + id);
        var imgsEl  = document.getElementById('pimgs-'  + id);

        if (!nameEl) return;

        var name  = nameEl.innerText.trim();
        var cat   = catEl.innerText.trim();
        var desc  = descEl.innerText.trim();
        var price = priceEl.innerText.trim();
        var img   = imgEl.innerText.trim();
        var imgs  = imgsEl.innerText.trim();

        // Populate modal fields
        modalName.innerText  = name;
        modalCat.innerText   = cat;
        modalDesc.innerText  = desc;
        modalPrice.innerText = price;
        modalImg.src         = img;
        modalBuy.href        = '/add_to_cart/' + id;

        // Build thumbnails
        thumbs.innerHTML = '';
        var imgList = imgs.split(',').filter(function(x) {
            return x.trim().length > 0;
        });

        if (imgList.length > 1) {
            imgList.forEach(function(src, i) {
                var t = document.createElement('img');
                t.src = src.trim();
                t.style.cssText =
                    'width:50px; height:50px; object-fit:cover;' +
                    'object-position:center; cursor:pointer;' +
                    'border:2px solid ' +
                    (i === 0 ? '#c8a96e' : 'transparent') + ';';
                t.addEventListener('click', function() {
                    modalImg.src = this.src;
                    thumbs.querySelectorAll('img').forEach(function(x) {
                        x.style.borderColor = 'transparent';
                    });
                    this.style.borderColor = '#c8a96e';
                });
                thumbs.appendChild(t);
            });
            thumbs.style.display = 'flex';
        } else {
            thumbs.style.display = 'none';
        }

        // Show modal
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    // ── Attach VIEW DETAILS buttons ──────────────────────
    var buttons = document.querySelectorAll('[id^="btn-"]');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            var id = this.id.replace('btn-', '');
            openModal(id);
        });
    });

});