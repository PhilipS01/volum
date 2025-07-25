import * as THREE from './three-proxy.js';
import { threetone } from '/static/assets/index.js';
import { viridis, magma, plasma, inferno, infernoGPU } from './shaders/index.js';


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
    const geometryBuilder = typeMap[obj.object ? obj.object.type : 'Arrow'];
    if (!geometryBuilder) {
      console.warn(`Unknown target geometry type for Quiver: ${obj.object.type}`);
      return null;
    }

    let material;

    if (!obj.colorscheme) {
      const materialBuilder = materialMap[obj.object.material.type];
      if (!materialBuilder) {
          console.warn(`Unknown material type: ${obj.material.type}`);
          return null;
      }
      material = materialBuilder(obj.object.material);

    } else {
      material = obj.colorscheme.toLowerCase();
    }

    const geometry = geometryBuilder(obj.object);

    // convert positions and vectors to THREE.Vector3
    const positionArray = obj.args[0].map(p => new THREE.Vector3(...p));
    const vectorArray = obj.args[1].map(v => new THREE.Vector3(...v));
    if (positionArray.length !== vectorArray.length) {
      console.warn(`Quiver: positionArray and vectorArray must have the same length, got ${positionArray.length}, ${vectorArray.length}`);
      return null;
    }
    if (positionArray.length === 0 || vectorArray.length === 0) {
      console.warn(`Quiver: positionArray and vectorArray must not be empty`);
      return null;
    }

    console.assert(material, "Quiver: material must be defined");
    console.log(obj.bounds, "Quiver bounds");
    return buildVectorFieldMeshes(geometry, material, positionArray, vectorArray, obj.bounds, obj.min_length ?? 0.1, obj.max_length ?? 1, obj.colormap ?? 'magnitude');
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
 * If the arrays are of larger size, computations will be offloaded to the GPU.
 * @param {THREE.BufferGeometry} geometry - The geometry to use for the vector field.
 * @param {THREE.Material|string} mat_or_col - The material vector field objects or the string name of a colormap.
 * @param {Array<THREE.Vector3>} positionArray - Array of positions where vectors are defined.
 * @param {Array<THREE.Vector3>} vectorArray - Array of vectors corresponding to each position.
 * @param {number} [max_length=1] - Maximum length of the vectors.
 * @returns {THREE.InstancedMesh|null} The created instanced mesh or null if there was an error.
 */
function buildVectorFieldMeshes(geometry, mat_or_col, positionArray, vectorArray, bounds, min_length = 0.1, max_length = 1, colormap = 'magnitude', animated = false) {
  // center at origin
  if (geometry instanceof THREE.BufferGeometry) {
    geometry.center();
  }
  else {
    console.warn(`buildVectorFieldMeshes: geometry is not a BufferGeometry, got ${geometry.constructor.name}`);
    return null;
  }

  if (!(mat_or_col instanceof THREE.Material) && !(typeof mat_or_col === 'string')) {
    console.warn(`buildVectorFieldMeshes: material is not a THREE.Material or string, got ${mat_or_col.constructor.name}`);
    return null;
  }

  if (!Array.isArray(positionArray) || !Array.isArray(vectorArray)) {
    console.warn(`buildVectorFieldMeshes: positionArray and vectorArray must be arrays, got ${typeof positionArray}, ${typeof vectorArray}`);
    return null;
  }

  if (positionArray.length !== vectorArray.length) {
    console.warn(`buildVectorFieldMeshes: positionArray and vectorArray must have the same length, got ${positionArray.length}, ${vectorArray.length}`);
    return null;
  }

  if (vectorArray.length === 0 || positionArray.length === 0) {
    console.warn(`buildVectorFieldMeshes: positionArray and vectorArray must not be empty`);
    return null;
  }

  if (vectorArray.some(v => !(v instanceof THREE.Vector3))) {
    console.warn(`buildVectorFieldMeshes: vectorArray must contain THREE.Vector3 instances only`);
    return null;
  }

  const count = positionArray.length;
  const mesh = new THREE.InstancedMesh(geometry, (mat_or_col instanceof THREE.Material) ? mat_or_col : null, count);
  // Benchmarks for normalization and coloring
  const lengths = vectorArray.map(v => v.length());
  const min_vec_len = Math.min(...lengths);
  const max_vec_len = Math.max(...lengths);
  
  if (count > 20000) {
    console.log(`buildVectorFieldMeshes: count is ${count} offloading to GPU`);
    buildVectorFieldMeshesGPU(mesh, mat_or_col, positionArray, vectorArray, ...bounds, min_vec_len, max_vec_len, min_length, max_length, colormap, animated);
  } else {
    buildVectorFieldMeshesCPU(mesh, mat_or_col, positionArray, vectorArray, ...bounds, min_vec_len, max_vec_len, min_length, max_length, colormap, animated);
  }
  return mesh;
}

/**
 * Builds a vector field mesh using instancing. Position and direction of vectors are calculated on the CPU.
 * @param {*} mesh - The instanced mesh to build.
 * @param {THREE.Material|string} mat_or_col - The material or colormap (string) to use for the vector field.
 * @param {Array<THREE.Vector3>} positionArray - Array of positions where vectors are defined.
 * @param {Array<THREE.Vector3>} vectorArray - Array of vectors corresponding to each position.
 * @param {number} min_x - Minimum x coordinate of the bounding box.
 * @param {number} min_y - Minimum y coordinate of the bounding box.
 * @param {number} min_z - Minimum z coordinate of the bounding box.
 * @param {number} max_x - Maximum x coordinate of the bounding box.
 * @param {number} max_y - Maximum y coordinate of the bounding box.
 * @param {number} max_z - Maximum z coordinate of the bounding box.
 * @param {number} min_vec_len - Minimum length of the vectors.
 * @param {number} max_vec_len - Maximum length of the vectors.
 * @param {number} min_length - Minimum visual length of the vectors.
 * @param {number} max_length - Maximum visual length of the vectors.
 * @param {string} colormap - Colormap to use for coloring the vectors.
 * @param {boolean} animated - Whether the field will be animated.
 * @returns 
 */
function buildVectorFieldMeshesCPU(mesh, mat_or_col, positionArray, vectorArray, min_x, min_y, min_z, max_x, max_y, max_z, min_vec_len, max_vec_len, min_length = 0.1, max_length = 1, colormap = 'magnitude', animated = false) {
  const count = positionArray.length;
  const instanceValues = new Float32Array(count); // to store normalized vector lengths

  for (let i = 0; i < count; i++) {
    // Normalize the vector length to [0, 1] range with respect to the biggest and smallest vectors
    const dir = vectorArray[i];
    const pos = positionArray[i];
    const rawLen = dir.length();
    const normalized = (rawLen - min_vec_len) / (max_vec_len - min_vec_len); // [0, 1]
    // Map the vector length to the desired range (visual length/size)
    dir.setLength(min_length + normalized * (max_length - min_length));
    // Store the normalized value for coloring
    switch (colormap.toLowerCase()) {
      case 'magnitude':
        instanceValues[i] = normalized; // use normalized length for colormap
        break;
      case 'x':
        instanceValues[i] = Math.abs((pos.x - min_x) / (max_x - min_x)); // use normalized x component for colormap
        break;
      case 'y':
        instanceValues[i] = Math.abs((pos.y - min_y) / (max_y - min_y)); // use normalized y component for colormap
        break;
      case 'z':
        instanceValues[i] = Math.abs((pos.z - min_z) / (max_z - min_z)); // use normalized z component for colormap
        break;
      default:
        console.warn(`Unknown colormap: ${colormap}, using magnitude`);
        instanceValues[i] = normalized; // default to magnitude
    }
  }

  if (animated) {
    mesh.geometry.setAttribute('instanceValue', new THREE.InstancedBufferAttribute(instanceValues, 1)).setUsage(THREE.DynamicDrawUsage);
    mesh.geometry.attributes.instanceValue.needsUpdate = true;
  }
  else {
    mesh.geometry.setAttribute('instanceValue', new THREE.InstancedBufferAttribute(instanceValues, 1));
    
  }

  switch (mat_or_col) {
    case 'viridis':
      mesh.material = viridis.clone();
      break;
    case 'magma':
      mesh.material = magma.clone();
      break;
    case 'plasma':
      mesh.material = plasma.clone();
      break;
    case 'inferno':
      mesh.material = inferno.clone();
      break;
    default:
      if (mat_or_col instanceof THREE.Material) break;
      else mesh.material = viridis.clone(); // default to viridis if string is not recognized
  }


  // Set the instance matrix for each instance
  const dummy = new THREE.Object3D();
  for (let i = 0; i < count; i++) {
    const pos = positionArray[i];
    const vec = vectorArray[i];

    // Set the position of the instance
    dummy.position.copy(pos);
    // Set the rotation to align with the vector direction
    dummy.lookAt(pos.clone().add(vec));
    dummy.updateMatrix();
    mesh.setMatrixAt(i, dummy.matrix);
    // scale the instance based on the vector length and clamp to min_length and max_length
    const len = vec.length();
    dummy.scale.set(len, len, len);
  }

  mesh.instanceMatrix.needsUpdate = animated;

  return mesh;
}

/**
 * Builds a vector field mesh using instancing. Position and direction calculations are offloaded to the shader (GPU).
 * @param {*} mesh - The instanced mesh to build.
 * @param {THREE.Material|string} mat_or_col - The material or colormap (string) to use for the vector field.
 * @param {Array<THREE.Vector3>} positionArray - Array of positions where vectors are defined.
 * @param {Array<THREE.Vector3>} vectorArray - Array of vectors corresponding to each position.
 * @param {number} min_x - Minimum x coordinate of the bounding box.
 * @param {number} min_y - Minimum y coordinate of the bounding box.
 * @param {number} min_z - Minimum z coordinate of the bounding box.
 * @param {number} max_x - Maximum x coordinate of the bounding box.
 * @param {number} max_y - Maximum y coordinate of the bounding box.
 * @param {number} max_z - Maximum z coordinate of the bounding box.
 * @param {number} min_vec_len - Minimum length of the vectors.
 * @param {number} max_vec_len - Maximum length of the vectors.
 * @param {number} min_length - Minimum visual length of the vectors.
 * @param {number} max_length - Maximum visual length of the vectors.
 * @param {string} colormap - Colormap to use for coloring the vectors.
 * @param {boolean} animated - Whether the field will be animated.
 * @returns 
 */
function buildVectorFieldMeshesGPU(mesh, mat_or_col, positionArray, vectorArray, min_x, min_y, min_z, max_x, max_y, max_z, min_vec_len, max_vec_len, min_length = 0.1, max_length = 1, colormap = 'magnitude', animated = false) {
  const count = positionArray.length;
  const instancePos = new Float32Array(count * 3); // to store positions
  const instanceDir = new Float32Array(count * 3); // to store vector components
  const instanceValues = new Float32Array(count); // to store normalized vector lengths
  
  for (let i = 0; i < count; i++) {
    // Normalize the vector length to [0, 1] range with respect to the biggest and smallest vectors
    const dir = vectorArray[i];
    const pos = positionArray[i];
    const rawLen = dir.length();
    const normalized = (rawLen - min_vec_len) / (max_vec_len - min_vec_len); // [0, 1]
    // Map the vector length to the desired range (visual length/size)
    dir.setLength(min_length + normalized * (max_length - min_length));
    // Store the normalized value for coloring
    switch (colormap.toLowerCase()) {
      case 'magnitude':
        instanceValues[i] = normalized; // use normalized length for colormap
        break;
      case 'x':
        instanceValues[i] = Math.abs((pos.x - min_x) / (max_x - min_x)); // use normalized x component for colormap
        break;
      case 'y':
        instanceValues[i] = Math.abs((pos.y - min_y) / (max_y - min_y)); // use normalized y component for colormap
        break;
      case 'z':
        instanceValues[i] = Math.abs((pos.z - min_z) / (max_z - min_z)); // use normalized z component for colormap
        break;
      default:
        console.warn(`Unknown colormap: ${colormap}, using magnitude`);
        instanceValues[i] = normalized; // default to magnitude
    }
  
    instancePos.set([pos.x, pos.y, pos.z], i * 3);
    instanceDir.set([dir.x, dir.y, dir.z], i * 3);
  }

  if (animated) {
    mesh.geometry.setAttribute('instancePos', new THREE.InstancedBufferAttribute(instancePos, 3)).setUsage(THREE.DynamicDrawUsage);
    mesh.geometry.setAttribute('instanceDir', new THREE.InstancedBufferAttribute(instanceDir, 3)).setUsage(THREE.DynamicDrawUsage);
    mesh.geometry.setAttribute('instanceValue', new THREE.InstancedBufferAttribute(instanceValues, 1)).setUsage(THREE.DynamicDrawUsage);
    mesh.geometry.attributes.instancePos.needsUpdate = true;
    mesh.geometry.attributes.instanceDir.needsUpdate = true;
    mesh.geometry.attributes.instanceValue.needsUpdate = true;
  } else {
    mesh.geometry.setAttribute('instancePos', new THREE.InstancedBufferAttribute(instancePos, 3));
    mesh.geometry.setAttribute('instanceDir', new THREE.InstancedBufferAttribute(instanceDir, 3));
    mesh.geometry.setAttribute('instanceValue', new THREE.InstancedBufferAttribute(instanceValues, 1));
    mesh.geometry.attributes.instancePos.needsUpdate = false;
    mesh.geometry.attributes.instanceDir.needsUpdate = false;
    mesh.geometry.attributes.instanceValue.needsUpdate = false;
  }

  switch (mat_or_col) {
    case 'viridis':
      break;
    case 'magma':
      break;
    case 'plasma':
      break;
    case 'inferno':
      mesh.material = infernoGPU.clone();
      break;
    default:
      if (mat_or_col instanceof THREE.Material) break;
      else mesh.material = viridis.clone(); // default to viridis if string is not recognized
  }

  return mesh;
}

/**
 * Builds a scalar field mesh, offloading computations to the GPU.
 */
function buildScalarFieldMeshGPU(fieldArray, bounds, animated = false) {
  if (!(fieldArray[0] instanceof THREE.Vector4 || fieldArray[0] instanceof THREE.Vector3)) {
    console.warn(`buildScalarFieldMeshGPU: fieldArray must contain THREE.Vector4 or THREE.Vector3 instances, got ${fieldArray[0].constructor.name}`);
    return null;
  }

  const count = fieldArray.length;

  if (fieldArray[0] instanceof THREE.Vector4) { // 3D scalar field
    const geometry = new THREE.BufferGeometry();
    const points = new Float32Array(count * 3);
    const values = new Float32Array(count * count * count);
    for (let i = 0; i < count; i++) {
      const p = fieldArray[i];
      points.set([p.x, p.y, p.z], i * 3);
      values[p.x + p.y * width + p.z * width * height] = p.w; // Assuming w is the scalar value
    }

    if (animated) {
      geometry.setAttribute('point', new THREE.BufferAttribute(points, 3)).setUsage(THREE.DynamicDrawUsage);
      geometry.attributes.point.needsUpdate = true;
    } else {
      geometry.setAttribute('point', new THREE.BufferAttribute(points, 3));
    }

    const scalarTex = new THREE.DataTexture3D(values, count, count, count);
    scalarTex.format = THREE.RedFormat;
    scalarTex.type = THREE.FloatType;
    scalarTex.minFilter = scalarTex.magFilter = THREE.LinearFilter;
    scalarTex.unpackAlignment = 1;
    scalarTex.needsUpdate = true;
    
    const material = infernoGPU(scalarTex, ...bounds);
    return new THREE.Mesh(geometry, material);


  } else { // 2D scalar field
    const geometry = new THREE.BufferGeometry();
    const points = new Float32Array(count * 2);
    const values = new Float32Array(count * count);
    for (let i = 0; i < count; i++) {
      const p = fieldArray[i];
      points.set([p.x, p.y], i * 2);
      values[p.x + p.y * width] = p.z; // Assuming z is the scalar value
    }

    if (animated) {
      geometry.setAttribute('point', new THREE.BufferAttribute(points, 2)).setUsage(THREE.DynamicDrawUsage);
      geometry.attributes.point.needsUpdate = true;
    } else {
      geometry.setAttribute('point', new THREE.BufferAttribute(points, 2));
    }
    // TODO: Implement 2D scalar field texture handling

    return null;
  }
}
