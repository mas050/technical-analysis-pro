# Quick Customization Guide

## 🎨 Change Colors (5 minutes)

**File:** `/src/index.css`

```css
:root {
  /* Change primary color */
  --primary: #6366f1;        /* Your color here */
  --primary-light: #818cf8;  /* Lighter shade */
  
  /* Change secondary color */
  --secondary: #ec4899;      /* Your color here */
  
  /* Change success color */
  --success: #10b981;        /* Your color here */
}
```

## 🌈 Change Gradients (5 minutes)

**File:** `/src/index.css`

```css
:root {
  /* Main gradient (buttons, headers) */
  --gradient-primary: linear-gradient(135deg, #START 0%, #END 100%);
  
  /* Secondary gradient */
  --gradient-secondary: linear-gradient(135deg, #START 0%, #END 100%);
  
  /* Success gradient */
  --gradient-success: linear-gradient(135deg, #START 0%, #END 100%);
}
```

## 💫 Adjust Particle Count (2 minutes)

**File:** `/src/components/AnimatedBackground.js` - Line 14

```javascript
const particleCount = isMobile ? 10 : 20; // Change these numbers
```

## 🎭 Adjust Glassmorphism Opacity (2 minutes)

**File:** `/src/index.css`

```css
:root {
  /* More transparent (0.01-0.05) */
  --glass-bg: rgba(255, 255, 255, 0.05);
  
  /* More opaque (0.1-0.2) */
  --glass-bg: rgba(255, 255, 255, 0.15);
}
```

## ⚡ Adjust Animation Speeds (5 minutes)

**Orb Float Speed:**
`/src/components/AnimatedBackground.css` - Lines 20-30
```css
.orb-1 {
  animation-duration: 20s; /* Higher = slower */
}
```

**Particle Rise Speed:**
`/src/components/AnimatedBackground.css` - Line 75
```css
.particle {
  animation-duration: 25s; /* Higher = slower */
}
```

**Gradient Shift Speed:**
`/src/components/LandingPage.css` - Line 64
```css
animation: gradient-shift 5s ease infinite; /* Change 5s */
```

**Progress Shimmer Speed:**
`/src/components/AnalysisProgress.css` - Line 189
```css
animation: progressShimmer 1.5s infinite; /* Change 1.5s */
```

## 🔆 Adjust Blur Intensity (2 minutes)

**Global Blur:**
All `.css` files with `backdrop-filter`
```css
backdrop-filter: blur(20px); /* 10-40px recommended */
```

## 🎯 Disable Parallax Scrolling (1 minute)

**File:** `/src/components/AnimatedBackground.js`

Comment out lines 45-58:
```javascript
// const handleScroll = () => {
//   ...
// };
// window.addEventListener('scroll', handleScroll);
```

## 📱 Adjust Mobile Breakpoints (5 minutes)

**Files:** All `.css` files

```css
/* Change breakpoint */
@media (max-width: 768px) { /* Change 768px */
  /* Mobile styles */
}
```

## 🎨 Change Background Orb Colors (5 minutes)

**File:** `/src/components/AnimatedBackground.css`

```css
.orb-1 {
  background: radial-gradient(circle, rgba(R, G, B, 0.8) 0%, rgba(R, G, B, 0) 70%);
}
```

Example colors:
- Purple: `rgba(102, 126, 234, 0.8)`
- Pink: `rgba(236, 72, 153, 0.7)`
- Blue: `rgba(59, 130, 246, 0.7)`
- Green: `rgba(16, 185, 129, 0.6)`

## 🔧 Performance Optimization

**Reduce for slower devices:**

1. **Fewer particles:** Change to 5-10 (AnimatedBackground.js line 14)
2. **Less blur:** Change to 10-15px (all backdrop-filter)
3. **Disable parallax:** Comment out scroll handler
4. **Smaller orbs:** Reduce width/height in AnimatedBackground.css

## 🎬 Add/Remove Orbs (10 minutes)

**Add Orb:**

1. In `/src/components/AnimatedBackground.js`:
```jsx
<div className="orb orb-5"></div>
```

2. In `/src/components/AnimatedBackground.css`:
```css
.orb-5 {
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(255, 100, 200, 0.7) 0%, rgba(255, 100, 200, 0) 70%);
  top: 60%;
  right: 10%;
  animation-delay: 18s;
  animation-duration: 28s;
}
```

## 🎨 Preset Color Schemes

### Ocean Theme
```css
--primary: #0ea5e9;
--secondary: #06b6d4;
--gradient-primary: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
```

### Sunset Theme
```css
--primary: #f97316;
--secondary: #ec4899;
--gradient-primary: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
```

### Forest Theme
```css
--primary: #10b981;
--secondary: #059669;
--gradient-primary: linear-gradient(135deg, #10b981 0%, #059669 100%);
```

### Midnight Theme
```css
--primary: #8b5cf6;
--secondary: #6366f1;
--gradient-primary: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
```

## 🚀 Quick Test

After making changes:
```bash
cd frontend
npm start
```

Open `http://localhost:3000` to see your changes!

---

**Need more details?** See `DESIGN_IMPLEMENTATION_GUIDE.md`
