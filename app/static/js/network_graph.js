/**
 * Force-Directed Document Similarity Visualizer (Canvas 2D).
 */
class DocumentSimilarityGraph {
    constructor(canvasId, nodes = [], links = []) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.nodes = nodes;
        this.links = links;
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        this.render();
    }

    render() {
        if (!this.ctx) return;
        this.ctx.clearRect(0, 0, this.width, this.height);

        // Draw Links
        this.ctx.strokeStyle = '#cbd5e1';
        this.ctx.lineWidth = 1.5;
        this.links.forEach(l => {
            const src = this.nodes[l.source];
            const tgt = this.nodes[l.target];
            if (src && tgt) {
                this.ctx.beginPath();
                this.ctx.moveTo(src.x, src.y);
                this.ctx.lineTo(tgt.x, tgt.y);
                this.ctx.stroke();
            }
        });

        // Draw Nodes
        this.nodes.forEach(n => {
            this.ctx.beginPath();
            this.ctx.arc(n.x, n.y, n.radius || 12, 0, 2 * Math.PI);
            this.ctx.fillStyle = n.color || '#3b82f6';
            this.ctx.fill();
            this.ctx.strokeStyle = '#ffffff';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            // Label
            this.ctx.font = '11px sans-serif';
            this.ctx.fillStyle = '#1e293b';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(n.label || '', n.x, n.y + 22);
        });
    }
}
window.DocumentSimilarityGraph = DocumentSimilarityGraph;
