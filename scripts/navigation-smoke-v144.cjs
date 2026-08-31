const { chromium } = require(process.cwd() + '/node_modules/playwright');
const BASE='https://kssafonova.github.io/kd';
const assert=(value,message)=>{if(!value)throw new Error(message)};

(async()=>{
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext({viewport:{width:390,height:844},locale:'ru-RU'});
  const page=await context.newPage();
  const diagnostics=[];
  const timings=[];
  page.on('pageerror',e=>diagnostics.push(`PAGEERROR ${e.message}`));
  page.on('requestfailed',r=>diagnostics.push(`FAILED ${r.url()} ${r.failure()?.errorText||''}`));

  async function goto(path,selector){
    await page.goto(BASE+path,{waitUntil:'domcontentloaded',timeout:60000});
    if(selector)await page.waitForSelector(selector,{timeout:15000});
  }
  async function home(){await goto('/','.home-fast')}
  async function catalog(){await goto('/catalog/','.view-catalog .product-grid .product-card')}
  async function closeOverlay(){
    const close=page.getByRole('button',{name:'Закрыть'}).first();
    if(await close.count())await close.click().catch(()=>{});
  }
  async function homeAction(name,label){
    await home();
    const start=Date.now();
    await page.getByRole('button',{name}).first().click();
    await page.waitForURL(url=>url.pathname.includes('/kd/catalog'),{timeout:12000});
    await page.waitForSelector('.overlay',{state:'visible',timeout:12000});
    timings.push([label,Date.now()-start]);
  }

  // Homepage menu and route coverage.
  await home();
  await page.getByRole('button',{name:'Открыть меню'}).click();
  await page.waitForSelector('.home-fast-menu',{state:'visible',timeout:4000});
  assert(await page.locator('.home-fast-menu a[href*="/capsules/"]').count()>0,'Homepage menu: capsules link missing');
  assert(await page.locator('.home-fast-menu a[href*="/collections/"]').count()>0,'Homepage menu: collections link missing');
  await page.getByRole('button',{name:'Закрыть'}).click();

  await homeAction('Поиск','home->search');
  await homeAction('Профиль','home->profile');
  await homeAction(/Избранное/,'home->favorites');
  await homeAction('Корзина','home->cart');

  // Homepage "Новинки" must use catalog product-card anatomy and open the real product flow.
  await home();
  assert(await page.locator('.home-fast-new .product-card').count()>=4,'Homepage New Products do not use catalog cards');
  const firstHomeProduct=page.locator('.home-fast-new .product-card .product-image').first();
  await firstHomeProduct.scrollIntoViewIfNeeded();
  const productStart=Date.now();
  await firstHomeProduct.click();
  await page.waitForURL(url=>url.pathname.includes('/kd/catalog'),{timeout:12000});
  await page.waitForSelector('.product-page',{state:'visible',timeout:12000});
  timings.push(['home->product',Date.now()-productStart]);
  assert(await page.locator('.product-page .purchase-cta').count()>0,'Homepage product did not open the catalog PDP form');

  // Catalog initial render, category slider, filter and sort.
  await catalog();
  const title=await page.locator('.title-line').innerText();
  assert(title.includes('139'),'Catalog initial count is not 139');
  assert(await page.locator('.catalog-category-slider-v141').count()===1,'Catalog category slider missing');
  await page.getByRole('tab',{name:'Декор для дома'}).click();
  await page.waitForFunction(()=>document.querySelector('.title-line h1')?.textContent?.includes('Декор для дома'),null,{timeout:5000});
  await page.locator('.catalog-filter-trigger-v123').click();
  await page.waitForSelector('.catalog-filter-layer-v123',{state:'visible',timeout:4000});
  assert(await page.locator('.catalog-filter-drawer-v123').count()===1,'Filter drawer did not open');
  await page.locator('.catalog-filter-header-v123 > button').click();
  await page.waitForSelector('.catalog-filter-layer-v123',{state:'detached',timeout:4000});
  await page.locator('.catalog-sort-v123 select').selectOption('price_asc');
  assert(await page.locator('.catalog-sort-v123 select').inputValue()==='price_asc','Sort did not switch');

  // Catalog menu and all global header actions.
  await catalog();
  await page.getByRole('button',{name:'Открыть меню'}).click();
  await page.waitForSelector('.navigation-overlay',{state:'visible',timeout:4000});
  assert(await page.locator('.navigation-overlay a[href*="/capsules/"]').count()>0,'Catalog menu capsules route missing');
  assert(await page.locator('.navigation-overlay a[href*="/collections/"]').count()>0,'Catalog menu collections route missing');
  await page.locator('.navigation-overlay .menu-top button').first().click();

  for(const [name,label] of [['Поиск','catalog-search'],['Профиль','catalog-profile'],['Корзина','catalog-cart']]){
    await catalog();
    const start=Date.now();
    await page.getByRole('button',{name}).first().click();
    await page.waitForSelector('.overlay',{state:'visible',timeout:5000});
    timings.push([label,Date.now()-start]);
    await closeOverlay();
  }
  await catalog();
  const favStart=Date.now();
  await page.getByRole('button',{name:/Избранное/}).first().click();
  await page.waitForSelector('.overlay',{state:'visible',timeout:5000});
  timings.push(['catalog-favorites',Date.now()-favStart]);
  await closeOverlay();

  // Product card from PLP opens the same PDP and global logo returns home.
  await catalog();
  await page.locator('.product-grid .product-card .product-image').first().click();
  await page.waitForSelector('.product-page',{state:'visible',timeout:5000});
  assert(await page.locator('.product-page .purchase-cta').count()>0,'Catalog product PDP missing purchase form');
  await page.locator('.header .logo').click();
  await page.waitForURL(url=>url.pathname==='/'||url.pathname==='/kd/'||url.pathname==='/kd',{timeout:12000});

  // Static routing pages should be available without a heavy client bootstrap.
  await goto('/capsules/','.story-index-grid');
  assert(await page.locator('.story-index-grid article').count()>=3,'Capsules routing page is empty');
  assert(await page.locator('.story-index-grid a[href*="capsule="]').count()>=3,'Capsule cards are not linked to catalog');
  await goto('/collections/','.story-index-grid');
  assert(await page.locator('.story-index-grid article').count()>=3,'Collections routing page is empty');
  assert(await page.locator('.story-index-grid a[href*="collection="]').count()>=3,'Collection cards are not linked');

  // Direct query bridges from external links/bookmarks.
  await goto('/catalog/?open=account','.overlay');
  await goto('/catalog/?open=search','.overlay');
  await goto('/catalog/?open=cart','.overlay');
  await goto('/catalog/?product=KD-PD-1024','.product-page');

  console.log('NAV_TIMINGS_MS',JSON.stringify(Object.fromEntries(timings)));
  const perf=await page.evaluate(()=>{
    const nav=performance.getEntriesByType('navigation')[0];
    const resources=performance.getEntriesByType('resource');
    return {dcl:nav?Math.round(nav.domContentLoadedEventEnd):null,load:nav?Math.round(nav.loadEventEnd):null,resources:resources.length,js:resources.filter(r=>/\.js($|\?)/.test(r.name)).length,css:resources.filter(r=>/\.css($|\?)/.test(r.name)).length};
  });
  console.log('NAV_PERF',JSON.stringify(perf));
  if(diagnostics.length)console.log('BROWSER_DIAGNOSTICS\n'+diagnostics.join('\n'));
  console.log('NAVIGATION_SMOKE_V144_OK');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});
