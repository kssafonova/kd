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

  // Homepage stays lightweight and opens the exact same shared premium menu
  // locally, without a wasteful route transition through catalog.
  await home();
  const menuStart=Date.now();
  await page.getByRole('button',{name:'Открыть меню'}).click();
  await page.waitForSelector('.navigation-overlay .menu-panel',{state:'visible',timeout:4000});
  timings.push(['home->menu',Date.now()-menuStart]);
  assert(!page.url().includes('/catalog'),'Homepage menu should open in place');
  assert(await page.getByRole('button',{name:/КАПСУЛЫ И КОЛЛЕКЦИИ/i}).count()>0,'Unified Kultura menu: capsules and collections action missing');
  assert(await page.getByRole('button',{name:/ГОТОВЫЕ РЕШЕНИЯ/i}).count()>0,'Unified Kultura menu: ready solutions action missing');
  assert(await page.locator('.navigation-overlay .premium-menu').count()===1,'Unified Kultura premium menu missing');
  await page.getByRole('button',{name:'Закрыть меню'}).click();

  await homeAction('Поиск','home->search');
  await homeAction('Профиль','home->profile');
  await homeAction(/Избранное/,'home->favorites');
  await homeAction('Корзина','home->cart');

  // Homepage New Products use catalog ProductCard anatomy and icons. Media/title
  // open canonical PDP; quick icon opens the canonical Kultura quick-add flow.
  await home();
  assert(await page.locator('.home-fast-new .product-card').count()>=4,'Homepage New Products do not use catalog cards');
  assert(await page.locator('.home-fast-new .product-card .heart').count()>=4,'Homepage New Products hearts missing');
  assert(await page.locator('.home-fast-new .product-card .quick .cart-add-icon').count()>=4,'Homepage New Products cart-add icons missing');
  const firstHomeProduct=page.locator('.home-fast-new .product-card .product-image').first();
  await firstHomeProduct.scrollIntoViewIfNeeded();
  const productStart=Date.now();
  await firstHomeProduct.click();
  await page.waitForURL(url=>url.pathname.includes('/kd/catalog'),{timeout:12000});
  await page.waitForSelector('.product-page',{state:'visible',timeout:12000});
  timings.push(['home->product',Date.now()-productStart]);
  assert(await page.locator('.product-page .primary').count()>0,'Homepage product did not open the Kultura PDP purchase form');

  await home();
  const quick=page.locator('.home-fast-new .product-card .quick').first();
  await quick.scrollIntoViewIfNeeded();
  await quick.click();
  await page.waitForURL(url=>url.pathname.includes('/kd/catalog'),{timeout:12000});
  await page.waitForSelector('.plp-size-overlay,.plp-size-flow,.overlay',{state:'visible',timeout:12000});

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

  // Catalog uses the same shared premium menu as home.
  await catalog();
  await page.getByRole('button',{name:'Открыть меню'}).click();
  await page.waitForSelector('.navigation-overlay .menu-panel',{state:'visible',timeout:4000});
  assert(await page.getByRole('button',{name:/КАПСУЛЫ И КОЛЛЕКЦИИ/i}).count()>0,'Catalog unified menu story action missing');
  assert(await page.getByRole('button',{name:/ГОТОВЫЕ РЕШЕНИЯ/i}).count()>0,'Catalog unified menu ready solutions action missing');
  await page.getByRole('button',{name:'Закрыть меню'}).click();

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
  assert(await page.locator('.product-page .primary').count()>0,'Catalog product PDP missing purchase form');
  await page.locator('.header .logo').click();
  await page.waitForURL(url=>url.pathname==='/'||url.pathname==='/kd/'||url.pathname==='/kd',{timeout:12000});

  // Capsules and collections are one lightweight server-rendered landing. Both
  // legacy URLs remain valid and expose both groups for backwards compatibility.
  for(const path of ['/collections/','/capsules/']){
    await goto(path,'.story-index-page');
    assert((await page.locator('.section-head h1').innerText()).includes('Капсулы и коллекции'),`${path}: combined title missing`);
    assert(await page.locator('#capsules').count()===1,`${path}: capsules section missing`);
    assert(await page.locator('#collections').count()===1,`${path}: collections section missing`);
    assert(await page.locator('#capsules a[href*="capsule="]').count()>=3,`${path}: capsule cards are not linked`);
    assert(await page.locator('#collections a[href*="collection="]').count()>=3,`${path}: collection cards are not linked`);
  }

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
  console.log('NAVIGATION_SMOKE_V148_OK');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});