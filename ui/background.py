"""
UPSC Neuro-OS Neural Background
================================
HTML5 Canvas particle animation for cyberpunk aesthetic.
Creates an animated neural network background effect.

Author: Senior Python Software Architect
Date: November 29, 2025
"""

import streamlit as st


def render_neural_background() -> None:
    """
    Inject HTML5 Canvas particle animation as background.
    
    Creates an animated neural network with particles and connections.
    Uses z-index: -1 to keep it behind all content.
    
    Features:
    - Floating particles with random motion
    - Dynamic connections between nearby particles
    - Neon green/cyan color scheme
    - Responsive to window size
    - Low performance impact
    
    Examples:
        >>> from ui.background import render_neural_background
        >>> render_neural_background()  # Call once at app start
    """
    
    background_html = """
    <style>
    #neural-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        opacity: 0.4;
    }
    </style>
    
    <canvas id="neural-bg"></canvas>
    
    <script>
    (function() {
        // Get canvas and context
        const canvas = document.getElementById('neural-bg');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        // Particle class
        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.radius = Math.random() * 2 + 1;
                
                // Neon colors (green, cyan, purple)
                const colors = [
                    'rgba(57, 255, 20, 0.8)',   // Neon green
                    'rgba(0, 240, 255, 0.8)',   // Cyber cyan
                    'rgba(191, 0, 255, 0.6)'    // Electric purple
                ];
                this.color = colors[Math.floor(Math.random() * colors.length)];
            }
            
            update() {
                this.x += this.vx;
                this.y += this.vy;
                
                // Bounce off edges
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                
                // Keep within bounds
                this.x = Math.max(0, Math.min(canvas.width, this.x));
                this.y = Math.max(0, Math.min(canvas.height, this.y));
            }
            
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
                
                // Add glow effect
                ctx.shadowBlur = 15;
                ctx.shadowColor = this.color;
                ctx.fill();
                ctx.shadowBlur = 0;
            }
        }
        
        // Create particles
        const particleCount = Math.min(100, Math.floor((canvas.width * canvas.height) / 15000));
        const particles = [];
        
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
        
        // Draw connections between nearby particles
        function drawConnections() {
            const maxDistance = 150;
            
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < maxDistance) {
                        const opacity = (1 - distance / maxDistance) * 0.3;
                        
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        
                        // Gradient line (green to cyan)
                        const gradient = ctx.createLinearGradient(
                            particles[i].x, particles[i].y,
                            particles[j].x, particles[j].y
                        );
                        gradient.addColorStop(0, `rgba(57, 255, 20, ${opacity})`);
                        gradient.addColorStop(1, `rgba(0, 240, 255, ${opacity})`);
                        
                        ctx.strokeStyle = gradient;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }
        }
        
        // Animation loop
        function animate() {
            // Clear canvas with slight trail effect
            ctx.fillStyle = 'rgba(15, 23, 42, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Update and draw particles
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });
            
            // Draw connections
            drawConnections();
            
            requestAnimationFrame(animate);
        }
        
        // Start animation
        animate();
        
        // Prevent memory leaks on page unload
        window.addEventListener('beforeunload', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });
    })();
    </script>
    """
    
    st.markdown(background_html, unsafe_allow_html=True)


def render_grid_background() -> None:
    """
    Alternative background: Cyberpunk grid with scanlines.
    
    Creates a retro-futuristic grid background with animated scanlines.
    Less resource-intensive than particle animation.
    
    Examples:
        >>> from ui.background import render_grid_background
        >>> render_grid_background()
    """
    
    grid_html = """
    <style>
    .cyber-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        opacity: 0.5;
    }
    
    .cyber-grid::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            180deg,
            transparent 0%,
            rgba(57, 255, 20, 0.05) 50%,
            transparent 100%
        );
        animation: scanline 4s linear infinite;
    }
    
    @keyframes scanline {
        0% {
            transform: translateY(-100%);
        }
        100% {
            transform: translateY(100%);
        }
    }
    </style>
    
    <div class="cyber-grid"></div>
    """
    
    st.markdown(grid_html, unsafe_allow_html=True)


def render_gradient_orbs() -> None:
    """
    Alternative background: Floating gradient orbs.
    
    Creates smooth animated gradient orbs for a modern aesthetic.
    Very lightweight performance-wise.
    
    Examples:
        >>> from ui.background import render_gradient_orbs
        >>> render_gradient_orbs()
    """
    
    orbs_html = """
    <style>
    .orbs-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.3;
        animation: float 20s ease-in-out infinite;
    }
    
    .orb-1 {
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(57, 255, 20, 0.4), transparent);
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .orb-2 {
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.3), transparent);
        top: 50%;
        right: 10%;
        animation-delay: 5s;
    }
    
    .orb-3 {
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(191, 0, 255, 0.3), transparent);
        bottom: 10%;
        left: 50%;
        animation-delay: 10s;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        33% {
            transform: translate(30px, -30px) scale(1.1);
        }
        66% {
            transform: translate(-20px, 20px) scale(0.9);
        }
    }
    </style>
    
    <div class="orbs-container">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>
    """
    
    st.markdown(orbs_html, unsafe_allow_html=True)


# Export all background functions
__all__ = [
    'render_neural_background',
    'render_grid_background',
    'render_gradient_orbs'
]
