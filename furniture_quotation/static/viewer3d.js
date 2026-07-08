// ============================================================
// viewer3d.js — Result Page ka JavaScript
// ============================================================
// Ye file result.html ke saath kaam karti hai.
//
// Python backend se ye data milta hai (result.html mein inject hota hai):
//   BOXES   → furniture ke 3D boxes ka data (viewer_3d.py se aata hai)
//   Furn_L  → furniture ki length (feet mein)
//   Furn_W  → furniture ki width (feet mein)
//   Furn_H  → furniture ki height (feet mein)
//   ITEM    → furniture ka naam (jaise "Wardrobe", "Bed" etc.)
//
// Iska kaam:
//   1. 2D / 3D view toggle karna
//   2. Three.js se 3D scene banana
//   3. Camera controls (rotate, zoom, pan)
//   4. Preset views (Front, Side, Top, Reset)
// ============================================================

// Three.js library: static/three.min.js se load hoti hai
// (ye ek local file hai, internet ki zaroorat nahi)

// Global variables (3D scene ke liye)
var _3dInitialised = false;   // kya 3D scene ban chuka hai?
var _controls, _renderer, _animId; // Three.js objects

// ============================================================
// 2D ↔ 3D VIEW TOGGLE
// ============================================================
// mode = '2d' ya '3d'
function switchView(mode) {
  var p2    = document.getElementById('panel2d');
  var p3    = document.getElementById('panel3d');
  var b2    = document.getElementById('btn2d');
  var b3    = document.getElementById('btn3d');
  var tb    = document.getElementById('toolbar3d');
  var title = document.getElementById('viewerTitle');
  var hint  = document.getElementById('viewerHint');

  if (mode === '2d') {
    // 2D panel dikhao, 3D panel chhupao
    p2.classList.add('visible');    p3.classList.remove('visible');
    b2.classList.add('active');     b3.classList.remove('active');
    tb.style.display = 'none';
    title.textContent = '\uD83D\uDCD0 2D Drawing \u2014 ' + ITEM;
    hint.textContent  = '\uD83D\uDCCF Front elevation view';
    // 3D animation band karo (battery/CPU bachao)
    if (_animId) { cancelAnimationFrame(_animId); _animId = null; }
  } else {
    // 3D panel dikhao, 2D panel chhupao
    p3.classList.add('visible');    p2.classList.remove('visible');
    b3.classList.add('active');     b2.classList.remove('active');
    tb.style.display = 'flex';
    title.textContent = '\uD83D\uDCE6 3D View \u2014 ' + ITEM;
    hint.textContent  = '\uD83D\uDDB1 Drag=Rotate \u00B7 Scroll=Zoom \u00B7 Right-drag=Pan';
    // Pehli baar 3D bana, baad mein sirf resume karo
    if (!_3dInitialised) { init3D(); }
    else { animate3D(); }
  }
}

// ============================================================
// ORBIT CONTROLS (Mouse se rotate/zoom/pan)
// ============================================================
// Three.js mein OrbitControls normally alag file mein hoti hai,
// yahan hum ise khud define kar rahe hain (no extra CDN needed)
function OrbitControls(object, domElement) {
  this.object = object;
  this.domElement = domElement;
  this.enabled = true;
  this.target = new THREE.Vector3();
  this.minDistance = 0; this.maxDistance = Infinity;
  this.autoRotate = true; this.autoRotateSpeed = 2.0;
  this.enableDamping = true; this.dampingFactor = 0.05;

  var scope = this;
  var STATE = { NONE:-1, ROTATE:0, DOLLY:1, PAN:2 };
  var state = STATE.NONE;
  var EPS = 1e-6;
  var spherical = new THREE.Spherical();
  var sphericalDelta = new THREE.Spherical();
  var scale = 1;
  var panOffset = new THREE.Vector3();
  var rotateStart = new THREE.Vector2();
  var rotateEnd = new THREE.Vector2();
  var rotateDelta = new THREE.Vector2();
  var panStart = new THREE.Vector2();
  var panEnd = new THREE.Vector2();
  var panDelta = new THREE.Vector2();
  var twoPI = 2 * Math.PI;

  // Camera position update (auto-rotate + user input)
  this.update = (function() {
    var offset       = new THREE.Vector3();
    var quat         = new THREE.Quaternion().setFromUnitVectors(object.up, new THREE.Vector3(0,1,0));
    var quatInverse  = quat.clone().invert();
    var lastPosition = new THREE.Vector3();
    var lastQuaternion = new THREE.Quaternion();
    return function update() {
      var position = scope.object.position;
      offset.copy(position).sub(scope.target);
      offset.applyQuaternion(quat);
      spherical.setFromVector3(offset);
      if (scope.autoRotate && state === STATE.NONE) {
        spherical.theta += (twoPI / 60 / 60) * scope.autoRotateSpeed;
      }
      spherical.phi = Math.max(EPS, Math.min(Math.PI - EPS, spherical.phi));
      spherical.makeSafe();
      spherical.theta += sphericalDelta.theta;
      spherical.phi   += sphericalDelta.phi;
      spherical.radius = Math.max(scope.minDistance, Math.min(scope.maxDistance, spherical.radius * scale));
      scope.target.addScaledVector(panOffset, 1);
      offset.setFromSpherical(spherical);
      offset.applyQuaternion(quatInverse);
      position.copy(scope.target).add(offset);
      scope.object.lookAt(scope.target);
      if (scope.enableDamping) {
        sphericalDelta.theta *= (1 - scope.dampingFactor);
        sphericalDelta.phi   *= (1 - scope.dampingFactor);
        panOffset.multiplyScalar(1 - scope.dampingFactor);
      } else {
        sphericalDelta.set(0,0,0);
        panOffset.set(0,0,0);
      }
      scale = 1;
      return true;
    };
  })();

  this.dispose = function() {
    scope.domElement.removeEventListener('mousedown', onMouseDown);
    scope.domElement.removeEventListener('wheel', onMouseWheel);
  };

  // ── Mouse Events ──────────────────────────────────────────
  function onMouseDown(ev) {
    if (!scope.enabled) return;
    ev.preventDefault();
    if (ev.button === 0) { state = STATE.ROTATE; rotateStart.set(ev.clientX, ev.clientY); }
    else if (ev.button === 2) { state = STATE.PAN; panStart.set(ev.clientX, ev.clientY); }
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  }
  function onMouseMove(ev) {
    if (!scope.enabled) return;
    ev.preventDefault();
    if (state === STATE.ROTATE) {
      rotateEnd.set(ev.clientX, ev.clientY);
      rotateDelta.subVectors(rotateEnd, rotateStart);
      var el = scope.domElement;
      sphericalDelta.theta -= (twoPI * rotateDelta.x) / (el.clientHeight * 4);
      sphericalDelta.phi   -= (twoPI * rotateDelta.y) / (el.clientHeight * 4);
      rotateStart.copy(rotateEnd);
    } else if (state === STATE.PAN) {
      panEnd.set(ev.clientX, ev.clientY);
      panDelta.subVectors(panEnd, panStart).multiplyScalar(0.002);
      panOffset.addScaledVector(new THREE.Vector3(-panDelta.x, panDelta.y, 0), 1);
      panStart.copy(panEnd);
    }
    scope.update();
  }
  function onMouseUp() {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
    state = STATE.NONE;
  }
  function onMouseWheel(ev) {
    if (!scope.enabled) return;
    ev.preventDefault();
    scale *= (ev.deltaY < 0) ? (1/0.92) : 0.92;
    scope.update();
  }
  function onContextMenu(ev) { ev.preventDefault(); }

  domElement.addEventListener('mousedown', onMouseDown, false);
  domElement.addEventListener('wheel', onMouseWheel, {passive:false});
  domElement.addEventListener('contextmenu', onContextMenu, false);

  // ── Touch Events (mobile support) ─────────────────────────
  function onTouchStart(ev) {
    ev.preventDefault();
    if (ev.touches.length === 1) { state = STATE.ROTATE; rotateStart.set(ev.touches[0].pageX, ev.touches[0].pageY); }
  }
  function onTouchMove(ev) {
    ev.preventDefault();
    if (ev.touches.length === 1 && state === STATE.ROTATE) {
      rotateEnd.set(ev.touches[0].pageX, ev.touches[0].pageY);
      rotateDelta.subVectors(rotateEnd, rotateStart).multiplyScalar(0.005);
      sphericalDelta.theta -= rotateDelta.x * 0.8;
      sphericalDelta.phi   -= rotateDelta.y * 0.8;
      rotateStart.copy(rotateEnd);
      scope.update();
    }
  }
  function onTouchEnd() { state = STATE.NONE; }
  domElement.addEventListener('touchstart', onTouchStart, {passive:false});
  domElement.addEventListener('touchmove',  onTouchMove,  {passive:false});
  domElement.addEventListener('touchend',   onTouchEnd,   false);

  Object.assign(this, THREE.EventDispatcher.prototype);
  this.update();
}

// ============================================================
// 3D SCENE INITIALIZE
// ============================================================
// Ye function ek baar chalti hai jab user pehli baar 3D view kholega
function init3D() {
  _3dInitialised = true;
  var container = document.getElementById('viewer3d');
  var W = container.clientWidth || 700;
  var H = 500;

  // Scene → ye 3D duniya hai jisme sab kuch rakhte hain
  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d0d1a);
  scene.fog = new THREE.FogExp2(0x0d0d1a, 0.005); // door ki cheezein fade hongi

  // Camera → user ki aankh
  var camera = new THREE.PerspectiveCamera(45, W/H, 0.05, 500);

  // Renderer → scene ko canvas pe draw karta hai
  _renderer = new THREE.WebGLRenderer({ antialias: true });
  _renderer.setSize(W, H);
  _renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  _renderer.shadowMap.enabled = true;
  _renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(_renderer.domElement); // canvas ko page pe daalo

  // ── LIGHTS (Roshan karo scene ko) ──────────────────────────
  scene.add(new THREE.AmbientLight(0x334466, 0.8));       // background light

  var sun = new THREE.DirectionalLight(0xffd060, 1.4);    // main sun light
  sun.position.set(12, 18, 10);
  sun.castShadow = true;
  sun.shadow.mapSize.width = sun.shadow.mapSize.height = 2048;
  sun.shadow.camera.near = 0.5; sun.shadow.camera.far = 200;
  sun.shadow.camera.left = sun.shadow.camera.bottom = -30;
  sun.shadow.camera.right = sun.shadow.camera.top = 30;
  scene.add(sun);

  var fill = new THREE.DirectionalLight(0x6699ee, 0.5);   // fill light (shadows soft karo)
  fill.position.set(-10, 8, -5); scene.add(fill);

  var rim = new THREE.DirectionalLight(0xff9933, 0.30);   // rim light (edge highlight)
  rim.position.set(0, 4, -15); scene.add(rim);

  scene.add(new THREE.HemisphereLight(0x3355aa, 0x221100, 0.45)); // sky/ground light

  // ── ROOM ENVIRONMENT ─────────────────────────────────────
  var maxDim = Math.max(Furn_L, Furn_W, Furn_H);
  buildRoom(scene);

  // Shadow receiver (invisible, just catches shadows on floor)
  var shadowPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(maxDim * 6, maxDim * 6),
    new THREE.ShadowMaterial({ opacity: 0.18 })
  );
  shadowPlane.rotation.x = -Math.PI / 2;
  shadowPlane.position.y = 0.001;
  shadowPlane.receiveShadow = true;
  scene.add(shadowPlane);

  // ── FINISH PROFILES (roughness, metalness, color tint) ──
  // Each finish gives a different realistic look in the 3D viewer
  var FINISH_PROFILES = {
    "Laminate":   { roughness: 0.55, metalness: 0.05, shine: 0.0,  tint: 0x000000 }, // matte flat
    "Veneer":     { roughness: 0.35, metalness: 0.08, shine: 0.05, tint: 0x000000 }, // satin wood sheen
    "PU Paint":   { roughness: 0.20, metalness: 0.10, shine: 0.15, tint: 0x050505 }, // semi-gloss smooth
    "Duco Paint": { roughness: 0.15, metalness: 0.12, shine: 0.20, tint: 0x080808 }, // glossy matte
    "Acrylic":    { roughness: 0.05, metalness: 0.18, shine: 0.40, tint: 0x0a0a0a }, // high gloss acrylic
    "High Gloss": { roughness: 0.02, metalness: 0.22, shine: 0.50, tint: 0x0d0d0d }, // mirror-like gloss
  };
  var fp = FINISH_PROFILES[FINISH] || FINISH_PROFILES["Laminate"];


  // ── FURNITURE BOXES ──────────────────────────────────────────
  // BOXES → Python ke viewer_3d.py ne ye data banaya hai
  var group = new THREE.Group();

  BOXES.forEach(function(b) {
    var w = b.x1 - b.x0;
    var h = b.z1 - b.z0;
    var d = b.y1 - b.y0;
    if (w <= 0.001 || h <= 0.001 || d <= 0.001) return;

    var geo = new THREE.BoxGeometry(w, h, d);
    var lbl = (b.label || '').toLowerCase();

    var isMetal  = lbl.indexOf('handle') >= 0 || lbl.indexOf('hinge') >= 0 || lbl.indexOf('rail') >= 0;
    var isFabric = lbl.indexOf('mattress') >= 0 || lbl.indexOf('cushion') >= 0 || lbl.indexOf('pillow') >= 0;
    var isBook   = lbl.indexOf('book') >= 0;

    var baseColor = new THREE.Color(b.color);

    // Apply finish tint to wood/main parts (not metal/fabric/books)
    if (!isMetal && !isFabric && !isBook) {
      baseColor.lerp(new THREE.Color(fp.tint), fp.shine * 0.3);
    }

    var mat;
    if (isMetal) {
      // Shiny metal handles/hinges
      mat = new THREE.MeshStandardMaterial({
        color: baseColor,
        roughness: 0.15,
        metalness: 0.90,
      });
    } else if (isFabric) {
      // Soft matte fabric for mattress/cushions
      mat = new THREE.MeshStandardMaterial({
        color: baseColor,
        roughness: 0.92,
        metalness: 0.00,
      });
    } else {
      // Wood/board surface — finish profile applied
      mat = new THREE.MeshStandardMaterial({
        color:     baseColor,
        roughness: fp.roughness,
        metalness: fp.metalness,
      });
    }

    var mesh = new THREE.Mesh(geo, mat);
    mesh.castShadow    = true;
    mesh.receiveShadow = true;
    mesh.position.set(
      (b.x0 + b.x1) / 2 - Furn_L / 2,
      (b.z0 + b.z1) / 2,
      (b.y0 + b.y1) / 2 - Furn_W / 2
    );

    // Edge lines (outline) — softer for glossy finishes
    var edgeOpacity = fp.roughness > 0.4 ? 0.18 : 0.08;
    var edges   = new THREE.EdgesGeometry(geo, 12);
    var lineMat = new THREE.LineBasicMaterial({ color: 0x000000, transparent: true, opacity: edgeOpacity });
    var lines   = new THREE.LineSegments(edges, lineMat);
    lines.position.copy(mesh.position);

    group.add(mesh);
    group.add(lines);
  });

  group.rotation.y = Math.PI; // rotate 180 degrees so it faces the front, not the wall
  scene.add(group);

  // ── CAMERA POSITION ──────────────────────────────────────
  var camDist  = maxDim * 1.65;
  var camTarget = new THREE.Vector3(0, Furn_H / 2, 0);
  camera.position.set(camDist * 0.9, camDist * 0.75, camDist * 1.1);
  camera.lookAt(camTarget);

  // ── ORBIT CONTROLS ────────────────────────────────────────
  _controls = new OrbitControls(camera, _renderer.domElement);
  _controls.target.copy(camTarget);
  _controls.minDistance     = maxDim * 0.15;
  _controls.maxDistance     = maxDim * 7;
  _controls.autoRotate      = true;
  _controls.autoRotateSpeed = 1.8;
  _controls.enableDamping   = true;
  _controls.dampingFactor   = 0.06;
  _controls.update();

  // Jab user mouse se rotate kare, auto-rotate band karo
  _renderer.domElement.addEventListener('mousedown', function() {
    _controls.autoRotate = false;
    var btn = document.getElementById('btnAuto');
    if (btn) { btn.classList.remove('active'); btn.textContent = '\u21BB Auto'; }
  });

  var overlayHidden = false;

  // ── PRESET VIEWS (Front, Side, Top, Reset) ────────────────
  window.setView = function(v) {
    var d = camDist;
    var positions = {
      front: new THREE.Vector3(0,       Furn_H/2, d * 1.3),  // seedha saamne
      side:  new THREE.Vector3(d * 1.3, Furn_H/2, 0),         // side se
      top:   new THREE.Vector3(0.01,    d * 2.5,  0.01),       // upar se
      iso:   new THREE.Vector3(d*0.9,   d*0.75,   d*1.1),     // default angle
    };
    var pos = positions[v];
    if (!pos) return;
    camera.position.copy(pos);
    camera.lookAt(camTarget);
    _controls.target.copy(camTarget);
    _controls.update();
  };

  // Auto-rotate toggle button
  window.toggleAutoRotate = function() {
    _controls.autoRotate = !_controls.autoRotate;
    var btn = document.getElementById('btnAuto');
    if (btn) {
      btn.classList.toggle('active', _controls.autoRotate);
      btn.textContent = _controls.autoRotate ? '\u23F8 Stop' : '\u21BB Auto';
    }
  };

  // ── ANIMATION LOOP ────────────────────────────────────────
  // Ye loop baar-baar chalta hai (60fps) — scene render karta hai
  function tick() {
    _animId = requestAnimationFrame(tick);
    _controls.update();
    _renderer.render(scene, camera);
    // Loading overlay hata do pehli render ke baad
    if (!overlayHidden) {
      overlayHidden = true;
      var ov = document.getElementById('loadingOverlay');
      if (ov) ov.style.display = 'none';
    }
  }
  _animId = requestAnimationFrame(tick);

  // ── WINDOW RESIZE HANDLE ──────────────────────────────────
  window.addEventListener('resize', function() {
    var nw = container.clientWidth;
    camera.aspect = nw / H;
    camera.updateProjectionMatrix();
    _renderer.setSize(nw, H);
  });
}

// Resume 3D animation (agar 2D view mein gaye the)
function animate3D() {
  if (_controls && _renderer && !_animId) {
    (function tick() {
      _animId = requestAnimationFrame(tick);
      _controls.update();
    })();
  }
}

// ============================================================
// ROOM ENVIRONMENT v2 — Vibrant colors, clean & clear
// ============================================================

function getRoomType() {
  var n = ITEM.toLowerCase();
  if (/wardrobe|walk.in|dressing|vanity|bedside|chest of draw/.test(n)) return 'bedroom';
  if (/\bbed\b|bunk bed|sofa bed|daybed|hydraulic|storage bed/.test(n)) return 'bedroom';
  if (/kitchen|pantry|sink unit|oven|refrigerator|bottle pull|tandem|drawer unit/.test(n)) return 'kitchen';
  if (/\btv unit\b|sofa frame|crockery|showcase|center table|coffee table|side table/.test(n)) return 'living';
  if (/dining|buffet|sideboard/.test(n))  return 'dining';
  if (/study|desk|computer table|executive|workstation|conference|book shelf|file cabinet/.test(n)) return 'office';
  if (/garden|outdoor|pergola|gazebo/.test(n)) return 'outdoor';
  if (/mandir|pooja/.test(n)) return 'pooja';
  return 'default';
}

// ── VIBRANT colour palettes — each room is clearly distinct ──
var _RP = {
  //          back wall      side walls     floor       ceiling     skirting    accent
  bedroom: { wall:0x7B6BB0, side:0x9080C8, floor:0xC49040, ceil:0xF0ECFF, sk:0x5A4A88, accent:0xD4AF37 },
  kitchen: { wall:0xEDF5ED, side:0xE5F2E5, floor:0xC4C4C4, ceil:0xF5F8F5, sk:0xBBBBBB, accent:0x3A8A4A },
  living:  { wall:0xC06840, side:0xCE7850, floor:0xB07030, ceil:0xFAF0EB, sk:0x884020, accent:0xD4AF37 },
  dining:  { wall:0x2A5838, side:0x346844, floor:0x885028, ceil:0xEAF2EA, sk:0xD4AF37, accent:0xD4AF37 },
  office:  { wall:0x354E6E, side:0x425E7E, floor:0x303C38, ceil:0xE8ECF6, sk:0x243448, accent:0x8AAACE },
  outdoor: { wall:null,     side:null,     floor:0x357A25, ceil:null,     sk:null,     accent:0x60B040 },
  pooja:   { wall:0xC85808, side:0xD86818, floor:0xD4AF37, ceil:0xFFF0B0, sk:0x983800, accent:0xFFD700 },
  default: { wall:0x8A7060, side:0x9A8070, floor:0x988060, ceil:0xF5F2EE, sk:0x786050, accent:0xD4AF37 },
};

function _mat(col, rough, metal) {
  return new THREE.MeshStandardMaterial({ color: col, roughness: rough !== undefined ? rough : 0.85, metalness: metal || 0 });
}

function buildRoom(scene) {
  var rt = getRoomType();
  var c  = _RP[rt] || _RP.default;

  // Room geometry relative to furniture
  var sM  = Math.max(2.0, Furn_L * 0.38);
  var rW  = Furn_L + sM * 2;
  var rH  = Math.max(Furn_H + 2.8, 9.5);
  var bwZ = -(Furn_W / 2 + 0.15);          // back wall z (just behind furniture)
  var fwZ =  Furn_W / 2 + sM * 1.8;        // front extent
  var sD  = fwZ - bwZ;                     // side wall depth
  var lX  = -(Furn_L / 2 + sM);            // left wall x
  var rX  =  (Furn_L / 2 + sM);            // right wall x
  var cZ  =  bwZ + sD / 2;                 // floor/ceiling centre z

  // ── FLOOR ────────────────────────────────────────────────────
  var fRough = rt==='kitchen' ? 0.25 : rt==='office' ? 0.95 : 0.65;
  var flr = new THREE.Mesh(new THREE.PlaneGeometry(rW, sD), _mat(c.floor, fRough, 0.02));
  flr.rotation.x = -Math.PI / 2;
  flr.position.set(0, -0.005, cZ);
  flr.receiveShadow = true;
  scene.add(flr);

  if (!c.wall) {
    // Outdoor — open sky plane behind
    var skyPlane = new THREE.Mesh(new THREE.PlaneGeometry(rW * 4, rH * 3),
      new THREE.MeshStandardMaterial({ color: 0x6EC6F0, emissive: 0x50A8E0, emissiveIntensity: 0.5, roughness: 1 }));
    skyPlane.position.set(0, rH * 0.8, bwZ - 4);
    scene.add(skyPlane);
    return;
  }

  // ── BACK WALL ────────────────────────────────────────────────
  var bw = new THREE.Mesh(new THREE.PlaneGeometry(rW, rH), _mat(c.wall, 0.85));
  bw.position.set(0, rH / 2, bwZ);
  scene.add(bw);

  // ── LEFT WALL ────────────────────────────────────────────────
  var lw = new THREE.Mesh(new THREE.PlaneGeometry(sD, rH), _mat(c.side, 0.85));
  lw.rotation.y = Math.PI / 2;
  lw.position.set(lX, rH / 2, cZ);
  scene.add(lw);

  // ── RIGHT WALL ───────────────────────────────────────────────
  var rw = new THREE.Mesh(new THREE.PlaneGeometry(sD, rH), _mat(c.side, 0.85));
  rw.rotation.y = -Math.PI / 2;
  rw.position.set(rX, rH / 2, cZ);
  scene.add(rw);

  // ── CEILING ──────────────────────────────────────────────────
  var cl = new THREE.Mesh(new THREE.PlaneGeometry(rW, sD), _mat(c.ceil, 0.92));
  cl.rotation.x = Math.PI / 2;
  cl.position.set(0, rH, cZ);
  scene.add(cl);

  // ── SKIRTING BOARDS ──────────────────────────────────────────
  if (c.sk) {
    var skMat = _mat(c.sk, 0.4, rt === 'dining' ? 0.3 : 0.05);
    var sh = 0.1;
    function addSk(geo, x, y, z) { var m = new THREE.Mesh(geo, skMat.clone()); m.position.set(x, y, z); scene.add(m); }
    addSk(new THREE.BoxGeometry(rW,    sh, 0.04),  0,        sh/2, bwZ + 0.02);
    addSk(new THREE.BoxGeometry(0.04, sh, sD),     lX+0.02,  sh/2, cZ);
    addSk(new THREE.BoxGeometry(0.04, sh, sD),     rX-0.02,  sh/2, cZ);
  }

  // ── WINDOW on back wall — ALWAYS above furniture height ───────
  var winW = Math.min(Furn_L * 0.42, 3.2);
  var winH = Math.min(rH * 0.27, 2.5);
  var winY = Math.max(Furn_H + 1.1, rH * 0.74);   // key: always above furniture
  addRoomWindow(scene, 0, winY, bwZ + 0.01, winW, winH);

  // ── CEILING FIXTURE ───────────────────────────────────────────
  addCeilingLight(scene, 0, rH, cZ * 0.2, rt, c.accent);

  // ── FLOOR PATTERNS ───────────────────────────────────────────
  if (rt === 'bedroom' || rt === 'dining') addWoodFloor(scene, rW, sD, bwZ);
  if (rt === 'kitchen')                    addKitchenTiles(scene, rW, sD, bwZ);
  if (rt === 'office')                     addCarpet(scene, rW, sD, bwZ);

  // ─── ROOM-SPECIFIC EXTRAS ────────────────────────────────────

  // KITCHEN
  if (rt === 'kitchen') {
    addBacksplash(scene, bwZ);
    var ucl = new THREE.PointLight(0xFFEA90, 0.55, Furn_L * 2.5);
    ucl.position.set(0, Math.min(Furn_H - 0.3, 2.75), bwZ + 0.5);
    scene.add(ucl);
  }

  // BEDROOM — curtains on LEFT SIDE WALL (not back wall!) so they never overlap wardrobe
  if (rt === 'bedroom') {
    addSideWallCurtains(scene, lX, rH, cZ, sD);
  }

  // LIVING ROOM
  if (rt === 'living') {
    var rug = new THREE.Mesh(new THREE.BoxGeometry(Furn_L * 0.85, 0.022, Furn_W * 0.75), _mat(0x5A2E10, 0.97));
    rug.position.set(0, 0.006, 0); scene.add(rug);
    addFloorLamp(scene, lX + 0.55, fwZ * 0.35, c.accent);
  }

  // DINING ROOM
  if (rt === 'dining') {
    var dRug = new THREE.Mesh(new THREE.BoxGeometry(Furn_L * 0.9, 0.022, Furn_W * 0.85), _mat(0x2A1808, 0.97));
    dRug.position.set(0, 0.006, 0); scene.add(dRug);
    addPendantLight(scene, 0, Furn_H + 1.3, Furn_W * 0.25);
  }

  // OFFICE
  if (rt === 'office') {
    addOfficeShelf(scene, rX - 0.15, rH, bwZ + 0.4);
  }

  // POOJA ROOM
  if (rt === 'pooja') {
    var pRug = new THREE.Mesh(new THREE.BoxGeometry(Furn_L * 0.6, 0.022, Furn_W * 0.55), _mat(0xAA1800, 0.97));
    pRug.position.set(0, 0.006, 0); scene.add(pRug);
    var diyaM = new THREE.MeshStandardMaterial({ color: 0xFF6600, roughness: 0.3, metalness: 0.2, emissive: new THREE.Color(0xFF4400), emissiveIntensity: 0.7 });
    [-0.4, 0, 0.4].forEach(function(dx) {
      var d = new THREE.Mesh(new THREE.SphereGeometry(0.065, 8, 6), diyaM.clone());
      d.position.set(dx, 0.07, Furn_W / 2 - 0.12); scene.add(d);
      var dl = new THREE.PointLight(0xFF8800, 0.65, 2.5);
      dl.position.set(dx, 0.22, Furn_W / 2 - 0.12); scene.add(dl);
    });
  }
}

// ── Window with sky + sunlight ────────────────────────────────
function addRoomWindow(scene, x, y, z, w, h) {
  // White window frame box
  var fr = new THREE.Mesh(new THREE.BoxGeometry(w + 0.18, h + 0.18, 0.08), _mat(0xEEE8D8, 0.35, 0.1));
  fr.position.set(x, y, z - 0.01); scene.add(fr);

  // Bright sky behind (emissive, looks like real daylight)
  var sky = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
    new THREE.MeshStandardMaterial({ color: 0x7EC8F0, emissive: 0x50B0E0, emissiveIntensity: 0.70, roughness: 0 }));
  sky.position.set(x, y, z - 0.025); scene.add(sky);

  // Frosted glass pane
  var glass = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
    new THREE.MeshStandardMaterial({ color: 0xC4E8F8, roughness: 0.01, metalness: 0.05, transparent: true, opacity: 0.25 }));
  glass.position.set(x, y, z + 0.02); scene.add(glass);

  // Cross dividers
  var dm = _mat(0xEEE8D8, 0.38);
  var hd = new THREE.Mesh(new THREE.BoxGeometry(w, 0.05, 0.065), dm);
  hd.position.set(x, y, z + 0.008); scene.add(hd);
  var vd = new THREE.Mesh(new THREE.BoxGeometry(0.05, h, 0.065), dm.clone());
  vd.position.set(x, y, z + 0.008); scene.add(vd);

  // Warm sunlight coming through
  var wl = new THREE.PointLight(0xFFF0C0, 1.05, Math.max(Furn_L, Furn_H) * 5);
  wl.position.set(x, y, z + 2.0); scene.add(wl);
}

// ── Ceiling light fixture ─────────────────────────────────────
function addCeilingLight(scene, x, rH, z, rt, accent) {
  var lcol = { kitchen:0xE0F8FF, office:0xDDE8F8, bedroom:0xFFE8B0, living:0xFFCC60, dining:0xFFBB40, default:0xFFF0C0 };
  var col = lcol[rt] || lcol.default;
  var em = new THREE.MeshStandardMaterial({ color: 0xF0F0F0, roughness: 0.2, metalness: 0.45, emissive: new THREE.Color(col), emissiveIntensity: 0.6 });
  var fix = (rt === 'kitchen' || rt === 'office')
    ? new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.055, 0.36), em)
    : new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.058, 12), em);
  fix.position.set(x, rH - 0.03, z); scene.add(fix);
  if (rt !== 'dining') {
    var pl = new THREE.PointLight(col, 0.88, Math.max(Furn_L, Furn_W, Furn_H) * 4);
    pl.position.set(x, rH - 0.22, z); scene.add(pl);
  }
}

// ── Wood plank lines on floor ─────────────────────────────────
function addWoodFloor(scene, rW, sD, bwZ) {
  var pm = _mat(0x482E0C, 0.24);
  var step = Math.max(0.25, Furn_L / 16);
  for (var px = -rW/2; px < rW/2; px += step) {
    var pl = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.006, sD * 1.05), pm);
    pl.position.set(px, 0.004, bwZ + sD / 2); scene.add(pl);
  }
}

// ── Kitchen ceramic tile grid ─────────────────────────────────
function addKitchenTiles(scene, rW, sD, bwZ) {
  var gm = _mat(0x888888, 0.45);
  var ts = 0.5;
  for (var tx = -rW/2; tx < rW/2; tx += ts) {
    var gx = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.005, sD), gm);
    gx.position.set(tx, 0.003, bwZ + sD/2); scene.add(gx);
  }
  for (var tz = bwZ; tz < bwZ + sD; tz += ts) {
    var gz = new THREE.Mesh(new THREE.BoxGeometry(rW, 0.005, 0.02), gm.clone());
    gz.position.set(0, 0.003, tz); scene.add(gz);
  }
}

// ── Office carpet stripes ─────────────────────────────────────
function addCarpet(scene, rW, sD, bwZ) {
  var sm = _mat(0x283830, 0.99);
  for (var sx = -rW/2; sx < rW/2; sx += 0.5) {
    var s = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.004, sD), sm);
    s.position.set(sx + 0.13, 0.003, bwZ + sD/2); scene.add(s);
  }
}

// ── Kitchen subway tile backsplash ────────────────────────────
function addBacksplash(scene, bwZ) {
  var cTop = Math.min(Furn_H * 0.94, 2.8);
  var endY = Math.min(cTop + 1.8, 4.7);
  if (endY <= cTop + 0.3) return;
  var tW = 0.30, tH = 0.15, gap = 0.012;
  var tM = _mat(0xF2F2F2, 0.20, 0.04);
  var row = 0, sX = -Furn_L / 2 - 0.05;
  for (var ty = cTop + 0.06; ty < endY; ty += tH + gap) {
    var offset = row % 2 === 0 ? 0 : tW / 2;
    for (var tx = sX + offset; tx < sX + Furn_L + 0.05; tx += tW + gap) {
      var t = new THREE.Mesh(new THREE.BoxGeometry(tW, tH, 0.024), tM.clone());
      t.position.set(tx + tW/2, ty + tH/2, bwZ + 0.028); scene.add(t);
    }
    row++;
  }
}

// ── Bedroom: curtains on LEFT SIDE WALL (avoids furniture overlap) ──
function addSideWallCurtains(scene, lX, rH, cZ, sD) {
  var winW = Math.min(sD * 0.38, 2.2);
  var winH = Math.min(rH * 0.28, 2.3);
  var winY = Math.max(Furn_H + 1.1, rH * 0.71);
  var winZ = cZ - sD * 0.08;   // slightly towards back of room

  // Window frame (thin box on left wall face)
  var fr = new THREE.Mesh(new THREE.BoxGeometry(0.08, winH + 0.16, winW + 0.16), _mat(0xEEE8D8, 0.35, 0.1));
  fr.position.set(lX + 0.01, winY, winZ); scene.add(fr);

  // Sky glow
  var sky = new THREE.Mesh(new THREE.PlaneGeometry(winW, winH),
    new THREE.MeshStandardMaterial({ color: 0x7EC8F0, emissive: 0x50B0D8, emissiveIntensity: 0.6, roughness: 0 }));
  sky.rotation.y = Math.PI / 2;
  sky.position.set(lX - 0.01, winY, winZ); scene.add(sky);

  // Glass
  var glass = new THREE.Mesh(new THREE.PlaneGeometry(winW, winH),
    new THREE.MeshStandardMaterial({ color: 0xC8EAF8, transparent: true, opacity: 0.25, roughness: 0.01 }));
  glass.rotation.y = Math.PI / 2;
  glass.position.set(lX + 0.025, winY, winZ); scene.add(glass);

  // Curtain panels — thick boxes clearly visible as drapes
  var cMat = _mat(0x7850A8, 0.97);
  var cH = winH + 1.5;
  var cW = winW * 0.35;
  [-1, 1].forEach(function(side) {
    var cur = new THREE.Mesh(new THREE.BoxGeometry(0.075, cH, cW), cMat.clone());
    cur.position.set(lX + 0.045, winY - 0.18, winZ + side * (winW / 2 + cW / 2 - 0.05));
    scene.add(cur);
  });

  // Gold curtain rod along z-axis
  var rod = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, winW + 1.0, 8), _mat(0xC8A840, 0.22, 0.78));
  rod.rotation.x = Math.PI / 2;
  rod.position.set(lX + 0.055, winY + cH / 2 + 0.06, winZ);
  scene.add(rod);

  // Sunlight from side window
  var wl = new THREE.PointLight(0xFFF5CC, 0.95, Math.max(Furn_L, Furn_H) * 4.5);
  wl.position.set(lX + 1.8, winY, winZ);
  scene.add(wl);
}

// ── Dining gold pendant light ─────────────────────────────────
function addPendantLight(scene, x, y, z) {
  var pm = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.12, metalness: 0.88, emissive: new THREE.Color(0xFFCC40), emissiveIntensity: 0.55 });
  var shade = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.25, 0.28, 12), pm);
  shade.position.set(x, y, z); scene.add(shade);
  var wire = new THREE.Mesh(new THREE.CylinderGeometry(0.013, 0.013, 0.65, 6), pm.clone());
  wire.position.set(x, y + 0.47, z); scene.add(wire);
  var light = new THREE.PointLight(0xFFDD80, 1.6, 12);
  light.position.set(x, y - 0.16, z); scene.add(light);
}

// ── Living room floor lamp ────────────────────────────────────
function addFloorLamp(scene, x, z, accentColor) {
  var stemM = _mat(accentColor || 0xC8A848, 0.18, 0.82);
  scene.add(Object.assign(new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.042, 1.62, 8), stemM), {}).position.set(x, 0.81, z));
  var stem = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.042, 1.62, 8), stemM);
  stem.position.set(x, 0.81, z); scene.add(stem);
  var base = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.21, 0.065, 10), stemM.clone());
  base.position.set(x, 0.032, z); scene.add(base);
  var shadeM = new THREE.MeshStandardMaterial({ color: 0xFFF0B8, roughness: 0.82, metalness: 0, emissive: new THREE.Color(0xFFE080), emissiveIntensity: 0.35, transparent: true, opacity: 0.82 });
  var shade = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.24, 0.34, 10), shadeM);
  shade.position.set(x, 1.76, z); scene.add(shade);
  var fl = new THREE.PointLight(0xFFE080, 0.75, 6);
  fl.position.set(x, 1.62, z); scene.add(fl);
}

// ── Office bookshelf on side wall ────────────────────────────
function addOfficeShelf(scene, x, rH, z) {
  var shM = _mat(0x3A2A18, 0.6);
  var shH = rH * 0.44, shD = 0.42;
  var body = new THREE.Mesh(new THREE.BoxGeometry(0.085, shH, shD), shM);
  body.position.set(x, shH / 2 + 0.5, z); scene.add(body);
  var bkCols = [0xC0392B, 0x2980B9, 0x27AE60, 0xF39C12, 0x8E44AD, 0xE67E22, 0x16A085, 0xD35400];
  for (var i = 0; i < 3; i++) {
    for (var j = 0; j < 3; j++) {
      var bk = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.20 + j * 0.03, 0.30 + j * 0.02), _mat(bkCols[(i*3+j) % bkCols.length], 0.88));
      bk.position.set(x - 0.04, 0.75 + i * 0.52, z + (j - 1) * 0.1);
      scene.add(bk);
    }
  }
}

