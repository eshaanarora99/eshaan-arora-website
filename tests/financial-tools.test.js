const test = require('node:test');
const assert = require('node:assert/strict');
const { calculateFinancialValue: calc } = require('../js/financial-tools.js');
const close = (a,b) => assert.ok(Math.abs(a-b) < 1e-8 * Math.max(1,Math.abs(b)), `${a} != ${b}`);
test('present and future values invert each other', () => {
  for (const rate of [-25,0,0.0000001,5,100]) {
    const future = calc({kind:'future',amount:1250,rate,periods:20});
    close(calc({kind:'present',amount:future,rate,periods:20}),1250);
  }
  close(calc({kind:'future',amount:1000,rate:5,periods:10}),1628.894626777442);
});
test('annuity agrees with individually discounted cash flows', () => {
  for (const rate of [-5,0,0.00000001,7]) {
    const direct = Array.from({length:12},(_,i) => 100/(1+rate/100)**(i+1)).reduce((a,b)=>a+b,0);
    close(calc({kind:'annuity',amount:100,rate,periods:12}),direct);
  }
});
test('bond equals coupon stream plus principal; par bond and zero yield', () => {
  close(calc({kind:'bond',amount:1000,rate:5,coupon:5,periods:10}),1000);
  close(calc({kind:'bond',amount:1000,rate:0,coupon:5,periods:10}),1500);
  close(calc({kind:'bond',amount:1000,rate:6,coupon:4,periods:10}),
    Array.from({length:10},(_,i)=>40/1.06**(i+1)).reduce((a,b)=>a+b,0)+1000/1.06**10);
});
test('zero periods have explicit financial meaning', () => {
  close(calc({kind:'future',amount:0,rate:10000,periods:1000}),0);
  for (const kind of ['future','present','bond']) close(calc({kind,amount:100,rate:5,periods:0}),100);
  close(calc({kind:'annuity',amount:100,rate:5,periods:0}),0);
});
test('rejects invalid assumptions and numeric overflow', () => {
  const valid = {kind:'future',amount:1000,rate:5,periods:10};
  for (const patch of [{amount:-1},{amount:NaN},{rate:-100},{rate:Infinity},{periods:-1},{periods:0.5},{periods:1001},{coupon:-1},{kind:'unknown'},{rate:10000,periods:1000}]) assert.throws(()=>calc({...valid,...patch}));
});
