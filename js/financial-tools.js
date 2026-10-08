/* Pure per-period formulas. No network requests or third-party runtime. */
function calculateFinancialValue({ kind, amount, rate, periods, coupon = 0 }) {
  if (![amount, rate, periods, coupon].every(Number.isFinite) || amount < 0 || coupon < 0 || rate <= -100 || !Number.isInteger(periods) || periods < 0 || periods > 1000) {
    throw new Error('Use nonnegative amounts, a rate above −100%, and 0–1,000 whole periods.');
  }
  if (!['future', 'present', 'annuity', 'bond'].includes(kind)) throw new Error('Choose a supported calculation.');
  if (amount === 0) return 0;
  const r = rate / 100;
  const factor = Math.exp(periods * Math.log1p(r));
  const annuityFactor = r === 0 ? periods : -Math.expm1(-periods * Math.log1p(r)) / r;
  let value;
  if (kind === 'future') value = amount * factor;
  else if (kind === 'present') value = amount / factor;
  else if (kind === 'annuity') value = amount * annuityFactor;
  else if (kind === 'bond') value = amount * coupon / 100 * annuityFactor + amount / factor;
  else throw new Error('Choose a supported calculation.');
  if (!Number.isFinite(value)) throw new Error('These assumptions exceed the calculator’s numeric range. Try fewer periods or a less extreme rate.');
  return value;
}
if (typeof module !== 'undefined') module.exports = { calculateFinancialValue };
if (typeof document !== 'undefined') {
  const form = document.getElementById('financial-form');
  const result = document.getElementById('financial-result');
  if (form && result) {
    const updateFields = () => {
      const bond = form.elements.kind.value === 'bond';
      const coupon = form.elements.coupon;
      coupon.disabled = !bond;
      coupon.closest('label').hidden = !bond;
      result.textContent = 'Enter your assumptions to calculate.';
    };
    form.elements.kind.addEventListener('change', updateFields);
    updateFields();
    form.addEventListener('submit', event => {
      event.preventDefault();
      try {
        const value = calculateFinancialValue({kind: form.elements.kind.value, amount: Number(form.elements.amount.value), rate: Number(form.elements.rate.value), periods: Number(form.elements.periods.value), coupon: Number(form.elements.coupon.value)});
        result.textContent = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD', maximumFractionDigits: 2}).format(value);
      } catch (error) { result.textContent = error.message; }
    });
  }
}
