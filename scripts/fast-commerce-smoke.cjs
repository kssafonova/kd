const { chromium } = require(process.cwd() + '/node_modules/playwright');
const BASE='https://kssafonova.github.io/kd';
const assert=(value,message)=>{if(!value)throw new Error(message)};

(async()=>{
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext({viewport:{width:390,height:844},locale:'ru-RU'});
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(`PAGEERROR ${e.message}`));
  page.on('requestfailed',r=>errors.push(`FAILED ${r.url()} ${r.failure()?.errorText||''}`));

  async function ready(path){
    await page.goto(BASE+path,{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForSelector('.fast-site',{timeout:20000});
  }
  async function openByLabel(label){
    await page.getByRole('button',{name:label}).first().click();
    await page.waitForSelector('.fast-overlay',{state:'visible',timeout:5000});
  }
  async function close(){
    const button=page.getByRole('button',{name:'Закрыть'}).first();
    if(await button.count())await button.click();
    await page.waitForSelector('.fast-overlay',{state:'detached',timeout:5000}).catch(()=>{});
  }

  await ready('/');
  await openByLabel('Меню');
  assert(await page.getByRole('link',{name:'Капсулы'}).count()>0,'Menu capsules link missing');
  assert(await page.getByRole('link',{name:'Коллекции'}).count()>0,'Menu collections link missing');
  await close();

  await openByLabel('Поиск');
  const search=page.getByPlaceholder('Что вы ищете?');
  await search.fill('Алая');
  await page.waitForSelector('.fast-search-results button',{timeout:5000});
  assert(await page.locator('.fast-search-results button').count()>0,'Search returned no products');
  await close();

  await openByLabel('Профиль');
  assert(await page.locator('.fast-account input').count()===1,'Profile form missing');
  await close();
  await openByLabel('Избранное');
  await close();
  await openByLabel('Корзина');
  await close();

  const homeProduct=page.locator('.fast-product-rail .fast-product-image').first();
  await homeProduct.scrollIntoViewIfNeeded();
  await homeProduct.click();
  await page.waitForSelector('.fast-quick',{timeout:5000});
  assert(await page.locator('.fast-quick .fast-primary').count()>0,'Home product quick view missing');
  await close();

  await ready('/catalog/');
  await page.waitForSelector('.fast-product-grid .fast-product-card',{timeout:10000});
  const title=await page.locator('.fast-catalog-title').innerText();
  assert(title.includes('139'),'Catalog does not expose 139 products on initial load');

  await page.locator('.fast-catalog-tools > button').click();
  await page.waitForSelector('.fast-filter-drawer',{timeout:5000});
  await page.locator('.fast-filter-drawer .fast-icon-btn').click();
  await page.locator('.fast-catalog-tools select').selectOption('price_asc');

  await page.locator('.fast-product-grid .fast-product-image').first().click();
  await page.waitForSelector('.fast-quick',{timeout:5000});
  await page.locator('.fast-quick .fast-primary').click();
  await page.waitForSelector('.fast-cart-list article',{timeout:5000});
  assert(await page.locator('.fast-cart-list article').count()>0,'Add to cart did not create cart item');
  await close();

  await ready('/capsules/');
  assert(await page.locator('.fast-stories-grid > a').count()>0,'Capsules index empty');
  await ready('/collections/');
  assert(await page.locator('.fast-stories-grid > a').count()>0,'Collections index empty');

  await ready('/catalog/?open=search');
  await page.waitForSelector('.fast-search-box',{timeout:5000});
  await close();
  await ready('/catalog/?open=cart');
  await page.waitForSelector('.fast-drawer',{timeout:5000});

  const perf=await page.evaluate(()=>{
    const nav=performance.getEntriesByType('navigation')[0];
    const resources=performance.getEntriesByType('resource');
    return {
      domContentLoaded:nav?Math.round(nav.domContentLoadedEventEnd):null,
      load:nav?Math.round(nav.loadEventEnd):null,
      resources:resources.length,
      js:resources.filter(r=>r.name.includes('.js')).length,
      css:resources.filter(r=>r.name.includes('.css')).length
    };
  });
  console.log('FAST_COMMERCE_PERF',JSON.stringify(perf));
  const critical=errors.filter(e=>!e.includes('favicon'));
  if(critical.length)console.log('BROWSER_DIAGNOSTICS\n'+critical.join('\n'));
  console.log('FAST_COMMERCE_SMOKE_OK');
  await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});
