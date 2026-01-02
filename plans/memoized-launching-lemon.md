# CERN Theme Deep Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Perfect the CERN theme as a distinct, handcrafted Particle Physics Lab UI experience. This becomes the template for other themes later.

**Architecture:** Create a comprehensive design token system with TypeScript types. CERN theme gets full implementation with all decorations, animations, and visual treatments. Other themes get placeholder tokens to maintain the system.

**Tech Stack:** TypeScript, CSS Custom Properties, Zustand, React Context

---

## CERN Theme Identity: Particle Physics Control Room

**Inspiration:**
- CERN Large Hadron Collider control room displays
- Oscilloscope and particle detector readouts
- Scientific instrumentation interfaces
- Space mission control aesthetics

**Visual Language:**
- **Colors:** Deep blacks, electric blues, phosphor greens, data highlights
- **Typography:** Monospace for data, tight letter-spacing, uppercase labels
- **Shapes:** Sharp corners, technical precision, no frivolous curves
- **Decorations:** Scanlines, CRT glow effects, grid overlays, data pulse animations
- **Data Display:** Dense information, technical readouts, status indicators everywhere

**Key Characteristics:**
1. **Dense Data Display** - Every panel feels like it shows useful metrics
2. **Terminal Aesthetic** - Command-line inspired inputs and outputs
3. **Glow Effects** - Selected items glow like oscilloscope traces
4. **Scanlines** - Subtle CRT effect for authenticity
5. **Grid Background** - Reference grid like scientific plotting paper
6. **Monospace Typography** - Technical, precise, uniform character widths
7. **Status Indicators** - Blinking lights, connection status, system health

---

## Task 1: Create Theme Token System

**Files:**
- Create: `src/styles/tokens/types.ts`
- Create: `src/styles/tokens/cern.ts`
- Create: `src/styles/tokens/index.ts`

**Step 1: Create token type definitions**

Create `src/styles/tokens/types.ts`:
```typescript
export interface ThemeTokens {
  id: 'cern' | 'intel' | 'pharma' | 'materials';
  name: string;
  description: string;

  typography: {
    fontFamily: { ui: string; data: string; display: string };
    fontWeight: { light: number; normal: number; medium: number; bold: number };
    letterSpacing: { tight: string; normal: string; wide: string };
    textTransform: { labels: string; headings: string };
  };

  spacing: {
    unit: number;
    panelPadding: number;
    sectionGap: number;
    itemGap: number;
    borderWidth: number;
  };

  shapes: {
    borderRadius: { none: string; sm: string; md: string; lg: string; full: string };
    buttonStyle: 'sharp' | 'rounded' | 'pill';
    inputStyle: 'underline' | 'bordered' | 'filled';
    panelStyle: 'flat' | 'elevated' | 'bordered' | 'floating';
  };

  shadows: { sm: string; md: string; lg: string; glow: string; inset: string };

  layout: {
    treePanelWidth: number;
    detailPanelMinHeight: number;
    detailPanelMaxHeight: number;
    statusBarHeight: number;
    toolbarHeight: number;
  };

  animations: {
    duration: { instant: number; fast: number; normal: number; slow: number };
    easing: { default: string; bounce: string; sharp: string };
    style: 'snappy' | 'smooth' | 'mechanical' | 'organic';
  };

  decorations: {
    gridVisible: boolean;
    gridStyle: 'dots' | 'lines' | 'none' | 'dashed';
    scanlines: boolean;
    glowEffects: boolean;
  };

  nodes: {
    shape: 'circle' | 'hexagon' | 'square' | 'rounded-square';
    glowIntensity: number;
    connectionStyle: 'curved' | 'straight' | 'orthogonal';
  };
}
```

**Step 2: Create CERN theme tokens (deep implementation)**

Create `src/styles/tokens/cern.ts`:
```typescript
import type { ThemeTokens } from './types';

export const cernTokens: ThemeTokens = {
  id: 'cern',
  name: 'CERN',
  description: 'Particle Physics Lab - Dark, data-dense, scientific instrumentation',

  typography: {
    fontFamily: {
      ui: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace',
      data: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace',
      display: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
    },
    fontWeight: { light: 300, normal: 400, medium: 500, bold: 700 },
    letterSpacing: { tight: '-0.02em', normal: '0', wide: '0.1em' },
    textTransform: { labels: 'uppercase', headings: 'uppercase' },
    fontSize: {
      xs: '10px',
      sm: '11px',
      base: '12px',
      lg: '13px',
      xl: '14px',
    },
  },

  spacing: { unit: 8, panelPadding: 10, sectionGap: 12, itemGap: 4, borderWidth: 1 },

  shapes: {
    borderRadius: { none: '0', sm: '2px', md: '3px', lg: '4px', full: '9999px' },
    buttonStyle: 'sharp',
    inputStyle: 'bordered',
    panelStyle: 'bordered',
  },

  shadows: {
    sm: '0 1px 2px rgba(0,0,0,0.9)',
    md: '0 2px 8px rgba(0,0,0,0.9)',
    lg: '0 4px 16px rgba(0,0,0,0.95)',
    glow: '0 0 12px rgba(59, 158, 255, 0.4)',
    glowStrong: '0 0 20px rgba(59, 158, 255, 0.6), 0 0 40px rgba(59, 158, 255, 0.3)',
    inset: 'inset 0 1px 3px rgba(0,0,0,0.6)',
  },

  colors: {
    // Deep space blacks
    bgPrimary: '#050608',
    bgSecondary: '#0a0c0e',
    bgTertiary: '#101316',
    bgPanel: '#080a0c',
    bgElevated: '#141820',

    // Electric blues (primary accent)
    accentPrimary: '#3b9eff',
    accentPrimaryDim: '#2a7acc',
    accentPrimaryGlow: 'rgba(59, 158, 255, 0.15)',

    // Phosphor greens (secondary/success)
    accentSecondary: '#00ff88',
    accentSecondaryDim: '#00cc6a',
    accentSecondaryGlow: 'rgba(0, 255, 136, 0.15)',

    // Warning/danger
    warning: '#ffb020',
    danger: '#ff4757',

    // Text
    textPrimary: '#e8eaed',
    textSecondary: '#8b919a',
    textTertiary: '#5a6270',
    textMono: '#00ff88',
    textData: '#3b9eff',

    // Borders
    border: '#1a1e24',
    borderActive: 'rgba(59, 158, 255, 0.3)',
    borderFocus: 'rgba(59, 158, 255, 0.5)',

    // Node colors
    nodeProduct: '#3b9eff',
    nodeComponent: '#8b5cf6',
    nodeMaterial: '#f59e0b',
    nodeChemical: '#00ff88',
    nodeElement: '#ef4444',
  },

  layout: {
    treePanelWidth: 240,
    detailPanelMinHeight: 140,
    detailPanelMaxHeight: 350,
    statusBarHeight: 24,
    toolbarHeight: 36,
    menuBarHeight: 28,
    panelHeaderHeight: 24,
  },

  animations: {
    duration: { instant: 0, fast: 80, normal: 150, slow: 300 },
    easing: { default: 'linear', bounce: 'cubic-bezier(0.68,-0.55,0.27,1.55)', sharp: 'steps(4)' },
    style: 'snappy',
    pulseSpeed: '2s',
    scanlineSpeed: '8s',
  },

  decorations: {
    gridVisible: true,
    gridStyle: 'lines',
    gridOpacity: 0.08,
    gridSize: 40,
    scanlines: true,
    scanlineOpacity: 0.02,
    glowEffects: true,
    pulseEffects: true,
    cornerMarkers: true, // Technical corner brackets
  },

  nodes: {
    shape: 'circle',
    glowIntensity: 0.5,
    connectionStyle: 'curved',
    strokeWidth: 1.5,
    hoverScale: 1.05,
  },
};
```

**Step 4: Create token index (CERN-focused)**

Create `src/styles/tokens/index.ts`:
```typescript
export * from './types';
export { cernTokens } from './cern';

import type { ThemeTokens } from './types';
import { cernTokens } from './cern';

// All themes use CERN for now - we'll add distinct themes later
export const themeTokensMap: Record<ThemeTokens['id'], ThemeTokens> = {
  cern: cernTokens,
  intel: cernTokens, // Placeholder
  pharma: cernTokens, // Placeholder
  materials: cernTokens, // Placeholder
};

export function getThemeTokens(themeId: ThemeTokens['id']): ThemeTokens {
  return themeTokensMap[themeId] || cernTokens;
}
```

**Step 5: Run type-check**

Run: `pnpm type-check`
Expected: PASS

**Step 6: Commit**

```bash
git add src/styles/tokens/
git commit -m "feat: add CERN theme token system

- Comprehensive TypeScript types for theme tokens
- Deep CERN particle physics lab token implementation
- Placeholder mappings for future themes"
```

---

## Task 2: Deep CERN CSS Implementation

**Files:**
- Modify: `src/app/globals.css`

**Step 1: Replace CERN theme block with deep implementation**

Replace the existing `[data-theme="cern"]` block in `src/app/globals.css`:

```css
/* ============================================
   CERN THEME - Particle Physics Control Room
   ============================================ */
:root, [data-theme="cern"] {
  /* Deep space blacks */
  --theme-bg-primary: #050608;
  --theme-bg-secondary: #0a0c0e;
  --theme-bg-tertiary: #101316;
  --theme-bg-panel: #080a0c;
  --theme-bg-elevated: #141820;

  /* Electric blues */
  --theme-accent-primary: #3b9eff;
  --theme-accent-primary-dim: #2a7acc;
  --theme-accent-primary-glow: rgba(59, 158, 255, 0.15);

  /* Phosphor greens */
  --theme-accent-secondary: #00ff88;
  --theme-accent-secondary-dim: #00cc6a;
  --theme-accent-secondary-glow: rgba(0, 255, 136, 0.15);

  /* Alerts */
  --theme-warning: #ffb020;
  --theme-danger: #ff4757;

  /* Text */
  --theme-text-primary: #e8eaed;
  --theme-text-secondary: #8b919a;
  --theme-text-tertiary: #5a6270;
  --theme-text-mono: #00ff88;
  --theme-text-data: #3b9eff;

  /* Borders */
  --theme-border: #1a1e24;
  --theme-border-active: rgba(59, 158, 255, 0.3);
  --theme-border-focus: rgba(59, 158, 255, 0.5);

  /* Confidence */
  --theme-confidence-verified: #00ff88;
  --theme-confidence-estimated: #ffb020;
  --theme-confidence-speculative: #ff4757;

  /* Node type colors */
  --theme-node-product: #3b9eff;
  --theme-node-component: #8b5cf6;
  --theme-node-material: #f59e0b;
  --theme-node-chemical: #00ff88;
  --theme-node-element: #ef4444;

  /* Typography */
  --theme-font-ui: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  --theme-font-data: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  --theme-font-display: ui-sans-serif, system-ui, -apple-system, sans-serif;
  --theme-font-size-xs: 10px;
  --theme-font-size-sm: 11px;
  --theme-font-size-base: 12px;
  --theme-font-size-lg: 13px;
  --theme-letter-spacing-labels: 0.1em;
  --theme-text-transform-labels: uppercase;

  /* Spacing (dense, data-focused) */
  --theme-spacing-unit: 8px;
  --theme-panel-padding: 10px;
  --theme-section-gap: 12px;
  --theme-item-gap: 4px;
  --theme-border-width: 1px;

  /* Shapes (sharp, technical) */
  --theme-radius-sm: 2px;
  --theme-radius-md: 3px;
  --theme-radius-lg: 4px;

  /* Shadows (deep, CRT-like) */
  --theme-shadow-sm: 0 1px 2px rgba(0,0,0,0.9);
  --theme-shadow-md: 0 2px 8px rgba(0,0,0,0.9);
  --theme-shadow-lg: 0 4px 16px rgba(0,0,0,0.95);
  --theme-shadow-glow: 0 0 12px rgba(59, 158, 255, 0.4);
  --theme-shadow-glow-strong: 0 0 20px rgba(59, 158, 255, 0.6), 0 0 40px rgba(59, 158, 255, 0.3);
  --theme-shadow-inset: inset 0 1px 3px rgba(0,0,0,0.6);

  /* Layout (compact) */
  --theme-tree-panel-width: 240px;
  --theme-detail-panel-min: 140px;
  --theme-detail-panel-max: 350px;
  --theme-status-bar-height: 24px;
  --theme-toolbar-height: 36px;
  --theme-menu-bar-height: 28px;
  --theme-panel-header-height: 24px;

  /* Animations (snappy, technical) */
  --theme-duration-instant: 0ms;
  --theme-duration-fast: 80ms;
  --theme-duration-normal: 150ms;
  --theme-duration-slow: 300ms;
  --theme-easing: linear;
  --theme-easing-sharp: steps(4);

  /* Decorations */
  --theme-grid-opacity: 0.08;
  --theme-grid-size: 40px;
  --theme-scanline-opacity: 0.02;
}
```

**Step 2: Add CERN-specific animations and utility classes**

Add at end of globals.css:
```css
/* ============================================
   CERN THEME - Animations & Effects
   ============================================ */

/* Scanline overlay effect */
@keyframes cern-scanline {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

/* Data pulse glow */
@keyframes cern-pulse {
  0%, 100% { opacity: 1; box-shadow: var(--theme-shadow-glow); }
  50% { opacity: 0.7; box-shadow: var(--theme-shadow-glow-strong); }
}

/* Blinking cursor */
@keyframes cern-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Status indicator pulse */
@keyframes cern-status-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.cern-scanline-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255, 255, 255, var(--theme-scanline-opacity)) 2px,
    rgba(255, 255, 255, var(--theme-scanline-opacity)) 4px
  );
}

.cern-grid-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(var(--theme-border) 1px, transparent 1px),
    linear-gradient(90deg, var(--theme-border) 1px, transparent 1px);
  background-size: var(--theme-grid-size) var(--theme-grid-size);
  opacity: var(--theme-grid-opacity);
}

.cern-glow {
  box-shadow: var(--theme-shadow-glow);
}

.cern-glow-strong {
  box-shadow: var(--theme-shadow-glow-strong);
}

.cern-pulse {
  animation: cern-pulse 2s ease-in-out infinite;
}

.cern-blink {
  animation: cern-blink 1s step-end infinite;
}

/* Corner bracket decorations */
.cern-corner-brackets::before,
.cern-corner-brackets::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: var(--theme-accent-primary);
  border-style: solid;
  opacity: 0.5;
}

.cern-corner-brackets::before {
  top: 0;
  left: 0;
  border-width: 1px 0 0 1px;
}

.cern-corner-brackets::after {
  bottom: 0;
  right: 0;
  border-width: 0 1px 1px 0;
}
```

**Step 3: Run lint check**

Run: `pnpm lint`
Expected: PASS

**Step 4: Commit**

```bash
git add src/app/globals.css
git commit -m "feat: deep CERN theme CSS implementation

- Complete CERN color palette (space blacks, electric blues, phosphor greens)
- Typography tokens for monospace-heavy UI
- Dense spacing for data-focused layout
- CRT-style shadows and glow effects
- Scanline and grid overlay animations
- Corner bracket decorations"
```

---

## Task 3: Create Theme Context and Hook

**Files:**
- Create: `src/contexts/theme-context.tsx`
- Create: `src/hooks/use-theme-tokens.ts`
- Modify: `src/components/providers/theme-provider.tsx`

**Step 1: Create theme context**

Create `src/contexts/theme-context.tsx`:
```typescript
'use client';
import { createContext, useContext, useMemo, type ReactNode } from 'react';
import { useUIStore } from '@/stores';
import { getThemeTokens, type ThemeTokens } from '@/styles/tokens';

interface ThemeContextValue {
  theme: ThemeTokens['id'];
  tokens: ThemeTokens;
  setTheme: (theme: ThemeTokens['id']) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeContextProvider({ children }: { children: ReactNode }) {
  const theme = useUIStore((s) => s.theme);
  const setTheme = useUIStore((s) => s.setTheme);

  const value = useMemo(() => ({
    theme,
    tokens: getThemeTokens(theme),
    setTheme,
  }), [theme, setTheme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeContextProvider');
  }
  return context;
}
```

**Step 2: Create useThemeTokens hook**

Create `src/hooks/use-theme-tokens.ts`:
```typescript
'use client';
import { useTheme } from '@/contexts/theme-context';

export function useThemeTokens() {
  const { tokens } = useTheme();
  return tokens;
}

export function useThemeLayout() {
  const { tokens } = useTheme();
  return tokens.layout;
}

export function useThemeAnimations() {
  const { tokens } = useTheme();
  return tokens.animations;
}

export function useThemeShapes() {
  const { tokens } = useTheme();
  return tokens.shapes;
}
```

**Step 3: Update theme provider**

Modify `src/components/providers/theme-provider.tsx`:
```typescript
'use client';
import { useEffect } from 'react';
import { useUIStore } from '@/stores';
import { ThemeContextProvider } from '@/contexts/theme-context';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useUIStore((s) => s.theme);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <ThemeContextProvider>
      {children}
    </ThemeContextProvider>
  );
}
```

**Step 4: Run type-check**

Run: `pnpm type-check`
Expected: PASS

**Step 5: Commit**

```bash
git add src/contexts/ src/hooks/use-theme-tokens.ts src/components/providers/theme-provider.tsx
git commit -m "feat: add theme context and hooks

- Create ThemeContextProvider with token access
- Create useTheme hook for theme state and tokens
- Create specialized hooks (useThemeTokens, useThemeLayout, etc.)
- Update ThemeProvider to wrap with context"
```

---

## Task 4: Create Theme-Aware UI Components

**Files:**
- Create: `src/components/ui/themed/index.ts`
- Create: `src/components/ui/themed/themed-panel.tsx`
- Create: `src/components/ui/themed/themed-button.tsx`
- Create: `src/components/ui/themed/themed-input.tsx`

**Step 1: Create themed panel component**

Create `src/components/ui/themed/themed-panel.tsx`:
```typescript
'use client';
import { type ReactNode } from 'react';
import { useTheme } from '@/contexts/theme-context';

interface ThemedPanelProps {
  children: ReactNode;
  className?: string;
  header?: string;
}

export function ThemedPanel({ children, className = '', header }: ThemedPanelProps) {
  const { theme, tokens } = useTheme();

  const panelStyle = {
    backgroundColor: 'var(--theme-bg-secondary)',
    border: `var(--theme-border-width) solid var(--theme-border)`,
    borderRadius: `var(--theme-radius-md)`,
    padding: `var(--theme-panel-padding)`,
  };

  return (
    <div style={panelStyle} className={className}>
      {header && (
        <div style={{
          fontSize: '11px',
          fontWeight: 600,
          textTransform: tokens.typography.textTransform.labels as 'uppercase' | 'capitalize' | 'none',
          letterSpacing: tokens.typography.letterSpacing.wide,
          color: 'var(--theme-text-secondary)',
          marginBottom: `var(--theme-item-gap)`,
          fontFamily: tokens.typography.fontFamily.ui,
        }}>
          {header}
        </div>
      )}
      {children}
      {/* CERN scanline effect */}
      {theme === 'cern' && tokens.decorations.scanlines && (
        <div className="absolute inset-0 pointer-events-none opacity-[0.03]"
          style={{
            background: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px)',
          }}
        />
      )}
    </div>
  );
}
```

**Step 2: Create themed button component**

Create `src/components/ui/themed/themed-button.tsx`:
```typescript
'use client';
import { type ButtonHTMLAttributes } from 'react';
import { useTheme } from '@/contexts/theme-context';

interface ThemedButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
}

export function ThemedButton({
  children,
  variant = 'primary',
  className = '',
  style,
  ...props
}: ThemedButtonProps) {
  const { tokens } = useTheme();

  const baseStyle = {
    fontFamily: tokens.typography.fontFamily.ui,
    fontWeight: tokens.typography.fontWeight.medium,
    borderRadius: tokens.shapes.buttonStyle === 'sharp' ? tokens.shapes.borderRadius.sm :
                  tokens.shapes.buttonStyle === 'pill' ? tokens.shapes.borderRadius.full :
                  tokens.shapes.borderRadius.md,
    transition: `all var(--theme-duration-fast) var(--theme-easing)`,
    letterSpacing: tokens.typography.letterSpacing.normal,
    textTransform: tokens.typography.textTransform.labels as 'uppercase' | 'capitalize' | 'none',
  };

  const variantStyles = {
    primary: {
      backgroundColor: 'var(--theme-accent-primary)',
      color: 'white',
      padding: '8px 16px',
      border: 'none',
    },
    secondary: {
      backgroundColor: 'var(--theme-bg-tertiary)',
      color: 'var(--theme-text-primary)',
      padding: '8px 16px',
      border: `var(--theme-border-width) solid var(--theme-border)`,
    },
    ghost: {
      backgroundColor: 'transparent',
      color: 'var(--theme-text-secondary)',
      padding: '6px 10px',
      border: 'none',
    },
  };

  return (
    <button
      className={className}
      style={{ ...baseStyle, ...variantStyles[variant], ...style }}
      {...props}
    >
      {children}
    </button>
  );
}
```

**Step 3: Create themed input component**

Create `src/components/ui/themed/themed-input.tsx`:
```typescript
'use client';
import { type InputHTMLAttributes } from 'react';
import { useTheme } from '@/contexts/theme-context';

interface ThemedInputProps extends InputHTMLAttributes<HTMLInputElement> {}

export function ThemedInput({ className = '', style, ...props }: ThemedInputProps) {
  const { tokens } = useTheme();

  const inputStyle = {
    fontFamily: tokens.typography.fontFamily.data,
    backgroundColor: tokens.shapes.inputStyle === 'filled' ? 'var(--theme-bg-tertiary)' : 'var(--theme-bg-primary)',
    border: tokens.shapes.inputStyle === 'underline'
      ? 'none'
      : `var(--theme-border-width) solid var(--theme-border)`,
    borderBottom: tokens.shapes.inputStyle === 'underline'
      ? `var(--theme-border-width) solid var(--theme-border)`
      : undefined,
    borderRadius: tokens.shapes.inputStyle === 'underline' ? '0' : `var(--theme-radius-md)`,
    padding: '10px 14px',
    color: 'var(--theme-text-primary)',
    transition: `all var(--theme-duration-fast) var(--theme-easing)`,
  };

  return (
    <input
      className={className}
      style={{ ...inputStyle, ...style }}
      {...props}
    />
  );
}
```

**Step 4: Create index export**

Create `src/components/ui/themed/index.ts`:
```typescript
export { ThemedPanel } from './themed-panel';
export { ThemedButton } from './themed-button';
export { ThemedInput } from './themed-input';
```

**Step 5: Run type-check**

Run: `pnpm type-check`
Expected: PASS

**Step 6: Commit**

```bash
git add src/components/ui/themed/
git commit -m "feat: add theme-aware UI components

- ThemedPanel with header and decorations per theme
- ThemedButton with variant styles adapting to theme shapes
- ThemedInput adapting style (bordered, filled, underline) per theme"
```

---

## Task 5: Update Workstation Layout for Theme-Aware Dimensions

**Files:**
- Modify: `src/components/workstation/workstation-layout.tsx`

**Step 1: Update layout to use theme tokens**

Update `src/components/workstation/workstation-layout.tsx`:
```typescript
'use client';
import { useState, ReactNode } from 'react';
import { StatusBar } from './status-bar';
import { Toolbar } from './toolbar';
import { useTheme } from '@/contexts/theme-context';

interface WorkstationLayoutProps {
  treePanel: ReactNode;
  canvas: ReactNode;
  detailPanel: ReactNode;
}

export function WorkstationLayout({ treePanel, canvas, detailPanel }: WorkstationLayoutProps) {
  const { tokens } = useTheme();
  const [treePanelCollapsed, setTreePanelCollapsed] = useState(false);
  const [detailExpanded, setDetailExpanded] = useState(false);

  const { layout, animations, shapes, decorations } = tokens;

  return (
    <div
      className="h-screen flex flex-col"
      style={{
        backgroundColor: 'var(--theme-bg-primary)',
        color: 'var(--theme-text-primary)',
        transition: `all ${animations.duration.normal}ms ${animations.easing.default}`,
      }}
    >
      <StatusBar />

      <div className="flex-1 flex overflow-hidden">
        {/* Tree Panel - theme-aware width */}
        <aside
          className="h-full overflow-hidden"
          style={{
            width: treePanelCollapsed ? 0 : layout.treePanelWidth,
            borderRight: `var(--theme-border-width) solid var(--theme-border)`,
            backgroundColor: 'var(--theme-bg-secondary)',
            transition: `width ${animations.duration.normal}ms ${animations.easing.default}`,
          }}
        >
          <div className="h-full overflow-y-auto">
            {treePanel}
          </div>
        </aside>

        {/* Toggle button */}
        <button
          onClick={() => setTreePanelCollapsed(!treePanelCollapsed)}
          className="flex items-center justify-center hover:bg-opacity-10 hover:bg-white"
          style={{
            width: 16,
            backgroundColor: 'var(--theme-bg-secondary)',
            transition: `background-color ${animations.duration.fast}ms ${animations.easing.default}`,
          }}
          aria-label={treePanelCollapsed ? 'Expand tree panel' : 'Collapse tree panel'}
        >
          <span className="text-xs" style={{ color: 'var(--theme-text-secondary)' }}>
            {treePanelCollapsed ? '>' : '<'}
          </span>
        </button>

        {/* Main content area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Canvas area with optional grid */}
          <div className="flex-1 overflow-hidden relative">
            {canvas}
            {/* Theme-specific grid overlay */}
            {decorations.gridVisible && (
              <div
                className="absolute inset-0 pointer-events-none"
                style={{
                  backgroundImage: decorations.gridStyle === 'lines'
                    ? `linear-gradient(var(--theme-border) 1px, transparent 1px), linear-gradient(90deg, var(--theme-border) 1px, transparent 1px)`
                    : decorations.gridStyle === 'dots'
                    ? `radial-gradient(circle, var(--theme-border) 1px, transparent 1px)`
                    : 'none',
                  backgroundSize: decorations.gridStyle === 'dots' ? '20px 20px' : '40px 40px',
                  opacity: 'var(--theme-grid-opacity)',
                }}
              />
            )}
          </div>

          <Toolbar />

          {/* Detail Panel - theme-aware heights */}
          <div
            className="overflow-hidden"
            style={{
              height: detailExpanded ? layout.detailPanelMaxHeight : layout.detailPanelMinHeight,
              borderTop: `var(--theme-border-width) solid var(--theme-border)`,
              backgroundColor: 'var(--theme-bg-secondary)',
              transition: `height ${animations.duration.normal}ms ${animations.easing.default}`,
            }}
          >
            <button
              onClick={() => setDetailExpanded(!detailExpanded)}
              className="w-full flex items-center justify-center cursor-row-resize hover:bg-opacity-10 hover:bg-white"
              style={{
                height: 24,
                borderBottom: `1px solid var(--theme-border)`,
                transition: `background-color ${animations.duration.fast}ms ${animations.easing.default}`,
              }}
            >
              <span className="text-xs" style={{ color: 'var(--theme-text-secondary)' }}>
                {detailExpanded ? 'v' : '^'} Details
              </span>
            </button>
            <div style={{ height: 'calc(100% - 24px)', overflow: 'auto' }}>
              {detailPanel}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
```

**Step 2: Run type-check**

Run: `pnpm type-check`
Expected: PASS

**Step 3: Run dev server to test**

Run: `pnpm dev`
Expected: Layout dimensions change when switching themes

**Step 4: Commit**

```bash
git add src/components/workstation/workstation-layout.tsx
git commit -m "feat: make workstation layout theme-aware

- Panel widths and heights use theme tokens
- Animation durations and easings from theme
- Grid overlay adapts to theme decorations
- All transitions use theme timing"
```

---

## Task 6: Update RadialNode for Theme-Aware Shapes

**Files:**
- Modify: `src/components/canvas/radial-node.tsx`

**Step 1: Replace hardcoded colors and add shape variants**

Update `src/components/canvas/radial-node.tsx` to use CSS variables and theme-aware shapes:
```typescript
'use client';
import { useCompositionStore } from '@/stores';
import { useTheme } from '@/contexts/theme-context';
import { LayoutNode } from '@/hooks/use-radial-layout';

// Use CSS variables instead of hardcoded colors
const NODE_COLORS: Record<string, string> = {
  product: 'var(--theme-accent-primary)',
  component: 'var(--node-component, #8b5cf6)',
  material: 'var(--node-material, #f59e0b)',
  chemical: 'var(--theme-accent-secondary)',
  element: 'var(--node-element, #ef4444)',
};

const NODE_SIZES: Record<string, number> = {
  product: 30,
  component: 24,
  material: 20,
  chemical: 16,
  element: 12,
};

interface RadialNodeProps {
  layoutNode: LayoutNode;
}

// Shape rendering functions
function CircleShape({ size, fill, stroke, strokeWidth }: { size: number; fill: string; stroke: string; strokeWidth: number }) {
  return <circle r={size} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />;
}

function HexagonShape({ size, fill, stroke, strokeWidth }: { size: number; fill: string; stroke: string; strokeWidth: number }) {
  const points = Array.from({ length: 6 }, (_, i) => {
    const angle = (i * 60 - 30) * Math.PI / 180;
    return `${size * Math.cos(angle)},${size * Math.sin(angle)}`;
  }).join(' ');
  return <polygon points={points} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />;
}

function RoundedSquareShape({ size, fill, stroke, strokeWidth }: { size: number; fill: string; stroke: string; strokeWidth: number }) {
  const s = size * 1.4;
  return <rect x={-s/2} y={-s/2} width={s} height={s} rx={size * 0.3} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />;
}

function SquareShape({ size, fill, stroke, strokeWidth }: { size: number; fill: string; stroke: string; strokeWidth: number }) {
  const s = size * 1.4;
  return <rect x={-s/2} y={-s/2} width={s} height={s} fill={fill} stroke={stroke} strokeWidth={strokeWidth} />;
}

export function RadialNode({ layoutNode }: RadialNodeProps) {
  const { node, x, y, path, hasChildren, isExpanded } = layoutNode;
  const { tokens } = useTheme();

  const selectedNode = useCompositionStore((s) => s.selectedNode);
  const selectNode = useCompositionStore((s) => s.selectNode);
  const setHoveredNode = useCompositionStore((s) => s.setHoveredNode);
  const toggleExpandedPath = useCompositionStore((s) => s.toggleExpandedPath);

  const isSelected = selectedNode?.id === node.id;
  const color = NODE_COLORS[node.type] || 'var(--theme-text-secondary)';
  const size = NODE_SIZES[node.type] || 16;

  const handleClick = () => selectNode(node);
  const handleDoubleClick = () => hasChildren && toggleExpandedPath(path);
  const handleMouseEnter = () => setHoveredNode(node);
  const handleMouseLeave = () => setHoveredNode(null);

  // Render shape based on theme
  const ShapeComponent = {
    circle: CircleShape,
    hexagon: HexagonShape,
    'rounded-square': RoundedSquareShape,
    square: SquareShape,
  }[tokens.nodes.shape] || CircleShape;

  return (
    <g
      transform={`translate(${x}, ${y})`}
      onClick={handleClick}
      onDoubleClick={handleDoubleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ cursor: 'pointer' }}
    >
      {/* Glow effect - intensity based on theme */}
      {isSelected && tokens.nodes.glowIntensity > 0 && (
        <ShapeComponent
          size={size + 8}
          fill="none"
          stroke={color}
          strokeWidth={2}
        />
      )}

      {/* Main shape */}
      <ShapeComponent
        size={size}
        fill="var(--theme-bg-secondary)"
        stroke={color}
        strokeWidth={isSelected ? 3 : 2}
      />

      {/* Inner fill based on percentage */}
      {node.percentage !== undefined && (
        <ShapeComponent
          size={size * 0.7}
          fill={color}
          stroke="none"
          strokeWidth={0}
        />
      )}

      {/* Labels */}
      <text
        y={size + 14}
        textAnchor="middle"
        fill="var(--theme-text-primary)"
        fontSize="11"
        style={{ fontFamily: tokens.typography.fontFamily.ui }}
      >
        {node.name.length > 12 ? node.name.slice(0, 10) + '...' : node.name}
      </text>

      {node.percentage !== undefined && (
        <text
          y={size + 26}
          textAnchor="middle"
          fill="var(--theme-text-mono)"
          fontSize="9"
          style={{ fontFamily: tokens.typography.fontFamily.data }}
        >
          {node.percentage.toFixed(1)}%
        </text>
      )}

      {/* Expand indicator */}
      {hasChildren && (
        <g>
          <circle
            cx={size * 0.7}
            cy={-size * 0.7}
            r="8"
            fill="var(--theme-bg-tertiary)"
            stroke={color}
            strokeWidth="1.5"
          />
          <text
            x={size * 0.7}
            y={-size * 0.7 + 1}
            textAnchor="middle"
            dominantBaseline="middle"
            fill={color}
            fontSize="12"
            fontWeight="bold"
            style={{ pointerEvents: 'none' }}
          >
            {isExpanded ? '-' : '+'}
          </text>
        </g>
      )}
    </g>
  );
}
```

**Step 2: Run type-check**

Run: `pnpm type-check`
Expected: PASS

**Step 3: Commit**

```bash
git add src/components/canvas/radial-node.tsx
git commit -m "feat: make RadialNode theme-aware

- Replace hardcoded colors with CSS variables
- Add shape variants (circle, hexagon, rounded-square, square)
- Shape, glow intensity, typography from theme tokens
- Support for CERN circles, Intel rounded squares, Materials hexagons"
```

---

## Task 7: Add CERN Theme Decorations

**Files:**
- Create: `src/components/ui/themed/cern-decorations.tsx`

**Step 1: Create CERN-specific decoration components**

Create `src/components/ui/themed/cern-decorations.tsx`:
```typescript
'use client';
import { useTheme } from '@/contexts/theme-context';

export function ScanlineOverlay() {
  const { theme } = useTheme();
  if (theme !== 'cern') return null;

  return (
    <div
      className="cern-scanline-overlay"
      aria-hidden="true"
    />
  );
}

export function GridOverlay() {
  const { theme } = useTheme();
  if (theme !== 'cern') return null;

  return (
    <div
      className="cern-grid-overlay"
      aria-hidden="true"
    />
  );
}

export function CornerBrackets({ className = '' }: { className?: string }) {
  const { theme } = useTheme();
  if (theme !== 'cern') return null;

  return (
    <div className={`cern-corner-brackets ${className}`} aria-hidden="true" />
  );
}

export function StatusPulse({ color = 'var(--theme-accent-secondary)' }: { color?: string }) {
  return (
    <span
      className="inline-block w-2 h-2 rounded-full cern-pulse"
      style={{ backgroundColor: color }}
    />
  );
}

export function DataReadout({ label, value, unit }: { label: string; value: string | number; unit?: string }) {
  return (
    <div className="flex items-center gap-2 font-mono text-xs">
      <span style={{ color: 'var(--theme-text-tertiary)', letterSpacing: 'var(--theme-letter-spacing-labels)' }}>
        {label}:
      </span>
      <span style={{ color: 'var(--theme-text-data)' }}>{value}</span>
      {unit && <span style={{ color: 'var(--theme-text-tertiary)' }}>{unit}</span>}
    </div>
  );
}
```

**Step 2: Update themed/index.ts exports**

Add to `src/components/ui/themed/index.ts`:
```typescript
export { ThemedPanel } from './themed-panel';
export { ThemedButton } from './themed-button';
export { ThemedInput } from './themed-input';
export * from './cern-decorations';
```

**Step 3: Commit**

```bash
git add src/components/ui/themed/
git commit -m "feat: add CERN theme decorations

- ScanlineOverlay for CRT effect
- GridOverlay for technical grid background
- CornerBrackets for technical panel decoration
- StatusPulse animated indicator
- DataReadout for displaying metrics"
```

---

## Task 8: Update Home Page for CERN Aesthetic

**Files:**
- Modify: `src/components/home/analysis-terminal.tsx`
- Modify: `src/components/home/specimen-input.tsx`
- Modify: `src/components/home/system-status.tsx`

**Step 1: Apply CERN aesthetic to analysis-terminal**

Update to include:
- Scanline overlay
- Grid background
- Corner brackets on panels
- Dense data displays
- Status indicators with pulse effects
- Monospace typography throughout
- Data readouts for system metrics

**Step 2: Update specimen-input with terminal styling**

- Command-line style input with prompt character
- Blinking cursor effect
- Sharp borders, dark backgrounds
- Phosphor green highlights

**Step 3: Update system-status with live readouts**

- Multiple status metrics displayed
- Pulsing status indicators
- Connection status with latency readout
- Model/version info in technical format

**Step 4: Commit**

```bash
git add src/components/home/
git commit -m "feat: apply deep CERN aesthetic to home page

- Dense data display layout
- Scanline and grid overlays
- Command-line style input
- Technical status readouts
- Pulsing status indicators"
```

---

## Task 9: Update Workstation Panels for CERN

**Files:**
- Modify: `src/components/panels/tree-panel.tsx`
- Modify: `src/components/panels/detail-panel.tsx`

**Step 1: Update tree-panel with CERN styling**

- Dense node rows
- Monospace labels
- Sharp borders
- Data-focused display
- Corner bracket decorations

**Step 2: Update detail-panel with CERN styling**

- Technical data layout
- Confidence indicators with glow
- Monospace data values
- Dense information display

**Step 3: Commit**

```bash
git add src/components/panels/
git commit -m "feat: apply CERN aesthetic to workstation panels

- Dense tree navigation
- Technical detail display
- Monospace typography
- Data-focused layout"
```

---

## Task 10: Final CERN Polish and Testing

**Files:**
- All modified files

**Step 1: Run full verification**

Run: `pnpm type-check && pnpm lint && pnpm build`
Expected: All pass

**Step 2: Visual testing checklist**

Test CERN theme specifically:
- [ ] Deep space black backgrounds
- [ ] Electric blue accents glowing
- [ ] Phosphor green for success/data
- [ ] Scanlines visible but subtle
- [ ] Grid overlay on canvas
- [ ] Dense, data-focused layouts
- [ ] Monospace typography throughout
- [ ] Sharp corners on all elements
- [ ] Pulsing status indicators
- [ ] Corner brackets on panels
- [ ] Snappy, linear animations

**Step 3: Final commit**

```bash
git add .
git commit -m "feat: complete CERN particle physics theme

Deep, handcrafted particle physics control room aesthetic:
- Dense data displays like CERN control room
- CRT-style scanlines and glow effects
- Monospace typography for technical precision
- Sharp corners, no frivolous curves
- Pulsing status indicators
- Grid overlay for scientific plotting feel
- Snappy, linear animations

Ready for Intel, Pharma, Materials themes later"
```

---

## Files Summary

### New Files (8)
- `src/styles/tokens/types.ts` - TypeScript type definitions for theme tokens
- `src/styles/tokens/cern.ts` - Deep CERN particle physics theme tokens
- `src/styles/tokens/index.ts` - Token exports and getThemeTokens helper
- `src/contexts/theme-context.tsx` - React context for theme tokens
- `src/hooks/use-theme-tokens.ts` - Convenience hooks for theme access
- `src/components/ui/themed/themed-panel.tsx` - Theme-aware panel component
- `src/components/ui/themed/themed-button.tsx` - Theme-aware button component
- `src/components/ui/themed/themed-input.tsx` - Theme-aware input component
- `src/components/ui/themed/cern-decorations.tsx` - CERN-specific decorations
- `src/components/ui/themed/index.ts` - UI component exports

### Modified Files (9)
- `src/app/globals.css` - Deep CERN CSS variables and utility classes
- `src/components/providers/theme-provider.tsx` - Add ThemeContextProvider
- `src/components/workstation/workstation-layout.tsx` - Theme-aware layout
- `src/components/canvas/radial-node.tsx` - Theme-aware node shapes
- `src/components/home/analysis-terminal.tsx` - CERN aesthetic home
- `src/components/home/specimen-input.tsx` - Terminal-style input
- `src/components/home/system-status.tsx` - Technical status display
- `src/components/panels/tree-panel.tsx` - Dense tree navigation
- `src/components/panels/detail-panel.tsx` - Technical detail display

---

## Next Steps (Future)

After CERN is perfected, apply same approach to:
1. **Intel** - Clean, minimal, Apple-like refinement
2. **Pharma** - Light mode, clinical precision
3. **Materials** - Industrial, bold, engineering
