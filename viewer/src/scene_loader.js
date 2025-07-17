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
  },

  ImageMaterial: (props) => {
    if (!props.map) {
      console.warn("ImageMaterial requires a map");
      return new THREE.MeshBasicMaterial({ color: 0xffffff });
    }


    return new THREE.MeshStandardMaterial({
      map: new THREE.TextureLoader().load(props.map),
      color: new THREE.Color(props.color ?? 0xffffff),
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
  if (!obj || typeof obj !== 'object' || obj.type.includes("Material")) return null;

  if (obj.type === 'Transform') {
    const child = await buildObject(obj.object); // recursively build child object
    if (!child) return null;

    if (obj.position) child.position.add(new THREE.Vector3(...obj.position));
    if (obj.rotation) {
      const rot = toRadians(obj.rotation); // assumes [x, y, z] in degrees
      child.rotation.x += rot[0];
      child.rotation.y += rot[1];
      child.rotation.z += rot[2];
    }
    if (obj.scale) child.scale.multiply(new THREE.Vector3(...obj.scale));

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
    const material = new THREE.MeshStandardMaterial({ map: new THREE.TextureLoader().load(obj.image_data), transparent: true, side: obj.double_sided ? THREE.DoubleSide : THREE.FrontSide });
    return new THREE.Mesh(geometry, material);
  }

  else if (obj.type === 'Quiver') {
    const geometryBuilder = typeMap[obj.geometry ? obj.geometry.type : 'Arrow'];
    if (!geometryBuilder) {
      console.warn(`Unknown target geometry type for Quiver: ${obj.type}`);
      return null;
    }

    const geometry = geometryBuilder(obj);
    const material = materialMap[obj.material.type] || new THREE.MeshBasicMaterial({ color: 0xffffff });

    // convert positions and vectors to THREE.Vector3
    const positionArray = obj.position_array.map(p => new THREE.Vector3(...p));
    const vectorArray = obj.vector_array.map(v => new THREE.Vector3(...v));
    if (positionArray.length !== vectorArray.length) {
      console.warn(`Quiver: position_array and vector_array must have the same length, got ${positionArray.length}, ${vectorArray.length}`);
      return null;
    }
    if (positionArray.length === 0 || vectorArray.length === 0) {
      console.warn(`Quiver: position_array and vector_array must not be empty`);
      return null;
    }
    return buildVectorFieldMeshes(geometry, material, positionArray, vectorArray, obj.max_length ?? 10);
  }

  else {
    return buildObjectDefault(obj);
  }
}

/** * Builds a Three.js object with default geometry and material.
 * @param {Object} obj - The JSON object describing the 3D object.
 * @param {boolean} [castShadow=true] - Whether the object should cast shadows.
 * @param {boolean} [receiveShadow=true] - Whether the object should receive shadows.
 * @returns {THREE.Mesh|null} The constructed Three.js mesh or null if invalid.
 */
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

/**
 * Builds a vector field mesh from the given geometry and vector arrays, using instancing.
 * @param {THREE.BufferGeometry} geometry - The geometry to use for the vector field.
 * @param {THREE.Material|THREE.Color} mat_or_col - The material or color to use for the vector field.
 * @param {Array<THREE.Vector3>} position_array - Array of positions where vectors are defined.
 * @param {Array<THREE.Vector3>} vector_array - Array of vectors corresponding to each position.
 * @param {number} [max_length=10] - Maximum length of the vectors.
 * @returns {THREE.InstancedMesh|null} The created instanced mesh or null if there was an error.
 */
function buildVectorFieldMeshes(geometry, mat_or_col, position_array, vector_array, max_length = 10) {
  // center at origin
  if (geometry instanceof THREE.BufferGeometry) {
    geometry.center();
  }
  else {
    console.warn(`buildVectorFieldMeshes: geometry is not a BufferGeometry, got ${geometry.constructor.name}`);
    return null;
  }

  if (!(mat_or_col instanceof THREE.Material) && !(mat_or_col instanceof THREE.Color)) {
    console.warn(`buildVectorFieldMeshes: material is not a THREE.Material, got ${mat_or_col.constructor.name}`);
    return null;
  }

  if (!Array.isArray(position_array) || !Array.isArray(vector_array)) {
    console.warn(`buildVectorFieldMeshes: position_array and vector_array must be arrays, got ${typeof position_array}, ${typeof vector_array}`);
    return null;
  }

  if (position_array.length !== vector_array.length) {
    console.warn(`buildVectorFieldMeshes: position_array and vector_array must have the same length, got ${position_array.length}, ${vector_array.length}`);
    return null;
  }

  if (vector_array.length === 0 || position_array.length === 0) {
    console.warn(`buildVectorFieldMeshes: position_array and vector_array must not be empty`);
    return null;
  }

  if (vector_array.some(v => !(v instanceof THREE.Vector3))) {
    console.warn(`buildVectorFieldMeshes: vector_array must contain THREE.Vector3 instances only`);
    return null;
  }

  const count = position_array.length;
  const mesh = new THREE.InstancedMesh(geometry, (mat_or_col instanceof THREE.Material) ? mat_or_col : null, count);

  // clamp vectors
  for (let v of vector_array) {
    v.clampLength(0, max_length); // clamp to a maximum length of max_length
  }

  if (mat_or_col instanceof THREE.Color) {
    const instanceColors = new Float32Array(count * 3); // RGB colors

    for (let i = 0; i < count; i++) {
      // calculate the magnitude of the vector at this point
      const magnitude = vector_array[i].length();
      // Normalize the magnitude to [0, 1] range
      const normalizedMagnitude = Math.min(1, magnitude / max_length); // assuming max magnitude of 10 for normalization
      mat_or_col.setHSL((1 - normalizedMagnitude), 1.0, 0.5);
      instanceColors.set([mat_or_col.r, mat_or_col.g, mat_or_col.b], i * 3);
    }
    mesh.instanceColor = new THREE.InstancedBufferAttribute(instanceColors, 3);

    // Shader
    const material = new THREE.ShaderMaterial({
      vertexShader: /* glsl */`
        attribute vec3 instanceColor;
        varying vec3 vColor;
        void main() {
          vColor = instanceColor;

          // Use instance matrix for position
          vec4 modelViewPosition = modelViewMatrix * instanceMatrix * vec4(position, 1.0);
          gl_Position = projectionMatrix * modelViewPosition;
          gl_PointSize = 1.0; // Adjust point size as needed
        }
      `,
      fragmentShader: /* glsl */`
        varying vec3 vColor;
        void main() {
          gl_FragColor = vec4(vColor, 1.0); // Use instanceColor for fragment color
        }
      `,
      transparent: true,
      vertexColors: true,
      side: THREE.DoubleSide
    });

    mesh.material = material;
  }

  const dummy = new THREE.Object3D();
  let i = 0;
  for (let x of x_array) {
    for (let y of y_array) {
      for (let z of z_array) {
        dummy.position.set(x - x_array.length/2, y - y_array.length/2, z - z_array.length/2);

        // Set arrow direction to vector field
        dummy.lookAt(new THREE.Vector3(x, y, z));

        dummy.updateMatrix();
        mesh.setMatrixAt(i++, dummy.matrix);
      }
    }
  }

  mesh.instanceMatrix.needsUpdate = true; // for setMatrixAt
  mesh.instanceColor.needsUpdate = true; // for setColorAt
  mesh.morphTexture.needsUpdate = true; // for setMorphAt


  return mesh;
}
