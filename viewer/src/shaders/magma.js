import { ShaderMaterial, DoubleSide } from '/static/three-proxy.js';


export const material = new ShaderMaterial({
    vertexShader: /* glsl */`
        attribute float instanceValue;
        varying float vValue;

        void main() {
            vValue = instanceValue;
            vec4 modelViewPosition = modelViewMatrix * instanceMatrix * vec4(position, 1.0);
            gl_Position = projectionMatrix * modelViewPosition;
            gl_PointSize = 1.0;
        }
    `,
  
    fragmentShader: /* glsl */`
        varying float vValue;
        
        vec3 magma(float x) {
            const vec3 c0 = vec3(0.0015, 0.0005, 0.0139);
            const vec3 c1 = vec3(0.063, 0.027, 0.145);
            const vec3 c2 = vec3(0.236, 0.054, 0.239);
            const vec3 c3 = vec3(0.387, 0.094, 0.325);
            const vec3 c4 = vec3(0.533, 0.165, 0.376);
            const vec3 c5 = vec3(0.678, 0.290, 0.388);
            const vec3 c6 = vec3(0.804, 0.431, 0.383);
            const vec3 c7 = vec3(0.906, 0.588, 0.376);
            const vec3 c8 = vec3(0.976, 0.751, 0.478);
            const vec3 c9 = vec3(0.984, 0.894, 0.706);
            const vec3 c10 = vec3(0.987, 0.991, 0.749);

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
            vec3 color = magma(clamp(vValue, 0.0, 1.0));
            gl_FragColor = vec4(color, 1.0);
        }
    `,
    transparent: true,
    side: DoubleSide
});