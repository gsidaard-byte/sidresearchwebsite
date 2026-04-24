# Research Website Design Brief

## Selected Theme

`Ocean Depths`

Base palette from `theme-factory`:

- Deep Navy: `#1a2332`
- Teal: `#2d8b8b`
- Seafoam: `#a8dadc`
- Cream: `#f1faee`

## Design Goal

Create a research-group website that feels:

- academically credible
- visually polished
- technically grounded
- student-centered

The site should read as a serious aerospace research presence with strong teaching and mentoring values, not as a startup landing page or a generic university template.

## Visual Direction

### Overall Look

- dark editorial shell with warm light content surfaces
- restrained, high-contrast color use
- strong section hierarchy
- large image moments for students, facilities, and lab work
- subtle technical detailing such as thin rules, grids, and measured spacing

### Tone

- calm
- precise
- confident
- human

### Typography Direction

Recommended website pairing:

- Headings: a serif display face with authority and warmth
- Body: a clean sans-serif for readability

Practical web-safe implementation for prototype:

- Headings: `Georgia`, `Times New Roman`, serif
- Body: `Arial`, `Helvetica`, sans-serif

Production implementation can be upgraded to better web fonts later.

## Information Architecture

Top-level navigation:

1. Home
2. Research
3. Students
4. Alumni
5. Publications
6. Teaching
7. Facilities
8. News
9. Awards
10. Contact / CV

Navigation model:

- each primary tab should open a separate page
- homepage should remain an overview page, not a long-scroll archive
- long lists such as publications and alumni should live on dedicated internal pages

## Homepage Structure

### Hero

- research identity
- one-sentence positioning statement
- quick links to publications, students, and projects

### Research Themes

Show 4 to 6 themes based on current content:

- Propulsion and advanced aircraft configurations
- Aerodynamics and wake physics
- Morphing wings and lift distribution
- Flow diagnostics and event-based sensing
- Agricultural spray and drone applications
- AI in education

### Current Work

- 3 to 5 featured active projects
- brief funding or impact notes where relevant

### Students

- current students preview with headshots
- link to full directory and student profile pages
- brief preview of alumni with link to dedicated alumni page

### Publications

- citation count highlight
- selected recent journal papers
- patent highlight

### Teaching and Outreach

- hands-on learning
- entrepreneurship and AI in education
- student clubs and Air Camp

### Facilities

- wind tunnel
- water tunnel
- flight simulator

### Footer

- CV link
- contact
- institution / lab affiliation

## Page Templates

### Research Page

- theme overview
- grouped project cards
- funding highlights

### Publications Page

- filters by journal, conference, patent
- recent featured papers at top

### Students Page

- current students first
- brief alumni preview with link out
- individual profiles generated from structured data

### Alumni Page

- prior students grouped by degree level
- thesis and dissertation mentorship highlights
- student awards and recognition

### Teaching Page

- teaching philosophy
- courses taught
- student experience and outreach

### Facilities Page

- facility sections with capability summaries
- downloadable or linked supporting materials where useful

## Motion and Interaction

- slow fade/slide-in on section entry
- hover emphasis on cards and navigation
- no flashy animations

## Content Work Still Needed

- homepage intro copy
- contact details
- facilities text and images
- final student profile markdown cleanup
- replacement of placeholder student quotes

## Recommended Next Build Step

Convert this folder into a content-driven Astro site using:

- markdown collections for sections
- structured student data for profiles
- reusable cards and listing templates
- the `Ocean Depths` palette as the site token system
