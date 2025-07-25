import { ShaderMaterial, Vector3 } from '/static/three-proxy.js';

export const material = (scalarTex, min_x, min_y, min_z, max_x, max_y, max_z) => new ShaderMaterial({
  uniforms: {
    uScalarField: { value: scalarTex },
    uBoundsMin: { value: new Vector3(min_x, min_y, min_z) },
    uBoundsMax: { value: new Vector3(max_x, max_y, max_z) }
  },
  vertexShader: `
    attribute vec3 point;
    attribute float instanceValue;
    varying float vValue;

    uniform sampler3D uScalarField;
    uniform vec3 uBoundsMin;
    uniform vec3 uBoundsMax;

    void main() {
      vec3 normalizedPos = (position - uBoundsMin) / (uBoundsMax - uBoundsMin);
      vValue = texture(uScalarField, normalizedPos).r;

      vec4 modelViewPosition = modelViewMatrix * instanceMatrix * vec4(position, 1.0);
      gl_Position = projectionMatrix * modelViewPosition;
    }
  `,
  fragmentShader: `
    varying float vValue;

    vec3 inferno(float x) {
      const vec3 c0 = vec3(0.001, 0.000, 0.014);
      const vec3 c1 = vec3(0.067, 0.016, 0.172);
      const vec3 c2 = vec3(0.223, 0.033, 0.373);
      const vec3 c3 = vec3(0.416, 0.057, 0.502);
      const vec3 c4 = vec3(0.626, 0.127, 0.474);
      const vec3 c5 = vec3(0.796, 0.254, 0.374);
      const vec3 c6 = vec3(0.902, 0.427, 0.286);
      const vec3 c7 = vec3(0.973, 0.627, 0.202);
      const vec3 c8 = vec3(0.988, 0.816, 0.144);
      const vec3 c9 = vec3(0.989, 0.957, 0.208);
      const vec3 c10 = vec3(0.998, 0.998, 0.858);

      float t = clamp(x, 0.0, 1.0);
      if (t < 0.1) return mix(c0, c1, t / 0.1);
      else if (t < 0.2) return mix(c1, c2, (t - 0.1) / 0.1);
      else if (t < 0.3) return mix(c2, c3, (t - 0.2) / 0.1);
      else if (t < 0.4) return mix(c3, c4, (t - 0.3) / 0.1);
      else if (t < 0.5) return mix(c4, c5, (t - 0.4) / 0.1);
      else if (t < 0.6) return mix(c5, c6, (t - 0.5) / 0.1);
      else if (t < 0.7) return mix(c6, c7, (t - 0.6) / 0.1);
      else if (t < 0.8) return mix(c7, c8, (t - 0.7) / 0.1);
      else if (t < 0.9) return mix(c8, c9, (t - 0.8) / 0.1);
      else return mix(c9, c10, (t - 0.9) / 0.1);
    }

    void main() {
      vec3 color = inferno(vValue);
      gl_FragColor = vec4(color, 1.0);
    }
  `,
  transparent: true
});