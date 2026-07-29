```markdown
# Harness Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill provides a comprehensive guide to the development patterns and workflows used in the Harness JavaScript codebase. It covers coding conventions, step-by-step instructions for common refactoring and redesign tasks, and best practices for maintaining a consistent and accessible website. The repository is primarily JavaScript, with no framework detected, and focuses on modular CSS and JS for a static website.

## Coding Conventions

- **File Naming:**  
  Use camelCase for JavaScript and CSS files.  
  _Example:_  
  ```
  website/js/footer.js
  website/css/global.css
  ```

- **Import Style:**  
  Use relative imports for JavaScript modules.  
  _Example:_  
  ```js
  import { updateFooter } from './footer.js';
  ```

- **Export Style:**  
  Use named exports for all JS modules.  
  _Example:_  
  ```js
  // In footer.js
  export function updateFooter() { /* ... */ }
  ```

- **Commit Messages:**  
  Freeform style, often prefixed with context keywords like `checkpoint`, `hero`, `fix`, `manifesto`, `docs`, `footer`.  
  _Example:_  
  ```
  fix: resolve sticky sidebar scroll issue on docs page
  ```

## Workflows

### CSS Design Token Refactor
**Trigger:** When you want to improve design consistency or update the design system across the site.  
**Command:** `/refactor-css-tokens`

1. Identify hardcoded CSS values (colors, font sizes, spacing) in files like `nav.css`, `global.css`, `index.css`, `style.css`.
2. Replace hardcoded values with CSS custom properties (design tokens).
   ```css
   /* Before */
   color: #333;
   font-size: 18px;

   /* After */
   color: var(--color-text-primary);
   font-size: var(--font-size-lg);
   ```
3. Update HTML files (e.g., `manifesto.html`, `index.html`) if necessary to use new tokenized styles.
4. Test for visual consistency and accessibility.

### Footer Component Redesign
**Trigger:** When you want to update the footer's design, structure, or accessibility features.  
**Command:** `/redesign-footer`

1. Update footer layout and content in `global.css` and `index.css`.
2. Remove or consolidate duplicate/legacy footer CSS from `style.css` and `index.css`.
3. Rewrite or simplify `footer.js` to match the new structure and improve accessibility.
   ```js
   // Example: Accessible footer focus management
   export function enhanceFooterAccessibility() {
     const links = document.querySelectorAll('footer a');
     links.forEach(link => link.setAttribute('tabindex', '0'));
   }
   ```
4. Test the footer on all relevant pages (e.g., `index.html`).

### Hero Section Redesign
**Trigger:** When you want to update the hero section's appearance or messaging.  
**Command:** `/update-hero`

1. Edit hero layout and content in `index.html`.
2. Update related CSS in `index.css` for new layout, typography, and button styles.
   ```css
   /* Example: Hero button style */
   .hero-cta {
     background: var(--color-accent);
     font-size: var(--font-size-xl);
   }
   ```
3. Remove unused hero-related CSS classes.
4. Test the hero section for visual correctness and responsiveness.

### Sticky Sidebar and Scroll Behavior Fix
**Trigger:** When you need to resolve issues with sidebar stickiness or scroll-spy behavior after layout/CSS changes.  
**Command:** `/fix-sidebar-scroll`

1. Identify the root cause of sticky/scroll issue (e.g., `overflow-x`, scroll container).
2. Update `global.css` (and sometimes `nav.css` or `docs.css`) to adjust overflow, positioning, or height.
   ```css
   /* Example: Fix for sticky sidebar */
   .sidebar {
     position: sticky;
     top: 0;
     height: 100vh;
     overflow-y: auto;
   }
   ```
3. Update or add JS handlers in `docs-sidebar.js` for scroll-spy or click behavior.
   ```js
   // Example: Scroll-spy logic
   export function activateScrollSpy() {
     // ...implementation...
   }
   ```
4. Test sidebar on `docs.html` and related pages.

## Testing Patterns

- **Test Framework:** Unknown (not detected)
- **File Pattern:** Test files are named with the pattern `*.test.*`.
  _Example:_  
  ```
  website/js/footer.test.js
  ```
- **Testing Approach:**  
  - Place test files alongside implementation files.
  - Use descriptive test names and cover both logic and UI behavior where possible.

## Commands

| Command              | Purpose                                                        |
|----------------------|----------------------------------------------------------------|
| /refactor-css-tokens | Standardize CSS using design tokens for colors, fonts, spacing |
| /redesign-footer     | Redesign and refactor the website footer                       |
| /update-hero         | Redesign the homepage hero section                             |
| /fix-sidebar-scroll  | Fix sticky sidebar and scroll behavior                         |
```
