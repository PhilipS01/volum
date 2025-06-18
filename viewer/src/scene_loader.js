import * as THREE from './three-proxy.js';


// Map object types to geometry constructors or custom builders
const typeMap = {
  Box: (props) => new THREE.BoxGeometry(props.width, props.height, props.depth),
  Sphere: (props) => new THREE.SphereGeometry(props.radius, 32, 32),
  Plane: (props) => new THREE.PlaneGeometry(props.width, props.height),

  // Custom example
  Pyramid: (props) => buildPyramidGeometry(props),

  // Data plot example (using canvas texture or mesh)
  Plot2D: (props) => buildPlot2DMesh(props)
};

/**
 * Loads a 3D scene from a JSON object.
 * @param {Object} sceneJSON - The JSON representation of the scene.
 * @param {THREE.Scene} scene - The Three.js scene to populate.
 */
export async function loadSceneFromJSON(sceneJSON, scene) {
  const ambientLight = new THREE.AmbientLight( 0x404040, 5 ); // soft white light
  scene.add(ambientLight);

  const directionalLight = new THREE.PointLight(0xffffff, 2); // bright white light
  directionalLight.position.set(50, 50, 50);
  directionalLight.castShadow = true;
  scene.add(directionalLight);
  console.log("Added lights to scene");
  console.log(sceneJSON.objects.length, "objects in scene");
  for (const obj of sceneJSON.objects) {
    const threeObject = await buildObject(obj);
    if (threeObject) scene.add(threeObject);
    console.log(`Added object: ${obj.type}`, threeObject);
  }
}

/**
 * Builds a Three.js object from a JSON representation.
 * @param {Object} obj - The JSON object describing the 3D object.
 * @returns {Promise<THREE.Object3D|null>} The constructed Three.js object or null if invalid.
 */
async function buildObject(obj) {
  if (!obj || typeof obj !== 'object') return null;

  if (obj.type === 'Transform') {
    const child = await buildObject(obj.object); // recursively build child object
    if (!child) return null;

    if (obj.position) child.position.set(...obj.position);
    if (obj.rotation) child.rotation.set(...toRadians(obj.rotation));
    if (obj.scale)    child.scale.set(...obj.scale);

    return child;
  }

  else if (obj.type === 'Volume') {
    const tex = await loadVolumeTexture(obj.file_path, {
      width: obj.width,
      height: obj.height,
      depth: obj.depth
    });
    return createVolumeProxyMesh(tex, {
      width: obj.width,
      height: obj.height,
      depth: obj.depth,
      color: obj.color ?? 0xffffff
    });
  }

  else {
    const geometryBuilder = typeMap[obj.type];
    if (!geometryBuilder) {
      console.warn(`Unknown object type: ${obj.type}`);
      return null;
    }

    const geometry = geometryBuilder(obj);
    const material = new THREE.MeshStandardMaterial({ color: new THREE.Color(obj.color ?? 0x00ff00) });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    return mesh;
  }
}

/**
 * Loads a 3D volume texture from a URL.
 * @param {string} url - The URL of the volume data.
 * @param {Object} param1 - Additional parameters.
 * @returns {Promise<THREE.DataTexture3D>} A promise that resolves to the loaded 3D texture.
 */
function loadVolumeTexture(url, { width, height, depth, format = THREE.RedFormat, type = THREE.UnsignedByteType }) {
  return fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.statusText}`);
      return res.arrayBuffer();
    })
    .then(buffer => {
      const array = (type === THREE.UnsignedByteType)
        ? new Uint8Array(buffer)
        : new Float32Array(buffer);
      const tex = new THREE.DataTexture3D(array, width, height, depth);
      tex.format = format;
      tex.type   = type;
      tex.minFilter = tex.magFilter = THREE.LinearFilter;
      tex.unpackAlignment = 1;
      tex.needsUpdate = true;
      return tex;
    });
}

/**
 * Creates a proxy mesh for a 3D volume texture.
 * @param {THREE.DataTexture3D} dataTex - The 3D texture to use.
 * @param {Object} param1 - Additional parameters.
 * @returns {THREE.Mesh} The created mesh.
 */
function createVolumeProxyMesh(dataTex, { width, height, depth, color }) {
  if (!dataTex || !(dataTex instanceof THREE.DataTexture3D)) {
    throw new Error('Invalid data texture provided to createVolumeProxyMesh');
  }

  // Simple “proxy” geometry covering the unit cube
  const geo = new THREE.BoxGeometry(1,1,1);

  // A basic ray-marching shader material (you’d swap in your real GLSL)
  const mat = new THREE.ShaderMaterial({
    uniforms: {
        uDataTex: { value: dataTex },
        uRes:     { value: new THREE.Vector3(width, height, depth) },
        uColor:   { value: new THREE.Color(color) },
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
                vec3 uvw = vPos * 0.5 + 0.5; // map [-1,1]→[0,1]
                float intensity = texture(uDataTex, uvw).r;
                gl_FragColor = vec4(uColor * intensity, intensity);
            }
        `,
        transparent: true,
    });

    return new THREE.Mesh(geo, mat);
}

/**
 * Helper function that converts an array of angles in degrees to radians.
 * @param {number[]} degrees - The angles in degrees.
 * @returns {number[]} The angles in radians.
 */
function toRadians(degrees) {
  return degrees.map(d => d * Math.PI / 180);
}

// --- Custom Geometry Builders ---
function buildPyramidGeometry({ base = 1, height = 1 }) {
  const geometry = new THREE.Geometry();
  const half = base / 2;

  geometry.vertices.push(
    new THREE.Vector3(-half, 0, -half),
    new THREE.Vector3(half, 0, -half),
    new THREE.Vector3(half, 0, half),
    new THREE.Vector3(-half, 0, half),
    new THREE.Vector3(0, height, 0)
  );

  geometry.faces.push(
    new THREE.Face3(0, 1, 4),
    new THREE.Face3(1, 2, 4),
    new THREE.Face3(2, 3, 4),
    new THREE.Face3(3, 0, 4),
    new THREE.Face3(0, 1, 2),
    new THREE.Face3(2, 3, 0)
  );

  geometry.computeFaceNormals();
  return geometry;
}

function buildPlot2DMesh({ data }) {
  // For demo: represent plot as flat plane (extend with texture/lines later)
  const [x, y] = data;
  const geometry = new THREE.PlaneGeometry(2, 2);
  const material = new THREE.MeshBasicMaterial({ color: 'cyan', side: THREE.DoubleSide });
  return new THREE.Mesh(geometry, material);
}