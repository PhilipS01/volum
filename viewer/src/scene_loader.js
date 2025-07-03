import * as THREE from './three-proxy.js';
import { threetone } from '/static/assets/index.js';


// Map object types to geometry constructors or custom builders
const typeMap = {
  Box: (props) => new THREE.BoxGeometry(props.width, props.height, props.depth, props.width_segments ?? 1, props.height_segments ?? 1, props.depth_segments ?? 1),
  Sphere: (props) => new THREE.SphereGeometry(props.radius, props.width_segments ?? 32, props.height_segments ?? 32, props.phi_start ?? 0, props.phi_length ?? Math.PI * 2, props.theta_start ?? 0, props.theta_length ?? Math.PI),
  Plane: (props) => new THREE.PlaneGeometry(props.width, props.height, props.width_segments ?? 1, props.height_segments ?? 1),
  PointLight: (props) => new THREE.PointLight(new THREE.Color(props.color ?? 0xffffff), props.intensity ?? 1),
  Cylinder: (props) => new THREE.CylinderGeometry(props.radius_top, props.radius_bottom, props.height, props.radial_segments ?? 32, props.height_segments ?? 1, props.open_ended ?? false, props.theta_start ?? 0, props.theta_length ?? Math.PI * 2),
  Line: (props) => {
    const points = props.args[0].map(p => new THREE.Vector3(...p));
    return new THREE.BufferGeometry().setFromPoints(points);
  },
  Capsule: (props) => new THREE.CapsuleGeometry(props.radius, props.height, props.cap_segments ?? 10, props.radial_segments ?? 20, props.height_segments ?? 1),
  Circle: (props) => new THREE.CircleGeometry(props.radius, props.segments ?? 32, props.theta_start ?? 0, props.theta_length ?? Math.PI * 2),
  Cone: (props) => new THREE.ConeGeometry(props.radius, props.height, props.radial_segments ?? 32, props.height_segments ?? 1, props.open_ended ?? false, props.theta_start ?? 0, props.theta_length ?? Math.PI * 2),
  Dodecahedron: (props) => new THREE.DodecahedronGeometry(props.radius ?? 1, props.detail ?? 0),
  Icosahedron: (props) => new THREE.IcosahedronGeometry(props.radius ?? 1, props.detail ?? 0),
  Octahedron: (props) => new THREE.OctahedronGeometry(props.radius ?? 1, props.detail ?? 0),
  Ring: (props) => new THREE.RingGeometry(props.inner_radius, props.outer_radius, props.theta_segments ?? 32, props.phi_segments ?? 1, props.theta_start ?? 0, props.theta_length ?? Math.PI * 2),
  Tetrahedron: (props) => new THREE.TetrahedronGeometry(props.radius ?? 1, props.detail ?? 0),
  Torus: (props) => new THREE.TorusGeometry(props.radius, props.tube_radius, props.radial_segments ?? 16, props.tubular_segments ?? 48, props.arc ?? Math.PI * 2),
  TorusKnot: (props) => new THREE.TorusKnotGeometry(props.radius, props.tube_radius, props.tubular_segments ?? 64, props.radial_segments ?? 16, props.p ?? 2, props.q ?? 3),

  // Custom example
  Pyramid: (props) => buildPyramidGeometry(props),

  // Data plot example (using canvas texture or mesh)
  Plot2D: (props) => buildPlot2DMesh(props)
};

const materialMap = {
  BasicMaterial: (props) => new THREE.MeshBasicMaterial({ 
    color: new THREE.Color(props.color ?? 0xffffff),
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide
  }),

  StandardMaterial: (props) => new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(props.color ?? 0xffffff),
    roughness: props.roughness ?? 0.5,
    metalness: props.metalness ?? 0.5,
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide
  }),

  PhongMaterial: (props) => new THREE.MeshPhongMaterial({
    color: new THREE.Color(props.color ?? 0xffffff),
    shininess: props.shininess ?? 30,
    specular: new THREE.Color(props.specular_color ?? 0x111111),
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide
  }),

  LineBasicMaterial: (props) => new THREE.LineBasicMaterial({
    color: new THREE.Color(props.color ?? 0xffffff),
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    linewidth: 1 // linewidth will be 1 on most platforms anyway (opengl limitations)
  }),

  LineDashedMaterial: (props) => new THREE.LineDashedMaterial({
    color: new THREE.Color(props.color ?? 0xffffff),
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    linewidth: 1 // linewidth will be 1 on most platforms anyway (opengl limitations)
  }),

  PhysicalMaterial: (props) => new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(props.color ?? 0xffffff),
    roughness: props.roughness ?? 0.5,
    metalness: props.metalness ?? 0.5,
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide,
    clearcoat: props.clearcoat ?? 0,
    clearcoatRoughness: props.clearcoat_roughness ?? 0,
    sheen: props.sheen ?? 0,
    sheenColor: new THREE.Color(props.sheen_color ?? 0x000000),
    sheenRoughness: props.sheen_roughness ?? 1.0,
    specularIntensity: props.specular_intensity ?? 1.0,
    specularColor: new THREE.Color(props.specular_color ?? 0x111111),
    flatShading: props.flat_shading ?? false,
    ior: props.ior ?? 1.5, // index of refraction
    transmission: props.transmission ?? 0, // for glass-like materials
    emissive: new THREE.Color(props.emissive_color ?? 0x000000),
    reflectivity: props.reflectivity ?? 0.5,
    iridescence: props.iridescence ?? 0.0,
    iridescenceIOR: props.iridescence_ior ?? 1.3,
  }),

  MatcapMaterial: (props) => new THREE.MeshMatcapMaterial({
    matcap: props.matcap ? new THREE.TextureLoader().load(props.matcap) :
      new THREE.TextureLoader().load('https://ksenia-k.com/img/threejs/matcaps/6.png'),
    // no color, matcap texture defines color
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide
  }),

  NormalMaterial: (props) => new THREE.MeshNormalMaterial({
    flatShading: props.flatShading ?? false,
    // no color, normal material uses vertex normals for color
    opacity: props.opacity ?? 1,
    transparent: props.opacity < 1,
    wireframe: props.wireframe ?? false,
    side: THREE.DoubleSide
  }),

  ToonMaterial: (props) => {
    const gradientMapTexture = props.gradientMap 
      ? new THREE.TextureLoader().load(props.gradientMap) 
      : new THREE.TextureLoader().load(threetone);
    gradientMapTexture.minFilter = THREE.NearestFilter;
    gradientMapTexture.magFilter = THREE.NearestFilter;

    return new THREE.MeshToonMaterial({
      color: new THREE.Color(props.color ?? 0xffffff),
      gradientMap: gradientMapTexture,
      opacity: props.opacity ?? 1,
      transparent: props.opacity < 1,
      wireframe: props.wireframe ?? false,
      side: THREE.DoubleSide
    });
  }
};

/**
 * Loads a 3D scene from a JSON object.
 * @param {Object} sceneJSON - The JSON representation of the scene.
 * @param {THREE.Scene} scene - The Three.js scene to populate.
 */
export async function loadSceneFromJSON(sceneJSON, scene) {
  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.3));

  // Objects
  console.log(sceneJSON.objects.length, "objects in scene");
  for (const obj of sceneJSON.objects) {
    const threeObject = await buildObject(obj);
    if (threeObject) {
      if (threeObject.material && 'envMap' in threeObject.material) {
        threeObject.material.envMap = scene.environment; // set environment map for physical materials
        threeObject.material.needsUpdate = true; // ensure material is updated
      }
      scene.add(threeObject);
    }
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

  else if (obj.type === 'PointLight' || obj.type === 'DirectionalLight' || obj.type === 'SpotLight') {
    const lightBuilder = typeMap[obj.type];
    if (!lightBuilder) {
      console.warn(`Unknown light type: ${obj.type}`);
      return null;
    }
    const light = lightBuilder(obj);

    light.castShadow = true;
    // high res shadows
    light.shadow.mapSize.width = 2048;
    light.shadow.mapSize.height = 2048;
    // reduce shadow acne
    light.shadow.bias = -0.0001;
    light.shadow.normalBias = 0.02;

    return light;
  }

  else if (obj.type === 'Line') {
    const geometryBuilder = typeMap[obj.type];
    if (!geometryBuilder) {
      console.warn(`Unknown line type: ${obj.type}`);
      return null;
    }

    const materialBuilder = materialMap[obj.material.type];
      if (!materialBuilder) {
        console.warn(`Unknown material type: ${obj.material.type}`);
        return null;
      }

    const geometry = geometryBuilder(obj);
    const material = materialBuilder(obj.material);
    const line = new THREE.Line(geometry, material);
    line.castShadow = true;
    line.receiveShadow = true;

    return line;
  }

  else if (obj.type === 'Plane') {
    buildObjectDefault(obj, false, true);
  }

  else if (obj.type === 'PlotImage') {
    const geometryBuilder = typeMap['Plane'];
    if (!geometryBuilder) {
      console.warn(`Unknown plane type: ${obj.type}`);
      return null;
    }

    const geometry = geometryBuilder(obj);
    const material = new THREE.MeshBasicMaterial({ map: new THREE.TextureLoader().load(obj.image_data), side: obj.double_sided ? THREE.DoubleSide : THREE.FrontSide, transparent: true });
    return new THREE.Mesh(geometry, material);
  }

  else {
    return buildObjectDefault(obj);
  }
}

function buildObjectDefault(obj, castShadow = true, receiveShadow = true) {
  const geometryBuilder = typeMap[obj.type];
  if (!geometryBuilder) {
    console.warn(`Unknown object type: ${obj.type}`);
    return null;
  }

  const materialBuilder = materialMap[obj.material.type];
  if (!materialBuilder) {
    console.warn(`Unknown material type: ${obj.material.type}`);
    return null;
  }

  const geometry = geometryBuilder(obj);
  const material = materialBuilder(obj.material);
  const mesh = new THREE.Mesh(geometry, material);
  mesh.castShadow = castShadow;
  mesh.receiveShadow = receiveShadow;

  return mesh;
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
