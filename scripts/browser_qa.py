"""Browser verification. Requires Playwright, Chromium, local server, and axe-core.

Usage: python scripts/browser_qa.py --axe /tmp/axe.min.js
No model benchmarks: inference is mocked so behavior is reproducible.
"""
import argparse,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8080');parser.add_argument('--axe',required=True);args=parser.parse_args()
qa=ROOT/'.qa';qa.mkdir(exist_ok=True)
rows=json.loads((ROOT/'docs/generated-pages.json').read_text())
report={'page_checks':[],'game_checks':[],'compatibility':[],'errors':[],'accessibility':[]}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for theme in ['light','dark']:
        for label,width,height in [('desktop',1440,1000),('mobile',390,844)]:
            context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme)
            context.route('https://api-connect4.eshaanarora.com/**',lambda route:route.fulfill(json={'status':'ok','best_move':6}))
            page=context.new_page(); errors=[];page.on('pageerror',lambda error: errors.append(str(error)))
            for row in rows:
                if not row['index']:continue
                page.goto(args.base+row['url'],wait_until='networkidle')
                # Force lazy visuals to load before inspecting full-page screenshots.
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)');page.wait_for_timeout(80)
                page.evaluate('window.scrollTo(0,0)')
                size=page.evaluate('({viewport:innerWidth,document:document.documentElement.scrollWidth})')
                assert size['document']<=width, f"Overflow {theme}/{label} {row['url']}: {size}"
                assert page.locator('h1').count()==1
                assert page.locator('nav[aria-label="Primary"] a').count()==5
                page.add_script_tag(path=args.axe)
                violations=page.evaluate("async () => (await axe.run(document, {runOnly: {type:'tag', values:['wcag2a','wcag2aa','wcag21aa','best-practice']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))")
                if violations:report['accessibility'].append({'url':row['url'],'theme':theme,'viewport':label,'violations':violations})
                report['page_checks'].append({'url':row['url'],'theme':theme,'viewport':label,'overflow':False})
                if row['url'] in ['/','/about/','/work/disney-valuation/','/connect4/play-cnn/','/lab/financial-tools/']:
                    page.screenshot(path=str(qa/f"{row['url'].strip('/').replace('/','-') or 'home'}-{theme}-{label}.png"),full_page=True)
            report['errors'].extend(errors);context.close()
            print(f'Checked {theme}/{label}',flush=True)
    context=browser.new_context();page=context.new_page()
    for old,new in [('/portfolio.html#amazonia','/work/#amazonia'),('/blog.html','/writing/'),('/disney-analysis.html','/work/disney-valuation/'),('/spotify-data-analysis.html','/work/spotify-analysis/'),('/msba-capstone/index.html','/work/financial-ai-assistant/'),('/square-apm-portfolio/','/work/')]:
        page.goto(args.base+old);page.wait_for_url(args.base+new)
        report['compatibility'].append({'old':old,'destination':new,'passed':True})
    # Manual override persists, system preference applies without saved selection.
    page.goto(args.base+'/');page.locator('[data-theme-toggle]').click();page.reload()
    assert page.locator('html').get_attribute('data-theme')=='dark'
    assert page.locator('[data-theme-toggle]').get_attribute('aria-pressed')=='true'
    page.goto(args.base+'/lab/financial-tools/');page.locator('#financial-form button').click()
    assert page.locator('#financial-result').inner_text()=='$1,628.89'
    context.close()
    for slug,model in [('play-transformer','transformer'),('play-cnn','cnn'),('play-policy-gradient','pg')]:
        context=browser.new_context();page=context.new_page();requests=[]
        def infer(route):
            if route.request.method=='POST':requests.append(route.request.post_data_json)
            route.fulfill(json={'status':'ok','best_move':6})
        context.route('https://api-connect4.eshaanarora.com/**',infer)
        page.goto(args.base+'/connect4/'+slug+'/');page.wait_for_load_state('networkidle')
        assert page.locator('#connect4-board button').count()==42
        page.locator('#connect4-start').click()
        for turn in range(4):
            page.locator('#connect4-board button[data-col="0"]').first.click()
            if turn<3:page.wait_for_function('document.querySelector("#connect4-status").textContent === "Your turn."')
        assert 'You win' in page.locator('#connect4-status').inner_text()
        assert page.locator('#connect4-user-wins').inner_text()=='1'
        assert requests[0]['modelType']==model and requests[0]['board'][5][0]==1
        page.reload();page.wait_for_load_state('networkidle');assert page.locator('#connect4-user-wins').inner_text()=='1'
        page.locator('input[value="ai"]').check();page.locator('#connect4-start').click()
        page.wait_for_function('document.querySelector("#connect4-status").textContent === "Your turn."')
        page.locator('#connect4-board button[data-col="0"]').first.click()
        page.wait_for_function('document.querySelector("#connect4-status").textContent === "Your turn."')
        assert requests[-1]['board'][5][0]==2 and requests[-1]['board'][5][6]==1
        page.locator('#connect4-resign').click();assert 'resigned' in page.locator('#connect4-status').inner_text()
        page.locator('#connect4-reset').click();assert page.locator('#connect4-board .is-red, #connect4-board .is-blue').count()==0
        report['game_checks'].append({'mode':model,'board':42,'user_first_encoding':True,'ai_first_encoding':True,'vertical_win':True,'persistence':True,'resign_reset':True})
        context.close()
    for fallback in ['failure','invalid']:
        context=browser.new_context();page=context.new_page()
        context.route('https://api-connect4.eshaanarora.com/**',lambda route:route.fulfill(status=503,json={'error':'unavailable'}) if fallback=='failure' else route.fulfill(json={'status':'ok','best_move':8}))
        page.goto(args.base+'/connect4/play-cnn/');page.wait_for_load_state('networkidle')
        page.locator('#connect4-start').click();page.locator('#connect4-board button[data-col="3"]').first.click()
        page.wait_for_function('document.querySelector("#connect4-status").textContent === "Your turn."')
        assert page.locator('#connect4-board .is-red').count()==1 and page.locator('#connect4-board .is-blue').count()==1
        report['game_checks'].append({'fallback':fallback,'legal_move':True});context.close()
    browser.close()
(qa/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['errors'],report['errors']
assert not report['accessibility'],report['accessibility']
print(f"PASS: {len(report['page_checks'])} responsive/theme checks, {len(report['compatibility'])} migrations, {len(report['game_checks'])} game scenarios, zero axe violations.")
