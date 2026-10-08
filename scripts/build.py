"""Compile trusted Markdown and shared templates to hosting-compatible HTML.

Output is tracked, so deployment does not need Python or a build command.
"""
from pathlib import Path
from html import escape as e
from datetime import date
import json
import re
import hashlib
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE = json.loads((ROOT / 'content/site.json').read_text())
GENERATED = []


def read_content(folder):
    items = []
    for path in sorted((ROOT / 'content' / folder).glob('*.md')):
        _, metadata, body = path.read_text().split('---', 2)
        item = json.loads(metadata)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['slug']):
            raise ValueError(f'Invalid slug: {path}')
        if item.get('date'):
            date.fromisoformat(item['date'])
        item['html'] = markdown.markdown(body, extensions=['tables', 'fenced_code', 'sane_lists'])
        item['minutes'] = max(1, round(len(re.findall(r'\b\w+\b', body)) / 220))
        item['url'] = item.get('external') or f"/{folder}/{item['slug']}/"
        items.append(item)
    if len({i['slug'] for i in items}) != len(items):
        raise ValueError('Duplicate content slug')
    return items


WORK = read_content('work')
ARTICLES = read_content('writing')
WORK_ORDER = ['connect-4-ai', 'financial-ai-assistant', 'disney-valuation', 'texas-unemployment', 'spotify-analysis', 'scansense-ai', 'michelin-analysis']
WORK.sort(key=lambda x: WORK_ORDER.index(x['slug']) if x['slug'] in WORK_ORDER else len(WORK_ORDER))
ARTICLES.sort(key=lambda x: {'japans-lost-decade': 0, 'ai-self-checkout': 1, 'finance-study-notes': 2}.get(x['slug'], 3))


def header(active=''):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if label.lower() == active else '')+f'>{label}</a>' for label, url in [('Home', '/'), ('About', '/about/'), ('Work', '/work/'), ('Writing', '/writing/'), ('Lab', '/lab/')])
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav-bar">
<a class="logo" href="/">Eshaan Arora<span class="logo-dot" aria-hidden="true">.</span></a>
<nav class="site-nav" aria-label="Primary">{nav}</nav>
<div class="header-actions"><a class="resume-link" href="{SITE['resume']}">Résumé <span aria-hidden="true">↗</span></a><button class="theme-toggle" data-theme-toggle type="button" aria-label="Switch to dark theme" aria-pressed="false"><span aria-hidden="true">◐</span><span data-theme-label>Light</span></button></div>
</div></header>'''


def footer():
    return f'''<footer class="footer"><div class="container footer-inner"><p>© <span data-year>{date.today().year}</span> Eshaan Arora</p><nav aria-label="Contact and social links"><a href="mailto:{SITE['email']}">Email</a><a href="{SITE['github']}">GitHub</a><a href="{SITE['linkedin']}">LinkedIn</a><a href="{SITE['substack']}">Substack</a></nav><a href="#main">Back to top ↑</a></div></footer>'''


def page(url, title, description, body, active='', extra_head='', body_attrs='', noindex=False):
    body = body.replace('<pre>', '<pre tabindex="0" aria-label="Code sample">')
    canonical = SITE['url'] + url
    structured = {'@context': 'https://schema.org', '@type': 'Person' if url == '/about/' else 'WebPage', 'name': 'Eshaan Arora' if url == '/about/' else title, 'url': canonical}
    if url == '/about/':
        structured['sameAs'] = [SITE['github'], SITE['linkedin'], SITE['substack']]
        structured['jobTitle'] = 'Operations and analytics professional'
    full_title = title + ' | Eshaan Arora' if title != 'Eshaan Arora — Operations, Analytics, and AI' else title
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title><meta name="description" content="{e(description, quote=True)}"><meta name="color-scheme" content="light dark">
<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{e(full_title, quote=True)}"><meta property="og:description" content="{e(description, quote=True)}"><meta property="og:type" content="website"><meta property="og:image" content="{SITE['url']}/assets/social-card.png"><meta name="twitter:card" content="summary_large_image">
<script src="/js/theme-init.js"></script><link rel="stylesheet" href="/css/styles.css"><script src="/js/main.js" defer></script>
<script type="application/ld+json">{json.dumps(structured).replace('<', chr(92)+'u003c')}</script>
{'<meta name="robots" content="noindex,follow">' if noindex else ''}{extra_head}</head>
<body {body_attrs}>{header(active)}<main id="main" tabindex="-1">{body}</main>{footer()}</body></html>'''
    output = ROOT / ('index.html' if url == '/' else url.lstrip('/') if url.endswith('.html') else url.strip('/') + '/index.html')
    output.parent.mkdir(parents=True, exist_ok=True)
    html = html.replace('↗', '<svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 13 13 3M3 3h10v10"/></svg>')
    output.write_text('\n'.join(line.rstrip() for line in html.splitlines()) + '\n')
    GENERATED.append({'url': url, 'path': str(output.relative_to(ROOT)), 'index': not noindex})


def intro(kicker, title, description):
    return f'<section class="page-intro container"><p class="eyebrow">{e(kicker)}</p><h1>{e(title)}</h1><p class="lede">{e(description)}</p></section>'


def card(item):
    img = f'<div class="project-visual"><img src="{item["image"]}" alt="{e(item["image_alt"], quote=True)}" loading="lazy" width="720" height="420"></div>' if item.get('image') else '<div class="project-visual type-visual" aria-hidden="true">{ }</div>'
    draft = ' draft' if 'draft' in item['status'] else ''
    return f'''<article class="project-card">{img}<div class="card-body"><div class="card-meta"><span>{e(item['category'])}</span><span class="status{draft}">{e(item['status'])}</span></div><h3><a href="{item['url']}">{e(item['title'])}<span aria-hidden="true"> ↗</span></a></h3><p>{e(item['description'])}</p><p class="tech-list">{' · '.join(e(t) for t in item['tools'])}</p></div></article>'''


def writing_row(item):
    when = f'<time datetime="{item["date"]}">{date.fromisoformat(item["date"]).strftime("%d %B %Y").lstrip("0")}</time>' if item.get('date') else ''
    reading = 'Read on Substack' if item.get('external') else str(item['minutes']) + (' min overview' if item.get('overview') else ' min read')
    metadata = '<br>'.join(part for part in [when, reading] if part)
    return f'''<article class="writing-row"><div><p class="eyebrow">{e(item['category'])}</p><h3><a href="{item['url']}">{e(item['title'])} <span aria-hidden="true">↗</span></a></h3><p>{e(item['description'])}</p></div><p class="writing-meta">{metadata}</p></article>'''


def contact():
    return f'''<section class="contact-section container" id="contact"><p class="eyebrow">Keep in touch</p><div class="contact-layout"><h2>Good work starts<br>with a conversation.</h2><div><p>For opportunities, technical collaborations, or a thoughtful exchange of ideas.</p><a class="text-link" href="mailto:{SITE['email']}">{SITE['email']} <span aria-hidden="true">↗</span></a></div></div></section>'''


def build_core():
    featured = ''.join(card(i) for i in WORK if i.get('featured'))
    home = f'''<section class="hero container"><div><p class="eyebrow">Operations, Analytics, and AI</p><h1>Making sense<br>of complex<br><em>systems.</em></h1><p class="hero-copy">I’m Eshaan — an operations and analytics professional at Uber, with a background in finance, economics, and applied machine learning. I work on business problems, build things with code, and explore ideas across technology, economics, and beyond.</p><div class="hero-cta"><a class="button button-primary" href="/work/">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="/about/">About me →</a></div></div><div class="hero-aside" id="about"><img class="portrait" src="/images/headshot.jpeg" width="280" height="280" alt="Eshaan Arora"><p class="eyebrow">At a glance</p><dl class="snapshot"><dt>Currently</dt><dd>Operations &amp; analytics<br><strong>Uber</strong></dd><dt id="experience">Education</dt><dd>MS, Business Analytics · UT Austin<br>Finance &amp; Economics · Florida State</dd><dt>Credentials</dt><dd>Certified Internal Auditor<br>Professional Scrum Master I</dd><dt id="skills">Practice</dt><dd>Forecasting · Financial analysis<br>Python · SQL · Machine learning</dd></dl></div></section>
<section class="section container" id="projects"><div class="section-heading"><div><p class="eyebrow">01 / Selected work</p><h2>Models, tools, and experiments.</h2></div><a class="text-link" href="/work/">All work →</a></div><div class="project-grid">{featured}</div></section>
<section class="experiment container"><div><p class="eyebrow">02 / From the lab</p><h2>A small board.<br>A lot of possibilities.</h2><p>Explore AI through a familiar game. Pick an opponent, plan your moves, and see how the match unfolds.</p><div class="hero-cta"><a class="button button-primary" href="/connect4/">Play Connect 4 →</a><a class="text-link" href="/work/connect-4-ai/">Read the case study</a></div></div><img src="/assets/connect4-board.svg" alt="Illustration of a Connect 4 board" width="720" height="420" loading="lazy"></section>
<section class="section container" id="writing"><div class="section-heading"><div><p class="eyebrow">03 / Selected writing</p><h2>Ideas worth spending time with.</h2></div><a class="text-link" href="/writing/">All writing →</a></div>{''.join(writing_row(i) for i in ARTICLES[:2])}</section>{contact()}'''
    page('/', 'Eshaan Arora — Operations, Analytics, and AI', 'Operations and analytics at Uber. Projects in finance and applied AI, writing on economics and technology, and independent experiments.', home, 'home')
    about = intro('About / Background & perspective', 'A quantitative background.\nA wider field of view.', 'I’m Eshaan Arora, an operations and analytics professional at Uber. My background connects finance, economics, and applied machine learning.') + f'''<div class="container about-layout"><article class="prose"><h2>How I approach work</h2><p>My work involves analytical problem-solving: using data and models to understand a business question, clarify assumptions, and support a decision. Forecasting, financial analysis, and operations are central to that practice.</p><p>Previous experience in financial and business environments informs how I think about trade-offs. Technical implementation matters, and so does explaining what a result means and where its limits lie.</p><h2>Education and credentials</h2><ul><li>Master of Science in Business Analytics — University of Texas at Austin.</li><li>Bachelor’s degrees in Finance and Economics — Florida State University.</li><li>Certified Internal Auditor (CIA).</li><li>Professional Scrum Master I (PSM I).</li></ul><h2>Selected skills</h2><p>Python, SQL, forecasting, financial modeling and analysis, machine learning, operations analytics, and clear technical communication.</p><h2>Beyond work</h2><p>Beyond my day-to-day work, I’m interested in economics, technology, and the questions that come from building something. My projects give those interests a practical outlet; writing gives me room to think them through.</p><p><a class="text-link" href="{SITE['resume']}">View my résumé (PDF) ↗</a></p></article><aside class="timeline"><p class="eyebrow">Professional timeline</p><ol><li><span>Current</span><h3>Uber</h3><p>Operations and analytics.</p></li><li><span>Earlier experience</span><h3>Financial &amp; business environments</h3><p>A foundation in analysis and business problem-solving.</p></li><li><span>Graduate education</span><h3>UT Austin</h3><p>MS in Business Analytics.</p></li><li><span>Undergraduate education</span><h3>Florida State University</h3><p>Finance and Economics.</p></li></ol></aside></div>{contact()}'''
    page('/about/', 'About', 'Eshaan Arora’s background in operations, analytics, finance, economics, and applied machine learning.', about, 'about')
    work = intro('Work / Selected projects', 'A closer look at the work.', 'Projects in analytics, finance, and applied AI: the questions behind them, what I built, and what I learned.') + f'<section class="container section"><h2 class="sr-only">Project case studies</h2><div class="project-grid">{"".join(card(i) for i in WORK if i.get('listed', True))}</div><div class="archive-note" id="amazonia"><h2>Earlier work &amp; resources</h2><p>Explore smaller finance programs and learning resources in the <a href="/lab/financial-tools/">Financial Tools collection</a> and <a href="/lab/archive/">archive</a>. You can also watch a <a href="https://www.youtube.com/watch?v=EAqpm_oeSso">recorded Amazonia Week seminar</a>.</p></div></section>'
    page('/work/', 'Work', 'Selected case studies in applied AI, financial valuation, economics, and data analysis.', work, 'work')
    writing = intro('Writing / Essays, research & notes', 'A place to think out loud.', 'Economics, technology, and ideas beyond the immediate problem. Selected papers and essays, with room for more.') + '<section class="container section"><nav class="category-nav" aria-label="Writing categories">'+''.join(f'<a href="#{slug}">{label}</a>' for slug, label in [('economics-finance', 'Economics & Finance'), ('technology-ai', 'Technology & AI'), ('notes-essays', 'Notes & Essays')])+'</nav>'
    for slug, label in [('economics-finance', 'Economics & Finance'), ('technology-ai', 'Technology & AI'), ('notes-essays', 'Notes & Essays')]:
        writing += f'<section class="writing-category" id="{slug}"><h2>{label}</h2>'+''.join(writing_row(i) for i in ARTICLES if i['category'] == label)+'</section>'
    writing += '<p class="index-note">Essays on Substack, research papers, and notes to return to.</p></section>'
    page('/writing/', 'Writing', 'Essays, papers, and notes on economics, finance, technology, and AI.', writing, 'writing')
    lab = intro('Lab / Tools & experiments', 'Build. Try. Learn.', 'Games, useful calculations, and smaller projects built to explore an idea.') + '''<section class="container section lab-grid"><article class="lab-card"><p class="eyebrow">01 / Play</p><h2>Connect 4 Playground</h2><p>Play the classic game against three AI opponents. Choose who goes first and try to get four in a row.</p><a class="button button-primary" href="/connect4/">Choose a mode →</a><a class="text-link" href="/work/connect-4-ai/">Case study</a></article><article class="lab-card"><p class="eyebrow">02 / Tools</p><h2>Financial Tools</h2><p>Explore how cash flows change over time with present value, future value, annuity, and bond calculators.</p><a class="button button-primary" href="/lab/financial-tools/">Open tools →</a></article><article class="lab-card"><p class="eyebrow">03 / Python project</p><h2>Spotify Listening History</h2><p>Explore listening patterns, favorite artists, and activity over time using your Spotify export. Download the Python program to run it locally.</p><a class="text-link" href="/lab/spotify-source/">Explore the program →</a><a class="text-link" href="/work/spotify-analysis/">Project overview</a></article><article class="lab-card"><p class="eyebrow">04 / Archived</p><h2>Earlier scripts &amp; notes</h2><p>Preserved Python finance programs, historical market data, and technical learning resources.</p><a class="text-link" href="/lab/archive/">Browse the archive →</a></article></section>'''
    page('/lab/', 'Lab', 'Interactive experiments, Connect 4, financial tools, and archived source programs.', lab, 'lab')


def build_content():
    for item in WORK:
        body = intro(item['category'], item['title'], item['description'])
        body += f'<div class="container case-layout"><aside class="case-meta"><p class="eyebrow">Project details</p><p class="status">{item["status"]}</p><p>{" · ".join(e(t) for t in item["tools"])}</p>'
        if item.get('date'): body += f'<p>Analysis date<br><time datetime="{item["date"]}">{item["date"]}</time></p>'
        headings = re.findall(r'<h2>(.*?)</h2>', item['html'])
        html = item['html']
        body += '<nav aria-label="Case study sections">'
        for n, title in enumerate(headings):
            html = html.replace(f'<h2>{title}</h2>', f'<h2 id="section-{n}">{title}</h2>', 1)
            body += f'<a href="#section-{n}">{title}</a>'
        body += f'</nav><a class="text-link" href="/work/">← All work</a></aside><article class="prose case-body">{html}</article></div>'
        page(item['url'], item['title'], item['description'], body, 'work', noindex=not item.get('listed', True))
    for item in ARTICLES:
        if item.get('external'): continue
        body = intro(item['category'], item['title'], item['description'])
        when = f'<time datetime="{item["date"]}">{item["date"]}</time> · ' if item.get('date') else ''
        reading = str(item['minutes']) + (' min overview' if item.get('overview') else ' min read')
        cover = item.get('cover')
        cover_html = f'<img src="{e(cover["src"], quote=True)}" alt="{e(cover["alt"], quote=True)}" width="{int(cover["width"])}" height="{int(cover["height"])}">' if cover else ''
        body += f'<article class="container reading prose"><p class="article-meta">{when}{reading}</p>{cover_html}{item["html"]}'
        if item.get('references'):
            body += '<h2>Further reading</h2><ul>'+''.join(f'<li><a href="{e(r["url"], quote=True)}">{e(r["title"])}</a></li>' for r in item['references'])+'</ul>'
        if item.get('related'):
            body += '<h2>Related reading</h2>'+''.join(f'<p><a href="{i["url"]}">{e(i["title"])}</a></p>' for i in ARTICLES if i['slug'] in item['related'])
        body += '<p><a class="text-link" href="/writing/">← All writing</a></p></article>'
        page(item['url'], item['title'], item['description'], body, 'writing')


def build_lab():
    modes = [('play-transformer','transformer','Casual','Transformer'), ('play-cnn','cnn','Challenge','CNN'), ('play-policy-gradient','pg','Insane','Policy gradient')]
    mode_descriptions = {
        'transformer': 'Start a match with the transformer opponent and find your rhythm on the board.',
        'cnn': 'Put your strategy to the test against the CNN opponent.',
        'pg': 'Try the policy-gradient opponent and see how the game unfolds.'
    }
    nav = '<nav class="game-mode-nav" aria-label="Connect 4 modes"><a href="/connect4/">Playground</a>'+''.join(f'<a href="/connect4/{slug}/">{label}</a>' for slug, _, label, _ in modes)+'<a href="/work/connect-4-ai/">Case study</a></nav>'
    home = intro('Lab / Connect 4', 'Your move.', 'The classic game, with an AI across the board. Choose a mode, decide who goes first, and try to connect four.')
    home += '<section class="container section">'+nav+'<div class="mode-grid">'+''.join(f'<article class="lab-card"><p class="eyebrow">{model}</p><h2>{label} mode</h2><p>{mode_descriptions[model_id]}</p><a class="button button-primary" href="/connect4/{slug}/">Play {label.lower()} →</a></article>' for slug, model_id, label, model in modes)+'</div><p><a href="/connect4/training-methodology/">How to play and meet the opponents →</a></p></section>'
    page('/connect4/', 'Connect 4 Playground', 'Choose one of three Connect 4 opponent modes and play in your browser.', home, 'lab')
    for slug, model_id, label, model in modes:
        original = (ROOT / 'content/legacy' / f'connect4--{slug}--index.html').read_text()
        original = re.sub(r'<div class="section-header" data-reveal>.*?</div>', '', original, count=1, flags=re.S)
        original = original.replace('role="grid"', 'role="group"')
        original = original.replace('User wins', 'Your wins').replace('AI wins', 'Opponent wins')
        original = original.replace('Tip: Click any column to drop your piece. The AI will respond automatically.', 'Select a column to drop your piece. Connect four in a row to win.')
        original = re.sub(r'Match record \([^<]+\)', 'Your match record', original)
        original = original.replace('our bespoke CNN-based model', 'the CNN API route')
        original = original.replace('our bespoke transformer model', 'the transformer API route')
        body = intro('Lab / Connect 4', f'{label} mode', f'Play against the {model.lower() if model != "CNN" else model} opponent. Choose who goes first, then make your move.')
        body += '<div class="container">'+nav+'<p class="small muted">Your match record is saved in this browser. <a href="/connect4/training-methodology/#connection">Playing offline?</a></p></div>'+original
        page(f'/connect4/{slug}/', f'Connect 4 — {label} mode', f'Play Connect 4 against the {model} opponent in {label} mode.', body, 'lab', extra_head='<link rel="stylesheet" href="/connect4/assets/connect4.css"><script src="/connect4/assets/connect4.js" defer></script>', body_attrs=f'data-opponent="{model_id}"')
    body = intro('Lab / Connect 4', 'Meet the game.', 'A quick guide to the rules, the opponents, and what happens between moves.') + '<article class="container reading prose">'+markdown.markdown('''## Four in a row

Choose who goes first and start a match. Select a column to drop a piece into its lowest available space. Connect four pieces horizontally, vertically, or diagonally before your opponent does. If the board fills without a winner, the match is a draw.

## Meet the opponents

**Casual** pairs you with the transformer opponent. **Challenge** uses a convolutional neural network (CNN). **Insane** uses the policy-gradient opponent. Choose a mode to explore its approach to the same board and rules.

## Between moves

The browser keeps track of the board and checks the rules. After your turn, it sends the board to the AI service and waits for the opponent's move. Your match record is saved in this browser so you can return for another game.

<h2 id="connection">If the connection drops</h2>

If the AI service is unavailable, the game can continue with randomly selected legal moves. These are fallback moves rather than decisions from your chosen model.

## A closer look

This project explores how machine learning and a clear, responsive interface come together in a game. Read the case study for the design and technical approach, or head straight to the board.

[Read the case study](/work/connect-4-ai/) · [Choose a mode and play](/connect4/)
''')+'</article>'
    page('/connect4/training-methodology/', 'How Connect 4 Works', 'Learn the rules, meet the three AI opponents, and see how Connect 4 works between moves.', body, 'lab')
    fields = '''<label>Amount / face value ($)<input name="amount" type="number" step="any" min="0" value="1000" required></label><label>Rate / yield (% per period)<input name="rate" type="number" step="any" min="-99.999" value="5" required></label><label>Number of periods<input name="periods" type="number" step="1" min="0" max="1000" value="10" required></label><label>Coupon rate (% per period)<input name="coupon" type="number" step="any" min="0" value="5" required></label>'''
    tools = intro('Lab / Financial tools', 'A few useful calculations.', 'Explore what a cash flow is worth today, how it grows, or how a bond is priced. Your inputs stay in your browser.') + f'''<section class="container tool-layout"><form id="financial-form" class="lab-card"><h2>Calculate</h2><label>Calculation<select name="kind"><option value="future">Future value</option><option value="present">Present value</option><option value="annuity">Ordinary annuity present value</option><option value="bond">Fixed-coupon bond price</option></select></label>{fields}<button class="button button-primary" type="submit">Calculate →</button><output id="financial-result" aria-live="polite">Enter your assumptions to calculate.</output></form><article class="prose"><h2>Conventions &amp; formulas</h2><p>The rate and number of periods must use the same frequency. For a semiannual bond, use semiannual yield and coupon rate with the number of half-year periods. Cash flows occur at period end.</p><ul><li>Future value: PV × (1 + r)<sup>n</sup>.</li><li>Present value: FV / (1 + r)<sup>n</sup>.</li><li>Ordinary annuity: C × [1 − (1 + r)<sup>−n</sup>] / r. At zero rate, C × n.</li><li>Bond price: present value of coupons plus discounted face value. At zero yield: face value + coupons × n.</li></ul><p>For annuities, amount is the payment each period. For bonds, it is the face value. At zero periods, a bond returns face value and an annuity returns zero. Rates above −100% are supported; periods must be whole numbers from 0 to 1,000. Results that exceed finite numeric range are rejected.</p><p>These are nominal, deterministic calculations. They exclude taxes, fees, accrued interest, default risk, and embedded options.</p><h2>Earlier Python programs</h2><p>Explore the earlier Python programs that grew out of these finance concepts.</p><ul><li><a href="/bond-calculator-code.html">Bond pricing source</a></li><li><a href="/present-future-value-calculator.html">PV/FV source</a></li><li><a href="/stock_quotes.html">Quote-fetching source</a></li></ul></article></section>'''
    page('/lab/financial-tools/', 'Financial Tools', 'Browser calculators for present value, future value, ordinary annuities, and fixed-coupon bonds.', tools, 'lab', extra_head='<script src="/js/financial-tools.js" defer></script>')
    source_notes = {
        'bond-pricing': 'This Python program calculates bond prices and plots pricing relationships. Download it and set up its Python libraries to run it locally.',
        'present-future-value': 'An archived Python learning project covering cash flows and growth phases. For standard present-value and future-value calculations, use the browser financial tools.',
        'stock-quotes': 'This Python program retrieves quotes through a Yahoo Finance API service. Running it requires your own API credentials and access to that service.',
        'spotify-analysis': 'Run this program locally with your Spotify extended listening-history export. Update the file paths for your machine; mapping also requires a GeoLite2 database.'
    }
    for url, filename, title in [('/bond-calculator-code.html', 'bond-pricing', 'Bond Pricing in Python'), ('/present-future-value-calculator.html', 'present-future-value', 'Cash Flow Calculations in Python'), ('/stock_quotes.html', 'stock-quotes', 'Yahoo Finance Quote Fetcher'), ('/lab/spotify-source/', 'spotify-analysis', 'Spotify Listening History in Python')]:
        code = (ROOT / f'content/sources/{filename}.py').read_text()
        body = intro('Lab / Archived source', title, 'Read the program below or download it to run on your own machine.')
        body += f'<article class="container reading prose"><p class="notice">{source_notes[filename]}</p><p><a href="/content/sources/{filename}.py" download>Download Python source</a> · <a href="/lab/financial-tools/">Browser financial tools</a></p><pre><code class="language-python">{e(code)}</code></pre></article>'
        page(url, title, f'Read and download the Python program: {title}.', body, 'lab')
    archive = intro('Lab / Archive', 'Keep the useful history.', 'Earlier programs, a historical market snapshot, and notes from my studies.') + '''<article class="container reading prose"><h2>Programs</h2><ul><li><a href="/bond-calculator-code.html">Bond pricing and graphing source</a></li><li><a href="/present-future-value-calculator.html">Present/future value source</a></li><li><a href="/stock_quotes.html">Yahoo Finance quote fetcher source</a></li><li><a href="/lab/spotify-source/">Spotify listening analysis source</a></li></ul><h2>Historical market snapshot</h2><p><a href="/market_dashboard.html">Market table — 18 February 2025</a>. Static historical data, not a live feed.</p><h2>Learning resources</h2><ul><li><a href="/documents/Finance_Final.pdf">Finance study guide</a></li><li><a href="/documents/Unsupervised_Learning_Final_Study_Guide-Final.pdf">Unsupervised learning study guide</a></li><li><a href="/documents/AML_Exam_Study_Guide_11_11_24.pdf">Applied machine learning notes — original</a></li><li><a href="/documents/AML_Exam_Study_Guide_11_11_24_Final.pdf">Applied machine learning notes — final</a></li></ul></article>'''
    page('/lab/archive/', 'Archive', 'Preserved Python programs, historical market data, and learning resources.', archive, 'lab')
    snapshot = (ROOT / 'content/legacy/market_dashboard.html').read_text().replace('border="1"', '').replace('<table>', '<table><caption>Historical market snapshot from the original website</caption>')
    page('/market_dashboard.html', 'Market Snapshot — February 2025', 'A preserved historical market table from 18 February 2025. Not live market data.', intro('Lab / Historical archive', 'Market snapshot.', 'Market values recorded on 18 February 2025.')+'<section class="container reading table-scroll" tabindex="0" aria-label="Historical market table">'+snapshot+'</section>', 'lab')


def build_compatibility():
    aliases = {'/portfolio.html':'/work/', '/blog.html':'/writing/', '/disney-analysis.html':'/work/disney-valuation/', '/spotify-data-analysis.html':'/work/spotify-analysis/', '/msba-capstone/':'/work/financial-ai-assistant/', '/square-apm-portfolio/':'/work/'}
    for old, new in aliases.items():
        page(old, 'This page has moved', 'Follow this project to its current location.', intro('Updated address', 'This page has moved.', 'Follow the link below to its new home.')+f'<div class="container section"><p><a class="button button-primary" href="{new}">Continue to the page →</a></p></div>', extra_head=f'<meta http-equiv="refresh" content="1;url={new}"><script src="/js/legacy-redirect.js" defer></script>', noindex=True)
        path = ROOT / (old.strip('/')+'/index.html' if old.endswith('/') else old.lstrip('/'))
        html = path.read_text().replace(f'{SITE["url"]}{old}', f'{SITE["url"]}{new}')
        path.write_text(html)
    resume = intro('Résumé / PDF', 'Résumé', 'View or download my résumé.')+f'<section class="container section"><p><a class="button button-primary" href="{SITE["resume"]}" download>Download résumé (PDF) ↗</a></p><iframe class="resume-embed" src="{SITE["resume"]}" title="Eshaan Arora résumé PDF" loading="lazy"></iframe><p>If the viewer doesn’t load, <a href="{SITE["resume"]}">open the PDF directly</a>.</p></section>'
    page('/resume.html', 'Résumé', 'View or download Eshaan Arora’s résumé PDF.', resume)
    page('/contact.html', 'Contact', 'Contact Eshaan Arora about opportunities, projects, or ideas.', intro('Contact', 'Let’s connect.', 'For professional opportunities, collaboration, or a conversation about ideas.')+contact())
    # Optional configuration, not installed as production vercel.json.
    redirects = [{'source':old.rstrip('/'), 'destination':new, 'permanent':True} for old,new in aliases.items()]
    for old, new in aliases.items():
        if old.endswith('/'): redirects.append({'source':old+'index.html','destination':new,'permanent':True})
    redirects.append({'source':'/index.html','destination':'/','permanent':True})
    (ROOT/'docs/vercel-redirects.example.json').write_text(json.dumps({'redirects':redirects},indent=2)+'\n')


def verify_preserved():
    manifest = json.loads((ROOT/'docs/preserved-assets.json').read_text())
    for path, expected in manifest.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'Protected file changed: {path}')


if __name__ == '__main__':
    verify_preserved()
    build_core()
    build_content()
    build_lab()
    build_compatibility()
    urls = sorted({i['url'] for i in GENERATED if i['index']})
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE["url"]}{url}</loc></url>\n' for url in urls)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sitemap)
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /content/\nDisallow: /docs/\nDisallow: /scripts/\nSitemap: {SITE["url"]}/sitemap.xml\n')
    (ROOT/'docs/generated-pages.json').write_text(json.dumps(GENERATED,indent=2)+'\n')
    verify_preserved()
    print(f'Generated {len(GENERATED)} pages; all protected file hashes unchanged.')
