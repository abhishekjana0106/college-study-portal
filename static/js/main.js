// Academix Portal - Client Side JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // 1. Live Global Quick Search Autocomplete
    const searchInput = document.getElementById('global-search-input');
    const searchResults = document.getElementById('quick-search-results');
    let debounceTimer;

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            const query = searchInput.value.trim();

            if (query.length < 2) {
                searchResults.classList.add('hidden');
                searchResults.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/api/quick-search?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        searchResults.innerHTML = '';
                        if (data.length === 0) {
                            searchResults.innerHTML = `
                                <div class="p-3 text-xs text-slate-400 text-center">
                                    No matching study materials found
                                </div>
                            `;
                        } else {
                            data.forEach(item => {
                                const a = document.createElement('a');
                                a.href = `/resource/${item.id}`;
                                a.className = 'block p-3 hover:bg-slate-50 transition-colors';
                                a.innerHTML = `
                                    <div class="flex items-center justify-between text-[11px] mb-0.5">
                                        <span class="font-bold text-blue-600">${item.dept} • ${item.type}</span>
                                        <span class="text-slate-400 font-mono">${item.year}</span>
                                    </div>
                                    <div class="text-xs font-bold text-slate-800 line-clamp-1">${item.title}</div>
                                    <div class="text-[11px] text-slate-500">${item.subject}</div>
                                `;
                                searchResults.appendChild(a);
                            });
                        }
                        searchResults.classList.remove('hidden');
                    })
                    .catch(err => {
                        console.error('Quick search error:', err);
                    });
            }, 250);
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('hidden');
            }
        });
    }

    // 2. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('[role="alert"]');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
