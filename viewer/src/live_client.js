import * as THREE               from '/static/three-proxy.js';
import { PointerLockControls }  from '/static/three-proxy.js';
import { OrbitControls }        from '/static/three-proxy.js';
import { loadSceneFromJSON }    from '/static/scene_loader.js';
import { RoomEnvironment }      from '/static/three-proxy.js';
import { RGBELoader }           from '/static/three-proxy.js';
import { indoorEnv, outdoorEnv }from '/static/assets/index.js';

const canvas = document.getElementById('three-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene    = new THREE.Scene();
const camera   = new THREE.PerspectiveCamera(60, innerWidth/innerHeight);
camera.position.set(0,10,10);
camera.lookAt(0, 0, 0);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // optional: for softer shadows

let controls = null;
let orbitControls = null;
let pointerControls = null;

const move = { forward: false, backward: false, left: false, right: false, up: false, down: false };
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();

function applyEnvironmentMap(tex) {
    scene.environment = tex;
    //scene.background = tex; // optional

    scene.traverse((child) => {
        if (child.isMesh && child.material && 'envMap' in child.material) {
            child.material.envMap = tex;
            child.material.needsUpdate = true;
        }
    });
    console.log('Environment loaded');
}

function removeEnvironmentMap() {
    scene.environment = null;
    scene.background = null; // optional, if you want to clear the background
    
    scene.traverse((child) => {
        if (child.isMesh && child.material && 'envMap' in child.material) {
            child.material.envMap = null;
            child.material.needsUpdate = true;
        }
    });
    console.log('Environment map removed');
}

function loadUserEnvironment(url) {
    if (url.endsWith('.hdr')) {
        console.log('Loading HDR environment:', url);
    } else if (url.endsWith('.exr')) {
        console.log('Loading EXR environment:', url);
    } else {
        console.warn('Unsupported environment format:', url);
    }
    const loader = new RGBELoader();
    loader.load(url, (hdrTexture) => {
        hdrTexture.mapping = THREE.EquirectangularReflectionMapping;

        applyEnvironmentMap(hdrTexture);
    });
}

// Set up event listeners for UI controls
const checkboxLight = document.getElementById('checkbox-light');
checkboxLight.checked = true;
checkboxLight.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    toggleAllLights(scene, enabled);
    console.log(`Lights ${enabled ? 'enabled' : 'disabled'}`);
});

const checkboxShadows =  document.getElementById('checkbox-shadows');
checkboxShadows.checked = false;
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

scene.background = new THREE.Color(0x444444); // Default gray background

const gridSizeInput = document.getElementById('tb-grid-size');
gridSizeInput.value = 10;
gridSizeInput.addEventListener('change', (e) => {
    const size = parseFloat(e.target.value);
    if (isNaN(size) || size <= 0) {
        console.warn('Invalid grid size, must be a positive number');
        return;
    }
    let gridHelper = scene.getObjectByName('gridHelper');
    if (gridHelper) {
        gridHelper.dispose(); // remove old grid helper
        scene.remove(gridHelper);
    }
    
    if (scene.background && scene.background.getHex() === 0x444444) {
        gridHelper = new THREE.GridHelper(gridSizeInput.value, gridSizeInput.value, 0xbcbcbc);
    } else {
        gridHelper = new THREE.GridHelper(gridSizeInput.value, gridSizeInput.value, 0x444444); // Default size
    }
    gridHelper.name = 'gridHelper';
    scene.add(gridHelper);
    
    console.log(`Grid size set to ${size}`);
});

const bgColorInput = document.getElementById('select-color');
bgColorInput.value = '0x444444'; // Default gray color
bgColorInput.addEventListener('change', (e) => {
    const color = parseInt(e.target.value, 16); // Convert hex string to number
    scene.background = new THREE.Color(color);
    console.log(`Background color set to ${e.target.value}`);
});

const preset_envs = {
    'indoor': indoorEnv,
    'outdoor': outdoorEnv
};

function setEnvironment(env_value) {
    switch (env_value) {
        case 'room':
            renderer.useLegacyLights = true;
            renderer.toneMapping = THREE.ReinhardToneMapping;
            renderer.toneMappingExposure = 1.0;

            const pmrem = new THREE.PMREMGenerator(renderer);
            const envMap = pmrem.fromScene(new RoomEnvironment()).texture;
            applyEnvironmentMap(envMap);
            pmrem.dispose();
            break;
        case 'custom':
            fileEnvHidden.click(); // trigger hidden file input
            return; // reset until file is selected
        case 'indoor':
        case 'outdoor':
            // Use preset environment
            renderer.useLegacyLights = false;
            renderer.toneMapping = THREE.ACESFilmicToneMapping; // reset to no tone mapping
            renderer.toneMappingExposure = 1.0;
            loadUserEnvironment(preset_envs[env_value]);
            break;
        default:
            // Custom HDR/EXR environment
            renderer.useLegacyLights = false; // disable legacy lights
            renderer.toneMapping = THREE.ACESFilmicToneMapping; // reset to no tone mapping
            renderer.toneMappingExposure = 1.0;
            loadUserEnvironment(env_value);
            break;
    }
}

const selectEnv = document.getElementById('select-env');
selectEnv.addEventListener('change', (e) => {
    if (e.target.value === 'custom') {
        fileEnvHidden.click(); // trigger file dialog
        // file handler will set the environment
        return;
    }
    setEnvironment(e.target.value);
});

const checkboxEnv = document.getElementById('checkbox-env');
checkboxEnv.checked = false;
checkboxEnv.addEventListener('change', (e) => {
    const enabled = e.target.checked;
    if (enabled) {
        setEnvironment(selectEnv.value);
        console.log('Environment map enabled');
    } else {
        setEnvironment('room'); // reset to default environment
        removeEnvironmentMap();
        const color = parseInt(bgColorInput.value, 16); // Convert hex string to number
        scene.background = new THREE.Color(color);
        renderer.toneMapping = THREE.NoToneMapping
        console.log('Environment map disabled');
    }
});

const fileEnvHidden = document.getElementById('file-env-hidden');
fileEnvHidden.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    const fileName = e.target.files[0].name;
    const fileUrl = URL.createObjectURL(e.target.files[0]);

    // Remove existing custom file option (but keep the "Custom..." option)
    const existingCustomFile = Array.from(selectEnv.options).find(opt => 
        opt.value.startsWith('custom-') && opt.value !== 'custom'
    );
    if (existingCustomFile) {
        existingCustomFile.remove();
    }
    
    // Add new option with file name (insert before "Custom..." option)
    const customOption = Array.from(selectEnv.options).find(opt => opt.value === 'custom');
    const newOption = new Option(fileName, fileUrl);
    selectEnv.insertBefore(newOption, customOption);
    selectEnv.value = fileUrl;
    
    console.log('Loading custom environment:', fileName);
    loadUserEnvironment(fileUrl);
  }
});

const checkboxOrbit =  document.getElementById('checkbox-orbit');
checkboxOrbit.checked = true; // default to orbit controls
const checkboxFirstPerson =  document.getElementById('checkbox-firstperson');
checkboxFirstPerson.checked = false; // default to orbit controls

checkboxOrbit.addEventListener('change', () => {
    if (checkboxOrbit.checked) {
        checkboxFirstPerson.checked = false;
        enableOrbitControls();
    } else if (!checkboxFirstPerson.checked) {
        checkboxOrbit.checked = true; // prevent both from being unchecked
    }
});

checkboxFirstPerson.addEventListener('change', () => {
    if (checkboxFirstPerson.checked) {
        checkboxOrbit.checked = false;
        enableFirstPersonControls();
    } else if (!checkboxOrbit.checked) {
        checkboxFirstPerson.checked = true; // prevent both from being unchecked
    }
});

function handleCanvasClick() {
    if (controls && controls.lock) {
        controls.lock();
    }
}

function enableOrbitControls() {
    canvas.removeEventListener('click', handleCanvasClick);
    if (pointerControls) {
        scene.remove(pointerControls.getObject());
    }

    orbitControls = new OrbitControls(camera, renderer.domElement);
    orbitControls.enableDamping = true;
    orbitControls.dampingFactor = 0.12;
    controls = orbitControls;
    console.log('Orbit controls enabled');
}

function enableFirstPersonControls() {
    if (orbitControls && orbitControls.dispose) {
        orbitControls.dispose();
    }

    pointerControls = new PointerLockControls(camera, renderer.domElement);
    controls = pointerControls;
    scene.add(pointerControls.getObject());

    canvas.addEventListener('click', handleCanvasClick);

    setupFirstPersonControls();
    console.log('First-person controls enabled');
}


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
    toggleAllLightShadows(scene, checkboxShadows.checked); // shadows
    toggleGridHelper(scene, checkboxGrid.checked); // grid helper
    toggleAxesHelper(scene, checkboxAxes.checked); // axes helper
    enableOrbitControls(); // default controls

    onWindowResize();
    window.addEventListener('resize', onWindowResize);
    animate();
})();

function onWindowResize() {
    camera.aspect = innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
}

const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    if (controls != null && controls instanceof PointerLockControls && controls.isLocked) {
        const delta = clock.getDelta();
        velocity.set(0, 0, 0);

        direction.z = Number(move.forward) - Number(move.backward);
        direction.x = Number(move.right) - Number(move.left);
        direction.normalize();

        const speed = 1000.0;
        const deltaSpeed = speed * delta;

        velocity.x -= direction.x * deltaSpeed;
        velocity.z -= direction.z * deltaSpeed;

        if (move.up) velocity.y += deltaSpeed;
        if (move.down) velocity.y -= deltaSpeed;

        controls.moveRight(-velocity.x * delta);
        controls.moveForward(-velocity.z * delta);
        controls.getObject().position.y += velocity.y * delta;
    } else if (controls != null && controls instanceof OrbitControls) {
        controls.update(); // for enabled damping
    }

    // scale axes helper based on camera distance
    let axesHelper = scene.getObjectByName('axesHelper');
    if (axesHelper) {
        axesHelper.scale.setScalar(camera.position.length() / 30);
    }

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
        if (scene.background && scene.background.getHex() === 0x444444) {
            gridHelper = new THREE.GridHelper(gridSizeInput.value, gridSizeInput.value, 0xbcbcbc);
        } else {
            gridHelper = new THREE.GridHelper(gridSizeInput.value, gridSizeInput.value, 0x444444); // Default size
        }
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

function setupFirstPersonControls() {
    document.addEventListener('keydown', (event) => {
      switch (event.code) {
        case 'KeyW': move.forward = true; break;
        case 'KeyS': move.backward = true; break;
        case 'KeyA': move.left = true; break;
        case 'KeyD': move.right = true; break;
        case 'Space': move.up = true; break;
        case 'ShiftRight':
        case 'ShiftLeft': move.down = true; break;
      }
    });

    document.addEventListener('keyup', (event) => {
      switch (event.code) {
        case 'KeyW': move.forward = false; break;
        case 'KeyS': move.backward = false; break;
        case 'KeyA': move.left = false; break;
        case 'KeyD': move.right = false; break;
        case 'Space': move.up = false; break;
        case 'ShiftRight':
        case 'ShiftLeft': move.down = false; break;
      }
    });
}
