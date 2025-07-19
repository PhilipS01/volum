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

        vec3 viridis(float x) {
            const vec3 c0 = vec3(0.267, 0.005, 0.329);
            const vec3 c1 = vec3(0.283, 0.141, 0.458);
            const vec3 c2 = vec3(0.254, 0.265, 0.530);
            const vec3 c3 = vec3(0.207, 0.372, 0.553);
            const vec3 c4 = vec3(0.164, 0.471, 0.558);
            const vec3 c5 = vec3(0.128, 0.567, 0.551);
            const vec3 c6 = vec3(0.135, 0.659, 0.518);
            const vec3 c7 = vec3(0.267, 0.749, 0.441);
            const vec3 c8 = vec3(0.478, 0.821, 0.318);
            const vec3 c9 = vec3(0.741, 0.873, 0.150);
            const vec3 c10 = vec3(0.993, 0.906, 0.144);
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
            vec3 color = viridis(clamp(vValue, 0.0, 1.0));
            gl_FragColor = vec4(color, 1.0);
        }
    `,
    transparent: true,
    side: DoubleSide
});