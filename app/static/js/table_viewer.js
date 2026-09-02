/**
 * Interactive Tabular Matrix Controller.
 * Provides client-side dynamic sorting, search filtering, column toggling, and CSV export.
 */
class TableViewer {
    constructor(tableElementId) {
        this.table = document.getElementById(tableElementId);
        this.originalRows = [];
        this.currentRows = [];
        this.sortDirection = 1;
        this.sortColumnIndex = -1;
        this.init();
    }

    init() {
        if (!this.table) return;
        const tbody = this.table.querySelector('tbody');
        if (!tbody) return;
        this.originalRows = Array.from(tbody.querySelectorAll('tr'));
        this.currentRows = [...this.originalRows];

        // Attach header click listeners for sorting
        const headers = this.table.querySelectorAll('th');
        headers.forEach((th, idx) => {
            th.style.cursor = 'pointer';
            th.addEventListener('click', () => this.sortByColumn(idx));
        });
    }

    sortByColumn(colIndex) {
        const tbody = this.table.querySelector('tbody');
        if (!tbody) return;

        if (this.sortColumnIndex === colIndex) {
            this.sortDirection *= -1;
        } else {
            this.sortColumnIndex = colIndex;
            this.sortDirection = 1;
        }

        this.currentRows.sort((rowA, rowB) => {
            const cellA = rowA.children[colIndex]?.innerText.trim() || '';
            const cellB = rowB.children[colIndex]?.innerText.trim() || '';

            const numA = parseFloat(cellA.replace(/[^0-9.-]+/g, ''));
            const numB = parseFloat(cellB.replace(/[^0-9.-]+/g, ''));

            if (!isNaN(numA) && !isNaN(numB)) {
                return (numA - numB) * this.sortDirection;
            }
            return cellA.localeCompare(cellB) * this.sortDirection;
        });

        tbody.innerHTML = '';
        this.currentRows.forEach(r => tbody.appendChild(r));
    }

    filter(query) {
        const q = query.toLowerCase().trim();
        const tbody = this.table.querySelector('tbody');
        if (!tbody) return;

        tbody.innerHTML = '';
        this.currentRows = this.originalRows.filter(row => {
            const text = row.innerText.toLowerCase();
            return text.includes(q);
        });
        this.currentRows.forEach(r => tbody.appendChild(r));
    }
}
window.TableViewer = TableViewer;
