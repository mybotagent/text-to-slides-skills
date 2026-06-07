# Chart Motion Defaults

Use these defaults when generating HTML slides with metrics, bars, KPI tables, comparisons, or chart-like proof objects.

## HTML Data Pattern

Large metric:

```html
<div class="metric counter" data-count-to="95" data-suffix="%">
  <span class="count-value">95</span><small>%</small>
</div>
```

Range metric:

```html
<div class="metric counter" data-count-to="8" data-prefix="5~" data-suffix="h">
  <span class="count-prefix">5~</span><span class="count-value">8</span><small>h</small>
</div>
```

Bar:

```html
<div class="bar-track">
  <div class="bar" style="--value: 80; --bar-delay: 520ms"></div>
</div>
```

Summary table value:

```html
<strong class="counter-inline" data-count-to="1.5" data-suffix="s+">1.5s+</strong>
```

## CSS Motion Pattern

```css
.metric.counter {
  display: inline-flex;
  align-items: baseline;
  gap: 0.02em;
  transform-origin: left bottom;
  animation: metricPop 780ms cubic-bezier(.2,.9,.2,1) both;
}

.bar-track {
  position: relative;
  overflow: hidden;
}

.bar-track::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.72), transparent);
  transform: translateX(-110%);
  animation: barSweep 900ms ease both;
  animation-delay: 940ms;
}

.bar {
  width: calc(var(--value) * 1%);
  transform-origin: left center;
  animation: barFill 980ms cubic-bezier(.2,.9,.2,1) both;
  animation-delay: var(--bar-delay, 360ms);
}

.summary-table tbody tr {
  opacity: 0;
  transform: translateY(18px);
  animation: rowReveal 620ms ease both;
}

.summary-table tbody tr:nth-child(1) { animation-delay: 360ms; }
.summary-table tbody tr:nth-child(2) { animation-delay: 520ms; }
.summary-table tbody tr:nth-child(3) { animation-delay: 680ms; }

@keyframes barFill {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

@keyframes barSweep {
  from { transform: translateX(-110%); }
  to { transform: translateX(110%); }
}

@keyframes metricPop {
  0% { opacity: 0; transform: translateY(20px) scale(0.92); }
  70% { opacity: 1; transform: translateY(0) scale(1.035); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes rowReveal {
  to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 1ms !important;
    animation-delay: 0ms !important;
    transition-duration: 1ms !important;
  }
}
```

## JavaScript Count-up Pattern

Use a small script so values animate when each slide enters the viewport. Keep final values in the HTML so the slide remains readable if JavaScript fails.

```html
<script>
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function formatNumber(value, decimals) {
  return Number(value).toLocaleString("ko-KR", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

function animateCounter(element) {
  const target = Number(element.dataset.countTo || 0);
  const suffix = element.dataset.suffix || "";
  const duration = prefersReducedMotion ? 1 : 980;
  const decimals = String(element.dataset.countTo || "").includes(".") ? 1 : 0;
  const valueNode = element.querySelector(".count-value");
  const inline = element.classList.contains("counter-inline");
  const start = performance.now();

  function write(value) {
    const text = formatNumber(value, decimals);
    if (valueNode) valueNode.textContent = text;
    else if (inline) element.textContent = `${text}${suffix}`;
  }

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    write(target * eased);
    if (progress < 1) requestAnimationFrame(tick);
    else write(target);
  }

  write(0);
  requestAnimationFrame(tick);
}

const observedCounters = new WeakSet();
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.querySelectorAll(".counter, .counter-inline").forEach((counter) => {
      if (observedCounters.has(counter)) return;
      observedCounters.add(counter);
      animateCounter(counter);
    });
  });
}, { threshold: 0.38 });

document.querySelectorAll(".slide").forEach((slide) => observer.observe(slide));
</script>
```

## Remotion Mapping

- `.counter[data-count-to]`: use `interpolate(frame, [start, end], [0, target])`.
- `.bar[style*="--value"]`: animate `transform: scaleX(value / 100)` or width.
- `.summary-table tbody tr`: wrap each row in a `<Sequence>` or apply frame-offset opacity/translate.
- `data-duration`: convert seconds to frames with `duration * fps`.
- Keep final static values visible for non-animated previews and reduced-motion mode.
