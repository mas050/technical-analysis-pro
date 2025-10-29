# CSS Variables Reference

Quick reference for all CSS custom properties used in the design system.

## 🎨 Colors

### Primary Colors
```css
--primary: #6366f1;           /* Main brand color */
--primary-light: #818cf8;     /* Lighter variant */
--primary-dark: #4f46e5;      /* Darker variant */
```

### Secondary Colors
```css
--secondary: #ec4899;         /* Accent color */
--secondary-light: #f472b6;   /* Lighter variant */
```

### Status Colors
```css
--success: #10b981;           /* Success/complete states */
--success-light: #34d399;     /* Lighter variant */
--warning: #f59e0b;           /* Warning states */
--error: #ef4444;             /* Error states */
```

---

## 🌈 Gradients

### Primary Gradients
```css
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Used in: Buttons, headers, text */

--gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
/* Used in: Accent elements */

--gradient-success: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
/* Used in: Success states */
```

### Specialized Gradients
```css
--gradient-purple-pink: linear-gradient(135deg, #667eea 0%, #ec4899 100%);
/* Used in: Hero text, special headings */

--gradient-blue-purple: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
/* Used in: Alternative elements */
```

---

## 💎 Glassmorphism

### Background Opacity
```css
--glass-bg: rgba(255, 255, 255, 0.05);           /* Very transparent */
--glass-bg-light: rgba(255, 255, 255, 0.1);      /* Slightly more opaque */
--glass-bg-dark: rgba(0, 0, 0, 0.1);             /* Dark variant */
```

### Borders
```css
--glass-border: rgba(255, 255, 255, 0.1);        /* Subtle border */
--glass-border-light: rgba(255, 255, 255, 0.2);  /* More visible border */
```

### Usage Example
```css
.glass-element {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
}
```

---

## 🌑 Shadows

### Standard Shadows
```css
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);       /* Small shadow */
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.2);      /* Medium shadow */
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.3);      /* Large shadow */
--shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.4);     /* Extra large shadow */
```

### Glow Shadows
```css
--shadow-glow: 0 0 40px rgba(102, 126, 234, 0.3);         /* Primary glow */
--shadow-glow-pink: 0 0 40px rgba(236, 72, 153, 0.3);     /* Pink glow */
--shadow-glow-success: 0 0 40px rgba(16, 185, 129, 0.3);  /* Success glow */
```

### Usage Example
```css
.button:hover {
  box-shadow: var(--shadow-lg), var(--shadow-glow);
}
```

---

## 📏 Spacing

```css
--spacing-xs: 0.5rem;    /* 8px */
--spacing-sm: 1rem;      /* 16px */
--spacing-md: 1.5rem;    /* 24px */
--spacing-lg: 2rem;      /* 32px */
--spacing-xl: 3rem;      /* 48px */
```

### Usage Example
```css
.container {
  padding: var(--spacing-lg);
  gap: var(--spacing-md);
}
```

---

## 🔲 Border Radius

```css
--radius-sm: 8px;        /* Small radius */
--radius-md: 12px;       /* Medium radius */
--radius-lg: 16px;       /* Large radius */
--radius-xl: 20px;       /* Extra large radius */
--radius-full: 9999px;   /* Fully rounded (pills, circles) */
```

### Usage Example
```css
.card {
  border-radius: var(--radius-lg);
}

.button {
  border-radius: var(--radius-full);
}
```

---

## ⚡ Transitions

```css
--transition-fast: 0.15s ease;    /* Quick transitions */
--transition-base: 0.3s ease;     /* Standard transitions */
--transition-slow: 0.5s ease;     /* Slow transitions */
```

### Usage Example
```css
.interactive-element {
  transition: all var(--transition-base);
}

.quick-feedback {
  transition: transform var(--transition-fast);
}
```

---

## 🎯 Common Combinations

### Glassmorphic Card
```css
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--spacing-lg);
}
```

### Primary Button
```css
.primary-button {
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-glow);
  padding: var(--spacing-sm) var(--spacing-lg);
  transition: all var(--transition-base);
}

.primary-button:hover {
  box-shadow: var(--shadow-lg), var(--shadow-glow);
}
```

### Gradient Text
```css
.gradient-heading {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Input Field
```css
.input-field {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-sm);
  transition: all var(--transition-base);
}

.input-field:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), var(--shadow-glow);
}
```

---

## 🔄 How to Override

### Method 1: Inline Override
```css
.custom-element {
  background: var(--glass-bg);
  --glass-bg: rgba(255, 255, 255, 0.15); /* Local override */
}
```

### Method 2: Global Override
In your CSS file, after importing:
```css
:root {
  --primary: #your-color;
  --gradient-primary: linear-gradient(135deg, #start 0%, #end 100%);
}
```

### Method 3: Component-Specific
```css
.special-section {
  --spacing-lg: 3rem; /* Override just for this section */
}
```

---

## 📊 Variable Usage Map

| Variable | Used In | Count |
|----------|---------|-------|
| `--gradient-primary` | Buttons, Headers, Text | 15+ |
| `--glass-bg` | All containers | 20+ |
| `--shadow-glow` | Buttons, Cards on hover | 10+ |
| `--radius-lg` | Cards, Containers | 12+ |
| `--transition-base` | All interactive elements | 30+ |
| `--primary` | Borders, Icons, Text | 8+ |

---

## 🎨 Color Palette Visual

```
Primary Colors:
████ #6366f1 (--primary)
████ #818cf8 (--primary-light)
████ #4f46e5 (--primary-dark)

Secondary Colors:
████ #ec4899 (--secondary)
████ #f472b6 (--secondary-light)

Status Colors:
████ #10b981 (--success)
████ #34d399 (--success-light)
████ #f59e0b (--warning)
████ #ef4444 (--error)
```

---

## 🔧 Debugging Tips

### View All Variables in DevTools
1. Open Chrome DevTools
2. Select any element
3. Go to "Computed" tab
4. Scroll to bottom to see all CSS variables

### Test Variable Changes Live
```javascript
// In browser console
document.documentElement.style.setProperty('--primary', '#ff0000');
```

### Check Variable Value
```javascript
// In browser console
getComputedStyle(document.documentElement).getPropertyValue('--primary');
```

---

## 📝 Best Practices

1. **Always use variables** instead of hardcoded values
2. **Create semantic names** for component-specific overrides
3. **Group related variables** (colors, spacing, etc.)
4. **Document custom variables** in comments
5. **Test in different browsers** for variable support

---

## 🚀 Quick Reference

**Most Used Variables:**
```css
/* Layout */
background: var(--glass-bg);
backdrop-filter: blur(20px);
border: 1px solid var(--glass-border);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-lg);

/* Interaction */
transition: all var(--transition-base);
box-shadow: var(--shadow-glow);

/* Colors */
background: var(--gradient-primary);
color: var(--primary);

/* Spacing */
padding: var(--spacing-lg);
gap: var(--spacing-md);
```

---

**File Location:** `/src/index.css` (lines 1-55)

**Last Updated:** Current transformation

**Total Variables:** 30+
