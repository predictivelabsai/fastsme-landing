// Predictive Labs hero — wireframe globe with European city dots + flowing arcs.
// Slow, restrained, dark-first. Capped at 30fps. Respects prefers-reduced-motion.

import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

const TEAL = 0x5eead4;
const TEAL_DIM = 0x134e4a;
const INK_DIM = 0x6b7280;

// European capitals + a few operational cities (lat, lon)
const CITIES = [
  ['London', 51.5074, -0.1278],
  ['Paris', 48.8566, 2.3522],
  ['Berlin', 52.52, 13.405],
  ['Madrid', 40.4168, -3.7038],
  ['Rome', 41.9028, 12.4964],
  ['Amsterdam', 52.3676, 4.9041],
  ['Brussels', 50.8503, 4.3517],
  ['Vienna', 48.2082, 16.3738],
  ['Warsaw', 52.2297, 21.0122],
  ['Copenhagen', 55.6761, 12.5683],
  ['Stockholm', 59.3293, 18.0686],
  ['Helsinki', 60.1699, 24.9384],
  ['Oslo', 59.9139, 10.7522],
  ['Dublin', 53.3498, -6.2603],
  ['Tallinn', 59.437, 24.7536],
  ['Riga', 56.9496, 24.1052],
  ['Vilnius', 54.6872, 25.2797],
  ['Prague', 50.0755, 14.4378],
  ['Lisbon', 38.7223, -9.1393],
  ['Athens', 37.9838, 23.7275],
];

// Which cities connect to which — arcs drawn once, animated in flow
const ARCS = [
  [0, 1], [0, 5], [0, 13], [0, 2], [0, 9],
  [1, 2], [1, 3], [1, 4],
  [2, 7], [2, 8], [2, 17],
  [5, 6], [5, 11],
  [9, 10], [9, 12], [10, 11], [10, 14],
  [11, 15], [15, 16], [16, 8],
  [4, 7], [7, 8], [17, 8],
  [14, 9], [14, 15],
];

function latLonToVec3(lat, lon, r = 1) {
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lon + 180) * Math.PI / 180;
  return new THREE.Vector3(
    -r * Math.sin(phi) * Math.cos(theta),
    r * Math.cos(phi),
    r * Math.sin(phi) * Math.sin(theta),
  );
}

function arc(a, b, lift = 0.25, segments = 48) {
  const start = a.clone();
  const end = b.clone();
  const mid = start.clone().add(end).multiplyScalar(0.5).normalize().multiplyScalar(1 + lift);
  const pts = [];
  for (let i = 0; i <= segments; i++) {
    const t = i / segments;
    // Quadratic Bezier across the sphere
    const p = start.clone().multiplyScalar((1 - t) * (1 - t))
      .add(mid.clone().multiplyScalar(2 * (1 - t) * t))
      .add(end.clone().multiplyScalar(t * t));
    pts.push(p);
  }
  return pts;
}

function init() {
  const container = document.getElementById('three-hero');
  if (!container) return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const width = container.clientWidth;
  const height = container.clientHeight;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
  camera.position.set(0, 0.7, 3.6);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
  renderer.setSize(width, height);
  renderer.setClearColor(0x000000, 0);
  container.appendChild(renderer.domElement);

  const globe = new THREE.Group();
  scene.add(globe);

  // Wireframe sphere
  const sphereGeom = new THREE.SphereGeometry(1, 40, 28);
  const wireMat = new THREE.LineBasicMaterial({ color: INK_DIM, transparent: true, opacity: 0.25 });
  const edges = new THREE.EdgesGeometry(sphereGeom);
  globe.add(new THREE.LineSegments(edges, wireMat));

  // Faint filled sphere to occlude back-facing arcs (subtle depth)
  const fillMat = new THREE.MeshBasicMaterial({ color: 0x0d2a70, transparent: true, opacity: 0.85 });
  globe.add(new THREE.Mesh(sphereGeom, fillMat));

  // City dots
  const cityPositions = CITIES.map(([, lat, lon]) => latLonToVec3(lat, lon, 1.005));
  const dotGeom = new THREE.BufferGeometry().setFromPoints(cityPositions);
  const dotMat = new THREE.PointsMaterial({ color: TEAL, size: 0.035, transparent: true, opacity: 0.9 });
  globe.add(new THREE.Points(dotGeom, dotMat));

  // City halos (pulsing)
  const haloMat = new THREE.PointsMaterial({ color: TEAL, size: 0.09, transparent: true, opacity: 0.15 });
  const halos = new THREE.Points(dotGeom, haloMat);
  globe.add(halos);

  // Arcs
  const arcObjects = [];
  ARCS.forEach(([i, j]) => {
    const pts = arc(cityPositions[i], cityPositions[j]);
    const geom = new THREE.BufferGeometry().setFromPoints(pts);
    const mat = new THREE.LineBasicMaterial({ color: TEAL_DIM, transparent: true, opacity: 0.5 });
    const line = new THREE.Line(geom, mat);
    globe.add(line);
    arcObjects.push({ line, pts, phase: Math.random() * Math.PI * 2 });
  });

  // Traveling pulses along arcs
  const pulseMat = new THREE.PointsMaterial({ color: TEAL, size: 0.05, transparent: true, opacity: 0.95 });
  const pulsePositions = new Float32Array(arcObjects.length * 3);
  const pulseGeom = new THREE.BufferGeometry();
  pulseGeom.setAttribute('position', new THREE.BufferAttribute(pulsePositions, 3));
  globe.add(new THREE.Points(pulseGeom, pulseMat));

  // Tilt to frame Europe nicely
  globe.rotation.x = 0.45;
  globe.rotation.y = -0.6;

  const clock = new THREE.Clock();
  const targetFps = reduced ? 12 : 30;
  const minFrameTime = 1 / targetFps;
  let lastRender = 0;

  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    if (t - lastRender < minFrameTime) return;
    lastRender = t;

    if (!reduced) {
      globe.rotation.y += 0.0014;
    }

    // Halo pulse
    haloMat.opacity = 0.12 + 0.06 * Math.sin(t * 1.2);

    // Move a traveling pulse along each arc
    arcObjects.forEach((a, idx) => {
      const prog = ((t * 0.12) + a.phase) % 1;
      const segIdx = Math.floor(prog * (a.pts.length - 1));
      const p = a.pts[segIdx];
      pulsePositions[idx * 3] = p.x;
      pulsePositions[idx * 3 + 1] = p.y;
      pulsePositions[idx * 3 + 2] = p.z;
    });
    pulseGeom.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener('resize', () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
