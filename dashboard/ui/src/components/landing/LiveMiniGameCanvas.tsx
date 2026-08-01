import React, { useEffect, useRef } from 'react';

export const LiveMiniGameCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let time = 0;

    const render = () => {
      time += 0.02;
      const width = canvas.width;
      const height = canvas.height;

      ctx.clearRect(0, 0, width, height);

      // 1. Draw Tactical Grid Backdrop
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
      ctx.lineWidth = 1;
      const gridSize = 24;
      for (let x = 0; x < width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // 2. Active Player Spot (Left)
      const p0X = 90;
      const p0Y = height / 2;

      // Pulse ring around active player
      const pulseRadius = 38 + Math.sin(time * 3) * 4;
      ctx.beginPath();
      ctx.arc(p0X, p0Y, pulseRadius, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.35)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Active Tank Node
      ctx.fillStyle = '#1e1b4b';
      ctx.beginPath();
      ctx.roundRect(p0X - 45, p0Y - 32, 90, 64, 8);
      ctx.fill();
      ctx.strokeStyle = '#6366f1';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Bellibolt ex', p0X, p0Y - 8);

      ctx.fillStyle = '#10b981';
      ctx.font = '9px monospace';
      ctx.fillText('HP 350/350', p0X, p0Y + 8);
      ctx.fillStyle = '#f59e0b';
      ctx.fillText('2x Energy (⚡⚡)', p0X, p0Y + 20);

      // 3. Opponent Spot (Right)
      const p1X = width - 90;
      const p1Y = height / 2;

      ctx.fillStyle = '#311018';
      ctx.beginPath();
      ctx.roundRect(p1X - 45, p1Y - 32, 90, 64, 8);
      ctx.fill();
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText('Target Basic', p1X, p1Y - 8);

      ctx.fillStyle = '#f43f5e';
      ctx.font = '9px monospace';
      ctx.fillText('HP 120/120', p1X, p1Y + 8);
      ctx.fillStyle = '#94a3b8';
      ctx.fillText('P(Gust) 37%', p1X, p1Y + 20);

      // 4. Combat Trajectory & Energy Flow
      ctx.beginPath();
      ctx.moveTo(p0X + 45, p0Y);
      const cpX = (p0X + p1X) / 2;
      const cpY = p0Y - 30 + Math.sin(time * 4) * 15;
      ctx.quadraticCurveTo(cpX, cpY, p1X - 45, p1Y);
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Traveling Energy Particle
      const tNorm = (time * 0.8) % 1;
      const partX = (1 - tNorm) * (1 - tNorm) * (p0X + 45) + 2 * (1 - tNorm) * tNorm * cpX + tNorm * tNorm * (p1X - 45);
      const partY = (1 - tNorm) * (1 - tNorm) * p0Y + 2 * (1 - tNorm) * tNorm * cpY + tNorm * tNorm * p1Y;

      ctx.beginPath();
      ctx.arc(partX, partY, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#fbbf24';
      ctx.shadowColor = '#f59e0b';
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.shadowBlur = 0;

      // 5. Lookahead Decision Tree Branches
      const branchNodes = [
        { label: 'Attack A [Lethal KO]', val: '+4250', color: '#10b981', yOff: -65, chosen: true },
        { label: 'Attach Energy', val: '+1800', color: '#6366f1', yOff: 0, chosen: false },
        { label: 'Pass Turn', val: '-1200', color: '#f43f5e', yOff: 65, chosen: false },
      ];

      branchNodes.forEach((node) => {
        const nodeX = (p0X + p1X) / 2;
        const nodeY = height / 2 + node.yOff;

        // Connecting line
        ctx.beginPath();
        ctx.moveTo(p0X + 45, p0Y);
        ctx.lineTo(nodeX - 55, nodeY);
        ctx.strokeStyle = node.chosen ? 'rgba(16, 185, 129, 0.7)' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = node.chosen ? 2 : 1;
        ctx.stroke();

        // Node Box
        ctx.fillStyle = node.chosen ? 'rgba(16, 185, 129, 0.15)' : 'rgba(17, 24, 39, 0.8)';
        ctx.beginPath();
        ctx.roundRect(nodeX - 55, nodeY - 14, 110, 28, 4);
        ctx.fill();
        ctx.strokeStyle = node.chosen ? '#10b981' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 9px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(node.label, nodeX - 50, nodeY + 3);

        ctx.fillStyle = node.color;
        ctx.textAlign = 'right';
        ctx.font = 'bold 9px monospace';
        ctx.fillText(node.val, nodeX + 50, nodeY + 3);
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="w-full h-full min-h-75 flex items-center justify-center relative overflow-hidden rounded-xl bg-[#060a14] border border-white/8 shadow-2xl">
      <canvas
        ref={canvasRef}
        width={560}
        height={320}
        className="w-full h-full object-contain"
      />
      <div className="absolute top-3 left-3 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
        <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
          Live Game-State & 2-Ply Lookahead Simulator
        </span>
      </div>
    </div>
  );
};
