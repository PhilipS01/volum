import * as THREE         from 'https://unpkg.com/three@0.152.0/build/three.module.js';
import { OrbitControls }  from 'https://unpkg.com/three@0.152.0/examples/jsm/controls/OrbitControls.js';
import { loadSceneFromJSON }   from '.scene_loader.js';
import { loadVolumeTexture }   from '.scene_loader.js';  // or inline helper

const canvas = document.getElementById('three-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
const scene    = new THREE.Scene();
const camera   = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 100);
camera.position.set(2,2,2);
//document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Helper to remove all meshes from scene
function clearScene() {
  scene.children.slice().forEach(c => scene.remove(c));
}

// Live-update socket
const ws = new WebSocket(`ws://${location.host}/scene/ws`);
ws.onmessage = async ({ data }) => {
    if (data === 'scene_updated') {
        const json = await fetch('/scene').then(r => r.json());
        clearScene();
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

    // TODO: Have to dynamically load volumes (from scene JSON or separate endpoint) (not only one volume)
    // TODO: put this inside volume_loader.js instead of here
    // const textures = await Promise.all(volumes.map(v => loadVolumeTexture(v.url, v)));
    const tex = await loadVolumeTexture('/api/scene/volume', { width, height, depth });
    volumeMesh = createVolumeProxyMesh(tex, { width, height, depth, color: 0xff0000 });
    scene.add(volumeMesh);

    // 4) For each volume texture, create a full‐screen proxy mesh with a custom shader
    textures.forEach((tex, i) => {
      // Simple “proxy” geometry covering the unit cube
      const geo = new THREE.BoxGeometry(1,1,1);

      // A basic ray-marching shader material (you’d swap in your real GLSL)
      const mat = new THREE.ShaderMaterial({
        uniforms: {
          uDataTex: { value: tex },
          uRes:     { value: new THREE.Vector3(volumes[i].width, volumes[i].height, volumes[i].depth) },
          uColor:   { value: new THREE.Color(volumes[i].color) },
          // …plus camera, model-matrix, step-size, etc…
        },
        vertexShader: /* glsl */`
          varying vec3 vPos;
          void main() {
            vPos = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `,
        fragmentShader: /* glsl */`
          precision highp float;
          uniform sampler3D uDataTex;
          uniform vec3 uRes;
          uniform vec3 uColor;
          varying vec3 vPos;
          void main() {
            // Ray-march simply by sampling one voxel at the vertex‐pos
            // (for demo purposes—real raymarch loops over t)
            vec3 uvw = vPos * 0.5 + 0.5; // map [-1,1]→[0,1]
            float intensity = texture(uDataTex, uvw).r;
            gl_FragColor = vec4(uColor * intensity, intensity);
          }
        `,
        transparent: true,
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(i*1.5, 0, 0); // offset volumes if you like
      scene.add(mesh);
    });

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