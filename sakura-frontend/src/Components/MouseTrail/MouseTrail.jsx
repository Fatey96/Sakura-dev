import React, { useEffect, useRef } from 'react';
import { Box, useColorMode } from '@chakra-ui/react';

const GRID_SIZE = 50; // Distance between static points
const HOVER_RADIUS = 150; // Radius of hover effect
const CONNECTION_DISTANCE = 80; // Maximum distance for connections
const MAX_CONNECTIONS = 3; // Maximum connections per point

class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.baseAlpha = 0.1; // Base visibility
    this.alpha = this.baseAlpha;
    this.connections = 0;
  }

  updateAlpha(mouseX, mouseY) {
    const dx = this.x - mouseX;
    const dy = this.y - mouseY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    // Illuminate points near mouse
    if (distance < HOVER_RADIUS) {
      this.alpha = this.baseAlpha + (0.5 * (1 - distance / HOVER_RADIUS));
    } else {
      this.alpha = this.baseAlpha;
    }
  }

  resetConnections() {
    this.connections = 0;
  }
}

export const MouseTrail = () => {
  const canvasRef = useRef(null);
  const pointsRef = useRef([]);
  const mouseRef = useRef({ x: 0, y: 0 });
  const animationFrameRef = useRef();
  const { colorMode } = useColorMode();

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Initialize grid of points
    const initializePoints = () => {
      pointsRef.current = [];
      const cols = Math.ceil(window.innerWidth / GRID_SIZE);
      const rows = Math.ceil(window.innerHeight / GRID_SIZE);

      for (let i = 0; i <= cols; i++) {
        for (let j = 0; j <= rows; j++) {
          // Add some randomness to point positions
          const randomOffset = GRID_SIZE * 0.2;
          const x = i * GRID_SIZE + (Math.random() * randomOffset - randomOffset/2);
          const y = j * GRID_SIZE + (Math.random() * randomOffset - randomOffset/2);
          pointsRef.current.push(new Point(x, y));
        }
      }
    };

    const handleMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      mouseRef.current = {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      };
    };

    const handleResize = () => {
      canvas.width = window.innerWidth * window.devicePixelRatio;
      canvas.height = window.innerHeight * window.devicePixelRatio;
      canvas.style.width = `${window.innerWidth}px`;
      canvas.style.height = `${window.innerHeight}px`;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      initializePoints();
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update point alphas based on mouse position
      pointsRef.current.forEach(point => {
        point.updateAlpha(mouseRef.current.x, mouseRef.current.y);
        point.resetConnections();
      });

      // Draw connections and points
      for (let i = 0; i < pointsRef.current.length; i++) {
        const pointA = pointsRef.current[i];

        // Find and sort nearby points
        const connections = [];
        for (let j = i + 1; j < pointsRef.current.length; j++) {
          const pointB = pointsRef.current[j];
          const dx = pointB.x - pointA.x;
          const dy = pointB.y - pointA.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < CONNECTION_DISTANCE) {
            connections.push({ point: pointB, distance });
          }
        }

        // Draw closest connections
        connections
          .sort((a, b) => a.distance - b.distance)
          .slice(0, MAX_CONNECTIONS)
          .forEach(({ point: pointB, distance }) => {
            if (pointB.connections < MAX_CONNECTIONS) {
              const alpha = Math.min(pointA.alpha, pointB.alpha) * 
                           (1 - distance / CONNECTION_DISTANCE);
              ctx.strokeStyle = colorMode === 'dark'
                ? `rgba(233, 57, 175, ${alpha * 0.3})`
                : `rgba(233, 57, 175, ${alpha * 0.2})`;
              ctx.lineWidth = 1;
              ctx.beginPath();
              ctx.moveTo(pointA.x, pointA.y);
              ctx.lineTo(pointB.x, pointB.y);
              ctx.stroke();

              pointA.connections++;
              pointB.connections++;
            }
          });

        // Draw point
        ctx.fillStyle = colorMode === 'dark'
          ? `rgba(233, 57, 175, ${pointA.alpha * 0.4})`
          : `rgba(233, 57, 175, ${pointA.alpha * 0.3})`;
        ctx.beginPath();
        ctx.arc(pointA.x, pointA.y, 1.5, 0, Math.PI * 2);
        ctx.fill();
      }

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    handleResize();
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', handleResize);
    animationFrameRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [colorMode]);

  return (
    <Box
      as="canvas"
      ref={canvasRef}
      position="fixed"
      top={0}
      left={0}
      right={0}
      bottom={0}
      pointerEvents="none"
      zIndex={2}
      sx={{
        mixBlendMode: 'screen'
      }}
    />
  );
}; 