import * as THREE               from '/static/three-proxy.js';
import { OrbitControls }        from '/static/three-proxy.js';
import { loadSceneFromJSON }    from '/static/scene_loader.js';

const canvas = document.getElementById('three-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene    = new THREE.Scene();
const camera   = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 100);
camera.position.set(3,3,3);

//document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // optional: for softer shadows

// Set up event listeners for UI controls
const checkboxLight = document.getElementById('checkbox-light');
checkboxLight.checked = true;
checkboxLight.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    toggleAllLights(scene, enabled);
    console.log(`Lights ${enabled ? 'enabled' : 'disabled'}`);
});

const checkboxShadows =  document.getElementById('checkbox-shadows');
checkboxShadows.checked = true;
checkboxShadows.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    toggleAllLightShadows(scene, enabled);
    console.log(`Shadows ${enabled ? 'enabled' : 'disabled'}`);
});

const checkboxGrid =  document.getElementById('checkbox-grid');
checkboxGrid.checked = true;
checkboxGrid.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    toggleGridHelper(scene, enabled);
    console.log(`Grid ${enabled ? 'enabled' : 'disabled'}`);
});

const checkboxAxes =  document.getElementById('checkbox-axes');
checkboxAxes.checked = false;
checkboxAxes.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    toggleAxesHelper(scene, enabled);
    console.log(`Axes ${enabled ? 'enabled' : 'disabled'}`);
});

const gridSizeInput = document.getElementById('tb-grid-size');
gridSizeInput.addEventListener('change', (e) => {
    const size = parseFloat(e.target.value);
    if (isNaN(size) || size <= 0) {
        console.warn('Invalid grid size, must be a positive number');
        return;
    }
    let gridHelper = scene.getObjectByName('gridHelper');
    if (!gridHelper) {
        gridHelper = new THREE.GridHelper(size, size);
        gridHelper.name = 'gridHelper';
        scene.add(gridHelper);
    } else {
        gridHelper.dispose(); // remove old grid helper
        scene.remove(gridHelper);
        gridHelper = new THREE.GridHelper(size, size);
        gridHelper.name = 'gridHelper';
        scene.add(gridHelper);
    }
    console.log(`Grid size set to ${size}`);
});


// Helper to remove all meshes from scene
function clearScene() {
    scene.children.slice().forEach(c => scene.remove(c));
}

// Live-update socket
const ws = new WebSocket(`ws://${location.host}/api/scene/ws`);
ws.onmessage = async ({ data }) => {
    if (data === 'scene_updated') {
        console.log('Scene updated, reloading...');
        const json = await fetch('/api/scene').then(r => r.json());
        clearScene();
        await loadSceneFromJSON(json, scene);

        toggleAllLights(scene, checkboxLight.checked);
        toggleAllLightShadows(scene, checkboxShadows.checked);
        toggleGridHelper(scene, checkboxGrid.checked);
        toggleAxesHelper(scene, checkboxAxes.checked);
        console.log('Scene reloaded');
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

    toggleAllLights(scene, checkboxLight.checked); // check for lights
    toggleGridHelper(scene, checkboxGrid.checked); // grid helper
    toggleAxesHelper(scene, checkboxAxes.checked); // axes helper

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


/**
 * Toggles shadow casting for all lights in the scene.
 * @param {THREE.Scene} scene 
 * @param {boolean} enabled 
 */
function toggleAllLightShadows(scene, enabled) {
  scene.traverse(obj => {
    if (obj.isLight && !(obj instanceof THREE.AmbientLight)) {
        obj.castShadow = enabled;
        obj.receiveShadow = enabled;
        obj.shadow.mapSize.width = 2048;
        obj.shadow.mapSize.height = 2048;
        obj.shadow.needsUpdate = true;
    }
  });
}

/**
 * Toggles visibility for all lights in the scene.
 * @param {THREE.Scene} scene 
 * @param {boolean} enabled 
 */
function toggleAllLights(scene, enabled) {
    var light_count = 0;
    scene.traverse(obj => {
        if (obj.isLight && !(obj instanceof THREE.AmbientLight)) {
            obj.visible = enabled;
            light_count++;
        }
    });
    // Enable/disable checkboxes based on light count
    if (light_count === 0) {
        checkboxLight.disabled = true;
        checkboxShadows.disabled = true;
    }
    else {
        checkboxLight.disabled = false;
        checkboxShadows.disabled = false;
    }
}

/**
 * Toggles the visibility of the grid helper.
 * @param {THREE.Scene} scene 
 * @param {boolean} enabled 
 */
function toggleGridHelper(scene, enabled) {
    let gridHelper = scene.getObjectByName('gridHelper');
    if (!gridHelper) {
        gridHelper = new THREE.GridHelper(gridSizeInput.value, gridSizeInput.value);
        gridHelper.name = 'gridHelper';
        scene.add(gridHelper);
    }
    gridHelper.visible = enabled;
}

/**
 * Toggles the visibility of the axes helper.
 * @param {THREE.Scene} scene 
 * @param {boolean} enabled 
 */
function toggleAxesHelper(scene, enabled) {
    let axesHelper = scene.getObjectByName('axesHelper');
    if (!axesHelper) {
        axesHelper = new THREE.AxesHelper(2);
        axesHelper.name = 'axesHelper';
        scene.add(axesHelper);
    }
    axesHelper.visible = enabled;
}