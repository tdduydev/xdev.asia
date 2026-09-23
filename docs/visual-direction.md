# xDev visual direction — September 23, 2026

The homepage still had the original layout after the AI Studio motion pass. Its
small generic diagram and repeated rounded panels did not communicate a distinct
maker or product identity. This pass changes composition before adding motion.

## References and decisions

- https://linear.app/now/behind-the-latest-design-refresh — foreground the important
  content; reduce competing borders and labels. Apply to navigation and sections.
- https://rauno.me/craft — treat interaction as a material and preserve continuity.
  Apply to the X sculpture and product preview transitions; do not copy assets.
- Local frontend-design and iart-ai animation skills — one memorable focal point,
  short response motion, native browser primitives, tiered reduced motion.

## Tokens

Paper #f7f9fc; ink #17243d; electric blue #0759ed; ice #b8e8ff;
workbench navy #102544; muted #586a83. Keep the existing xDev identity.
Inter: 500–550 display, 400 reading, 600 controls. Display 48–108px, body
16–18px, line lengths below 75 characters. Left-aligned copy.

## Composition

    quiet navigation                                  EN / VI
    large two-line statement       interactive extruded X
    personal introduction         spatial grid and controls
    discover product              pause / rotate / reset
    ------------------------------------------------------
    product introduction + a wide navy product workbench
    real screenshots, selected by visible working controls
    ------------------------------------------------------
    oversized maker initial       personal story / interests
    journal heading               linked topic rows
    large closing statement       links

The visual signature is an extruded X derived from the brand, not a generic
particle globe. Native canvas projects polygon faces with a static SVG fallback.
No fabricated customer logos, usage statistics, testimonials, or biography.

## Motion and fallbacks

Finite entry sequence. Pointer response and rotate/replay controls on the X.
No looping ambient animation or scroll hijacking. Canvas renders only while a
finite interpolation is running; stop offscreen, hidden, or reduced-motion.
Product previews fade on explicit selection. Reduced mode preserves short
opacity feedback and shows the sculpture statically. All content and links work
without JavaScript; controls appear only after successful initialization.

AI Studio receives matching typography, spacing, and a deeper workbench canvas,
while documentation retains its reading layout. Validate both locales, keyboard,
small screens, no-JS, reduced motion, and the existing documentation routes.
