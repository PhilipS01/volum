import * as THREE               from '/static/three-proxy.js';
import { OrbitControls }        from '/static/three-proxy.js';
import { loadSceneFromJSON }    from '/static/scene_loader.js';

const canvas = document.getElementById('three-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene    = new THREE.Scene();
const camera   = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 100);
camera.position.set(3,3,3);

const axesHelper = new THREE.AxesHelper(3);
scene.add(axesHelper);

const gridHelper = new THREE.GridHelper(10, 10);
scene.add(gridHelper);


//document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // optional: for softer shadows

// Helper to remove all meshes from scene
function clearScene() {
  scene.children.slice().forEach(c => scene.remove(c));
  const axesHelper = new THREE.AxesHelper(3);
    scene.add(axesHelper);

    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);
}

// Live-update socket
const ws = new WebSocket(`ws://${location.host}/api/scene/ws`);
ws.onmessage = async ({ data }) => {
    if (data === 'scene_updated') {
        console.log('Scene updated, reloading...');
        const json = await fetch('/api/scene').then(r => r.json()); // TODO: old json when updating
        clearScene();
        console.log('Loaded new scene JSON:', json);
        await loadSceneFromJSON(json, scene);
    }
    if (data === 'volume_updated') {
        const tex = await loadVolumeTexture('/scene/volume', { width, height, depth });
        volumeMesh.material.uniforms.uDataTex.value = tex;
    }
};
ws.onopen  = () => console.log('Live socket open');
ws.onclose = () => console.warn('Live socket closed');

// Initial load
(async function init() {
    const json = await fetch('/api/scene').then(r => r.json());
    await loadSceneFromJSON(json, scene);

    onWindowResize();
    window.addEventListener('resize', onWindowResize);
    animate();
})();

function onWindowResize() {
    camera.aspect = innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}