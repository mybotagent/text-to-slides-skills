# Responsive HTML Rules

Use these rules whenever `text-to-slides` creates a web-viewable HTML deck.

## Base Pattern

Keep Remotion's canonical frame size as metadata:

```html
<main class="deck" data-format="slides" data-remotion-width="1920" data-remotion-height="1080" data-fps="30">
  <section class="slide" data-duration="8" data-notes="Narration note">
    ...
  </section>
</main>
```

Use responsive CSS for actual web layout:

```css
:root {
  --page-pad: clamp(10px, 2vw, 28px);
  --slide-pad-x: clamp(22px, 5.8vw, 112px);
  --slide-pad-top: clamp(30px, 4.5vw, 86px);
  --slide-pad-bottom: clamp(34px, 3.8vw, 72px);
}

body {
  margin: 0;
  padding: var(--page-pad);
  background: #101216;
}

.deck {
  width: min(100%, 1920px);
  margin: 0 auto;
}

.slide {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  padding: var(--slide-pad-top) var(--slide-pad-x) var(--slide-pad-bottom);
  overflow: hidden;
}
```

## Typography And Spacing

Use `clamp()` for all large or layout-critical values:

```css
h1 { font-size: clamp(26px, 3.75vw, 72px); }
.eyebrow { font-size: clamp(12px, 1.15vw, 22px); }
.metric { font-size: clamp(54px, 9.16vw, 176px); }
.panel { padding: clamp(16px, 1.77vw, 34px) clamp(18px, 1.98vw, 38px); }
```

Do not scale everything through `transform: scale(...)`; it often causes scroll and hit-test issues in browsers.

## Mobile Breakpoint

For narrow viewports:

```css
@media screen and (max-width: 760px) {
  body { padding: 0; }
  .slide {
    aspect-ratio: auto;
    min-height: 100svh;
    box-shadow: none;
  }
  .grid,
  .comparison {
    grid-template-columns: 1fr;
  }
}
```

For tables, convert rows into stacked blocks or reduce columns before text becomes unreadable.

## Verification

At minimum, check:

- desktop viewport around `1440x900`
- mobile viewport around `390x844`
- no horizontal scrolling
- all slide titles visible
- all key numbers visible
- no text relies on fixed `1920px` dimensions

If using Playwright, serve local files through `python3 -m http.server` because `file://` may be blocked by the browser tool.
