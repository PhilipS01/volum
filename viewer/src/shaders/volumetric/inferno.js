import { ShaderMaterial, Vector3, DoubleSide } from '/static/three-proxy.js';

export const material = (tex3D, dims) => new ShaderMaterial({
  uniforms: {
    uField: { value: tex3D },
    uThreshold: { value: 0.5 },
    uSize: { value: new Vector3(...dims) }
  },
  vertexShader: `
    varying vec3 vPos;
    void main() {
      vPos = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    precision highp sampler3D;
    uniform sampler3D uField;
    uniform float uThreshold;
    uniform vec3 uSize;
    varying vec3 vPos;

    void main() {
      vec3 texCoord = vPos * 0.5 + 0.5; // map [-1,1] to [0,1]
      float val = texture(uField, texCoord).r;

      if (val < uThreshold) discard;

      gl_FragColor = vec4(vec3(val), 1.0); // grayscale based on value
    }
  `,
  transparent: true,
  side: DoubleSide
});