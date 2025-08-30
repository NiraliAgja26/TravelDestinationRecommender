document.addEventListener('DOMContentLoaded', function() {
    const favoriteForm = document.getElementById('favorite-form');
    const favoriteBtn = document.getElementById('favorite-btn');
    
    if (favoriteForm && favoriteBtn) {
        favoriteForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Disable button during request
            favoriteBtn.disabled = true;
            const originalText = favoriteBtn.innerHTML;
            favoriteBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> <span class="d-none d-md-inline">Processing...</span>';
            
            const formData = new FormData(favoriteForm);
            const url = favoriteForm.action;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                if (data.is_favorite) {
                    favoriteBtn.className = 'btn btn-danger';
                    favoriteBtn.innerHTML = '<i class="bi bi-heart-fill"></i> <span class="d-none d-md-inline">Favorited</span>';
                    favoriteBtn.title = 'Remove from Favorites';
                } else {
                    favoriteBtn.className = 'btn btn-outline-danger';
                    favoriteBtn.innerHTML = '<i class="bi bi-heart-fill"></i> <span class="d-none d-md-inline">Add to Favorites</span>';
                    favoriteBtn.title = 'Add to Favorites';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                favoriteBtn.innerHTML = originalText;
                alert('An error occurred while updating favorites. Please try again.');
            })
            .finally(() => {
                favoriteBtn.disabled = false;
            });
        });
    }
});