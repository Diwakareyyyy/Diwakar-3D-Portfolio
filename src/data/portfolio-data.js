/**
 * ==============================================================================
 * CENTRALIZED PORTFOLIO DATA CONFIGURATION
 * ==============================================================================
 * This is the SINGLE SOURCE OF TRUTH for all editable content in this portfolio:
 *   - Profile, Biography & Contact Details
 *   - Home / Intro Labels & Headings
 *   - Technical Skills & Tools (11 interactive 3D nodes)
 *   - Journey & Milestones (2023–2027 Timeline)
 *   - Work Experience (Infologia Technologies Internship)
 *   - Projects (15 Spatial Showcase Projects)
 *   - Certifications (5 Holographic Credentials)
 *   - Audio Configuration (Music & Footsteps)
 *
 * To edit any text, title, project, certificate, or contact link, simply update
 * the values in this file. Changes take effect across all scenes and components.
 * ==============================================================================
 */

export const PROFILE = {
  name: 'S DIWAKAR',
  shortName: 'Diwakar S',
  role: 'Software Developer',
  tagline: 'SOFTWARE DEVELOPER | CREATIVE DEVELOPER | 3D TECHNOLOGIST',
  titles: {
    primary: 'SOFTWARE DEVELOPER',
    secondary: 'Creative Developer | 3D Technologist',
  },
  degree: 'Bachelor of Engineering in Computer Science and Engineering',
  college: 'Peri Institute of Technology',
  graduationPeriod: '2023–2027',
  cgpa: '8.40',
  headline: 'Software Developer · Creative Technologist',
  intro:
    'Computer Science undergraduate experienced in building modern web, mobile, and interactive 3D digital experiences with Python, React & Flutter.',
  careerObjective:
    'Graduating with a BE in CSE and beginning my professional journey as a Software Developer.',
  technicalInterests:
    'Full-Stack Development · Mobile & Flutter · Interactive Systems · AI Integration',
  contact: {
    email: 'sdiwakar2005s@gmail.com',
    phone: '+918608885338',
    phoneFormatted: '+91 8608885338',
    linkedin: 'https://www.linkedin.com/in/s-diwakar-164169291/',
    github: 'https://github.com/Diwakareyyyy',
    resumePdf: 'public/resume.pdf',
    resumeDownloadName: 'Diwakar_S_Resume.pdf',
  },
  achievements: [
    {
      title: 'Smart India Hackathon 2025',
      result: 'Finalist / Innovator',
    },
    {
      title: 'National Badminton',
      result: 'Silver Medalist',
    },
  ],
};

export const HOME = {
  welcome: '– Welcome to the World of –',
  chips: {
    artist: '•S Diwakar•',
    legend: '•Software Dev•',
  },
  roles: ['Creative', 'Software', 'Developer'],
  fallbackSubtitle: 'Software Developer & Creative Technologist',
};

export const SKILLS = [
  { id: 'python', name: 'Python', category: 'Backend & AI Systems', icon: 'public/tools/python.svg' },
  { id: 'sql', name: 'SQL', category: 'Relational Databases', icon: 'public/tools/sql.svg' },
  { id: 'react', name: 'React', category: 'Frontend Web Framework', icon: 'public/tools/react.svg' },
  { id: 'antigravity', name: 'Antigravity', category: 'Development Tooling', icon: 'public/tools/antigravity.svg' },
  { id: 'flutter', name: 'Flutter', category: 'Cross-Platform Mobile UI', icon: 'public/tools/flutter.svg' },
  { id: 'vercel', name: 'Vercel', category: 'Cloud Deployment & CI/CD', icon: 'public/tools/vercel.svg' },
  { id: 'cpp', name: 'C++', category: 'High-Performance Systems', icon: 'public/tools/cpp.svg' },
  { id: 'github', name: 'GitHub', category: 'Version Control & DevOps', icon: 'public/tools/github.svg' },
  { id: 'html', name: 'HTML5', category: 'Web Standards & DOM', icon: 'public/tools/html.svg' },
  { id: 'figma', name: 'Figma', category: 'UI/UX Interface Design', icon: 'public/tools/figma.svg' },
  { id: 'claude', name: 'Claude', category: 'AI Engineering & Prompting', icon: 'public/tools/claude.svg' },
];

export const JOURNEY = [
  {
    year: '2023',
    key: 'Academic Foundation',
    badge: 'academic',
    lines: [
      'Started BE in Computer Science',
      'Developing Technical Foundation',
      'Exploring Programming & Tech',
    ],
    desc: 'Started my BE in Computer Science and Engineering journey. Began developing my technical foundation and exploring the world of programming and technology.',
    image: '2023',
  },
  {
    year: '2024',
    key: 'Project Development',
    badge: 'laptop',
    lines: [
      'Ideas to Practical Software',
      'Core Programming Concepts',
      'Software Problem-Solving',
    ],
    desc: 'Started learning how to transform ideas into practical software projects. Explored project development, programming concepts, and problem-solving.',
    image: '2024',
  },
  {
    year: '2025',
    key: 'Hackathon Experience',
    badge: 'hackathon',
    lines: [
      'Smart India Hackathon 2025',
      'Collaborative Teamwork',
      'Real-World Problem Solving',
    ],
    desc: 'Participated in Smart India Hackathon 2025. Gained valuable exposure to innovation, teamwork, technical problem-solving, and developing solutions for real-world challenges.',
    image: '2025',
  },
  {
    year: '2026',
    key: 'Practical Dev & Internship',
    badge: 'flutter',
    lines: [
      'Infologia Technologies Intern',
      'Flutter & Dart Expense App',
      '2–3 College Software Projects',
    ],
    desc: 'Worked as a Software Developer Intern at Infologia Technologies from July to August 2026 on a Flutter/Dart expense tracking app, alongside building college software projects.',
    image: '2026',
  },
  {
    year: '2027',
    key: 'Professional Vision',
    badge: 'vision',
    lines: [
      'BE CSE Graduation Goal',
      'Software Developer Ambition',
      'Future Professional Journey',
    ],
    desc: 'Targeting graduation with a BE in Computer Science and Engineering, aiming to begin a professional software development career and contribute to impactful tech products.',
    image: '2027',
  },
];

export const EXPERIENCES = [
  {
    id: 'infologia-internship-2026',
    role: 'SOFTWARE DEVELOPER INTERN',
    company: 'Infologia Technologies',
    legalName: 'Infologia Technologies',
    period: 'July 2026 – August 2026',
    durationLabel: 'July 2026 – August 2026',
    type: 'Internship',
    projectTitle: 'Smart Expense Tracker Application',
    summary:
      'Worked on a cross-platform Smart Expense Tracker application using Flutter and Dart. Contributed to responsive and reusable UI components, expense-management features, and application testing.',
    previewImage: 'public/experience/expense_app_preview.png',
    buildingSketch: 'public/experience/office_sketch_startup.png',
    developerFig: 'public/experience/developer_facing_building.png',
    isPlaceholder: false,
    responsibilities: [
      'Worked on a cross-platform Smart Expense Tracker application using Flutter and Dart.',
      'Contributed to responsive and reusable UI components, expense-management features, and application testing.',
    ],
    stack: [
      'Flutter',
      'Dart',
      'Cross-Platform UI',
      'State Management',
      'Testing & QA',
    ],
  },
];

export const PROJECTS = [
  // ROW 1: PROJECTS 1 TO 6 (Moving Right to Left)
  {
    id: 'p01_evcdrp',
    number: '01',
    name: 'EVRouteX',
    shortDesc: 'Optimized route planning for electric vehicles.',
    category: 'EV Logistics & Route Optimization',
    desc: 'An intelligent EV delivery route optimization system that considers battery constraints, vehicle load, driving range, traffic conditions, and charging requirements to generate efficient delivery routes.',
    problem: 'Standard navigation applications do not account for EV battery depletion under varied payload weights, elevation changes, dynamic traffic congestion, and specialized charging station plug availability.',
    solution: 'EVRouteX implements multi-parameter graph routing algorithms that evaluate real-time battery constraints, charging curve models, and payload weights to generate reliable, range-safe delivery routes.',
    features: [
      'Constraint-aware battery consumption modeling',
      'Dynamic route re-planning with charging stops',
      'Payload and elevation impact calculations',
      'Real-time charging station availability tracking'
    ],
    technologies: ['Python', 'FastAPI', 'Graph Algorithms', 'OpenStreetMap', 'Leaflet.js'],
    image: 'public/projects/1.jpg',
    github: 'https://github.com/Diwakareyyyy/EVRouteX',
    demo: '#',
    row: 1,
    featured: true
  },
  {
    id: 'p03_cloud',
    number: '02',
    name: 'Personalized Cloud',
    shortDesc: 'Personalized cloud storage with secure access from anywhere.',
    category: 'Cloud Storage & Secure Access',
    desc: 'A personalized cloud storage platform that provides individual storage allocation and allows users to securely upload, store, and access their files from anywhere.',
    problem: 'Public cloud storage platforms impose restrictive tier limits, privacy concerns, and lack tailored access control for personalized cross-device storage ecosystems.',
    solution: 'Personalized Cloud provides encrypted individual storage quotas, chunked multi-threaded file uploads, zero-knowledge security, and responsive media streaming from any connected client.',
    features: [
      'Client-side AES encryption and token auth',
      'Chunked resumable file upload pipeline',
      'Cross-platform file explorer interface',
      'Automated deduplication and storage quotas'
    ],
    technologies: ['React', 'Node.js', 'Express', 'SQLite', 'Docker', 'Web Crypto API'],
    image: 'public/projects/2.jpg',
    github: 'https://github.com/Diwakareyyyy/Personalized-Cloud',
    demo: '#',
    row: 1,
    featured: true
  },
  {
    id: 'p02_expense',
    number: '03',
    name: 'Smart AI Expense Tracker',
    shortDesc: 'Smart expense management with AI-powered features.',
    category: 'Flutter & Financial Intelligence',
    desc: 'A Flutter-based expense management application featuring OCR-powered receipt scanning, automated expense entry, expense categorization, and payment application integration.',
    problem: 'Manual expense entry is tedious, error-prone, and leads to inconsistent personal financial tracking across multiple bank accounts and physical cash receipts.',
    solution: 'Smart AI Expense Tracker combines on-device OCR receipt parsing, natural language expense logging, predictive spending analytics, and automated multi-currency budgeting.',
    features: [
      'On-device OCR receipt extraction and itemization',
      'AI-assisted expense categorization and anomaly alerts',
      'Interactive visual breakdown charts and monthly targets',
      'Exportable accounting reports in PDF and CSV formats'
    ],
    technologies: ['Flutter', 'Dart', 'Google ML Kit', 'SQLite', 'Provider', 'Python'],
    image: 'public/projects/3.jpg',
    github: 'https://github.com/Diwakareyyyy/Smart-AI-Expense-Tracker',
    demo: '#',
    row: 1,
    featured: true
  },
  {
    id: 'p10_drdms',
    number: '04',
    name: 'Disaster Relief Distribution Tracking System',
    shortDesc: 'Tracks inventory and relief distribution during disaster response.',
    category: 'Logistics & Humanitarian Tech',
    desc: 'A real-time humanitarian supply tracking platform enabling relief agencies to monitor warehouse reserves, dispatch vehicle manifests, and verify last-mile distribution using digital acknowledgments.',
    problem: 'During disaster emergencies, lack of transparent logistics coordination leads to critical relief supply hoarding, inventory mismatches, and delayed delivery to hard-hit zones.',
    solution: 'A transparent supply chain network that synchronizes dispatch manifests, maps delivery routes with offline resiliency, and records verified aid distribution at relief camps.',
    features: [
      'Real-time warehouse inventory and depletion monitoring',
      'Disaster dispatch route coordination and GPS tracking',
      'Digital proof-of-delivery and recipient verification',
      'Role-based access for relief agencies and emergency squads'
    ],
    technologies: ['React', 'Node.js', 'MongoDB', 'Socket.io', 'Express', 'Tailwind CSS'],
    image: 'public/projects/4.jpg',
    github: 'https://github.com/Diwakareyyyy/Disaster-Relief-Tracking',
    demo: '#',
    row: 1,
    featured: true
  },
  {
    id: 'p06_perry',
    number: '05',
    name: 'Peri Chatbot',
    shortDesc: 'An unsupervised chatbot project.',
    category: 'Conversational AI & NLP',
    desc: 'An unsupervised conversational chatbot system built to understand and resolve student queries across campus regulations, course schedules, and academic workflows autonomously.',
    problem: 'Traditional rule-based chatbots fail to generalize across unstructured student inquiries and require costly manual intent annotation for campus knowledge retrieval.',
    solution: 'Peri Chatbot utilizes unsupervised semantic clustering, dense vector embeddings, and retrieval-augmented generation to answer diverse academic and campus queries autonomously.',
    features: [
      'Unsupervised intent discovery and vector clustering',
      'Semantic document retrieval for college FAQs',
      'Contextual multi-turn dialogue management',
      'Lightweight API backend for seamless web integration'
    ],
    technologies: ['Python', 'NLTK', 'scikit-learn', 'FastAPI', 'Vector Embeddings'],
    image: 'public/projects/5.jpg',
    github: 'https://github.com/Diwakareyyyy/Peri-Chatbot',
    demo: '#',
    row: 1,
    featured: false
  },
  {
    id: 'p13_clfms',
    number: '06',
    name: 'Campus Lost & Found',
    shortDesc: 'Helps students report, find, and recover lost items on campus.',
    category: 'Campus Automation & Community Web',
    desc: 'A centralized digital lost-and-found system for university students and administrative staff to report, locate, claim, and recover misplaced personal items on campus.',
    problem: 'Lost student property on university campuses is frequently misplaced permanently due to fragmented notice boards and lack of verified claim systems.',
    solution: 'A unified campus portal where students report found or missing items with photographic evidence, search categorized listings, and safely arrange verified campus handovers.',
    features: [
      'Verified student login and item cataloging',
      'Image upload with keyword and location tagging',
      'Claim verification protocol with contact masking',
      'Status tracking from report to successful return'
    ],
    technologies: ['React', 'Python', 'Flask', 'SQL', 'Bootstrap', 'Cloudinary'],
    image: 'public/projects/6.jpg',
    github: 'https://github.com/Diwakareyyyy/Campus-Lost-Found',
    demo: '#',
    row: 1,
    featured: false
  },

  // ROW 2: PROJECTS 7 TO 12 (Moving Left to Right)
  {
    id: 'p14_marketplace',
    number: '07',
    name: 'Campus Book Sale & Exchange',
    shortDesc: 'A platform for students to sell and exchange books within their campus.',
    category: 'Campus Peer Commerce',
    desc: 'A dedicated peer-to-peer textbook marketplace enabling students within the same campus to list, trade, sell, or donate academic course books directly without intermediary fees.',
    problem: 'Engineering and academic textbooks are expensive and often sit unused after semester exams while junior students struggle to find affordable copies locally.',
    solution: 'An intuitive campus marketplace connecting buyers and sellers directly within departments, facilitating quick cash or exchange transactions between semesters.',
    features: [
      'Course code and department book filtering',
      'In-app student chat and price negotiations',
      'Listing condition rating with cover photos',
      'Free exchange and donation designation flags'
    ],
    technologies: ['Flutter', 'Dart', 'Firebase', 'Cloud Firestore', 'Material 3'],
    image: 'public/projects/7.jpg',
    github: 'https://github.com/Diwakareyyyy/Campus-Book-Exchange',
    demo: '#',
    row: 2,
    featured: false
  },
  {
    id: 'p09_glitch',
    number: '08',
    name: 'Glitchyugam 2026',
    shortDesc: 'An animated symposium website for college events.',
    category: 'Creative Web & Event Platform',
    desc: 'The official digital portal for the national-level inter-college symposium Glitchyugam 2026, delivering interactive cyberpunk visuals, event agendas, and participant registration workflows.',
    problem: 'Annual national college symposiums require an engaging, high-energy digital identity to showcase events, schedules, rules, and coordinate hundreds of participant registrations.',
    solution: 'An interactive cyberpunk-themed symposium website featuring custom WebGL glitch shaders, dynamic sound reactive UI animations, and automated team registration workflows.',
    features: [
      'WebGL glitch and chromatic aberration shaders',
      'Interactive event timeline and rulebook downloads',
      'Automated participant ticket generation and QR codes',
      'Live countdown and schedule sync across mobile viewports'
    ],
    technologies: ['HTML5', 'CSS3', 'JavaScript', 'WebGL', 'GSAP', 'Vercel'],
    image: 'public/projects/8.jpg',
    github: 'https://github.com/Diwakareyyyy/Glitchyugam-2026',
    demo: '#',
    row: 2,
    featured: false
  },
  {
    id: 'p07_icicdt',
    number: '09',
    name: 'ICICDT 2026',
    shortDesc: 'An international conference website developed for a college conference.',
    category: 'Academic Conference Systems',
    desc: 'The official web portal developed for the International Conference on Information, Communication, and Digital Technologies (ICICDT 2026).',
    problem: 'International academic conferences need an authoritative, accessible platform to handle paper submissions, peer reviewer guidelines, keynote speaker itineraries, and delegate passes.',
    solution: 'Developed the official web portal for ICICDT 2026, delivering indexed track agendas, speaker directories, submission deadlines, and responsive registration capabilities.',
    features: [
      'Research track indexing and call-for-papers portal',
      'Keynote speaker and organizing committee galleries',
      'Responsive conference schedule and location maps',
      'Secure delegate inquiry and registration pipeline'
    ],
    technologies: ['React', 'JavaScript', 'Tailwind CSS', 'Vite', 'Responsive Web'],
    image: 'public/projects/9.jpg',
    github: 'https://github.com/Diwakareyyyy/ICICDT-2026',
    demo: '#',
    row: 2,
    featured: false
  },
  {
    id: 'p08_baimmozhi',
    number: '10',
    name: 'Peripaayumoli',
    shortDesc: 'A college culturals and events website.',
    category: 'Cultural Showcase & Media Hub',
    desc: 'An expressive cultural festival website developed for college cultural celebrations, highlighting dance, music, drama, art events, schedules, and live scoring.',
    problem: 'Annual cultural fests need vibrant multimedia coverage, stage slot bookings, performer showcases, and live score announcements across multi-venue campus auditoriums.',
    solution: 'Built an immersive cultural web experience featuring rich video backdrops, event scoring leaderboards, performance registrations, and festival highlight archives.',
    features: [
      'Dynamic event schedules and multi-stage venue locator',
      'Live festival announcements and winner highlights',
      'Embedded media gallery and promotional teasers',
      'Mobile-first registration for solo and group events'
    ],
    technologies: ['HTML5', 'CSS3', 'JavaScript', 'Vercel', 'Figma'],
    image: 'public/projects/10.jpg',
    github: 'https://github.com/Diwakareyyyy/Peripaayumoli',
    demo: '#',
    row: 2,
    featured: false
  },
  {
    id: 'p12_cir',
    number: '11',
    name: 'Civic Issue Reporter',
    shortDesc: 'Enables citizens to report public issues and allows authorities to review reported problems.',
    category: 'Civic Tech & Public Systems',
    desc: 'A full-stack municipal issue reporting platform where citizens geotag and submit public infrastructure problems while civic departments prioritize, resolve, and update status.',
    problem: 'Civic complaints regarding road potholes, sanitation hazards, and streetlighting failures often go unaddressed due to lack of transparent logging and department routing.',
    solution: 'A transparent civic reporting platform where citizens geotag and photograph municipal issues, while civic administrators review, triage, update resolution stages, and notify residents.',
    features: [
      'Geotagged issue submission with photo attachments',
      'Status lifecycle tracking from Reported to Resolved',
      'Administrative dashboard for municipal department assignment',
      'Public resolution feed with before/after comparisons'
    ],
    technologies: ['React', 'Node.js', 'Express', 'PostgreSQL', 'Mapbox API'],
    image: 'public/projects/11.jpg',
    github: 'https://github.com/Diwakareyyyy/Civic-Issue-Reporter',
    demo: '#',
    row: 2,
    featured: false
  },
  {
    id: 'p05_vehiclegpt',
    number: '12',
    name: 'Vehicle GPT',
    shortDesc: 'An AI vehicle assistant designed to operate without cloud dependency.',
    category: 'Edge AI & Automotive Telemetry',
    desc: 'An on-device AI automotive assistant that analyzes vehicle sensor telemetry, decodes diagnostic trouble codes (DTC), and answers vehicle queries completely offline.',
    problem: 'Connected vehicle assistants lose functionality in remote highways, tunnels, and low-connectivity regions where cloud reliance causes latency or total service failure.',
    solution: 'Vehicle GPT operates a quantized on-device language model and OBD-II telemetry parser directly on embedded automotive hardware, providing instant voice guidance completely offline.',
    features: [
      'Zero-cloud on-device quantized model inference',
      'Real-time OBD-II engine diagnostic interpretation',
      'Voice-activated vehicle controls and safety manuals',
      'Offline trip efficiency and maintenance forecasting'
    ],
    technologies: ['Python', 'C++', 'Quantized LLM', 'ONNX Runtime', 'OBD-II Telemetry'],
    image: 'public/projects/12.jpg',
    github: 'https://github.com/Diwakareyyyy/Vehicle-GPT',
    demo: '#',
    row: 2,
    featured: true
  }
];

export const CERTIFICATES = [
  {
    id: 'cert-01',
    number: '01',
    title: 'Prompt Engineering Workshop',
    category: 'Generative AI & Prompt Engineering',
    issuer: 'PrepInsta Prime Campus Club',
    date: 'July 2025',
    status: 'VERIFIED',
    credentialId: 'PREP-PE-2025-0707',
    image: 'public/certs/cert_prepinsta_prompt_engineering.jpg',
    verifyUrl: '#'
  },
  {
    id: 'cert-02',
    number: '02',
    title: 'Software Developer Internship (AI Developer Intern)',
    category: 'Software & AI Development',
    issuer: 'Infologia Technologies Pvt Ltd',
    date: 'August 2026',
    status: 'VERIFIED',
    credentialId: 'INF-AIDEV-2026-0813',
    image: 'public/certs/cert_infologia_internship.jpg',
    verifyUrl: '#'
  },
  {
    id: 'cert-03',
    number: '03',
    title: 'Full Stack Development BootCamp',
    category: 'Full Stack Web Engineering',
    issuer: 'NoviTech R&D Pvt Ltd',
    date: 'January 2025',
    status: 'VERIFIED',
    credentialId: 'NT-FSDB300-2025',
    image: 'public/certs/cert_novitech_fullstack.jpg',
    verifyUrl: '#'
  },
  {
    id: 'cert-04',
    number: '04',
    title: 'Smart India Hackathon 2025 (Grand Finale)',
    category: 'National Hackathon Grand Finale',
    issuer: 'Ministry of Education & AICTE',
    date: 'December 2025',
    status: 'VERIFIED',
    credentialId: 'SIH-2025-FINALE',
    image: 'public/certs/cert_sih_2025.jpg',
    verifyUrl: '#'
  },
  {
    id: 'cert-05',
    number: '05',
    title: "ICEECT'24 International Conference",
    category: 'Research Paper Presentation & AI',
    issuer: 'PERI Institute of Technology',
    date: 'April 2024',
    status: 'VERIFIED',
    credentialId: 'PERI-ICEECT-2024-0427',
    image: 'public/certs/cert_iceect_2024.jpg',
    verifyUrl: '#'
  }
];

export const AUDIO_CONFIG = {
  // Strict Audio Policy: Initial walking character intro footsteps ONLY.
  // Background music, ambient music, whoosh, click SFX and transitions are completely removed.
  music: null,
  musicFallbacks: [],
  // Intro boot footstep sounds (synchronized to walking character)
  stepL: 'public/audio/boot_step_left.wav',
  stepR: 'public/audio/boot_step_right.wav',
};
