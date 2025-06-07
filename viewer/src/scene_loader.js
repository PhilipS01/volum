import * as THREE from 'three';

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

// Recursive scene loader
export function loadSceneFromJSON(sceneJSON, scene) {
  for (const obj of sceneJSON.objects) {
    const threeObject = buildObject(obj);
    if (threeObject) {
      scene.add(threeObject);
    }
  }
}

function buildObject(obj) {
  if (!obj || typeof obj !== 'object') return null;

  if (obj.type === 'Transform') {
    const child = buildObject(obj.object); // recursively build child object
    if (!child) return null;

    if (obj.position) child.position.set(...obj.position);
    if (obj.rotation) child.rotation.set(...toRadians(obj.rotation));
    if (obj.scale)    child.scale.set(...obj.scale);

    return child;
  }

  const geometryBuilder = typeMap[obj.type];
  if (!geometryBuilder) {
    console.warn(`Unknown object type: ${obj.type}`);
    return null;
  }

  const geometry = geometryBuilder(obj);
  const material = new THREE.MeshStandardMaterial({ color: obj.color || 'gray' });
  const mesh = new THREE.Mesh(geometry, material);

  return mesh;
}

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