---
{"title":"Disney DCF Valuation","slug":"disney-valuation","category":"Finance · Valuation","description":"A historical discounted cash flow analysis connecting operating assumptions, cost of capital, and equity value.","tools":["Excel","FCFF","Sensitivity analysis"],"image":"/images/DIS_FCFF_Projection.png","image_alt":"Original Disney ten-year free cash flow forecast chart","featured":true,"status":"Historical analysis","date":"2025-08-22"}
---
## Executive summary

This independent analysis values Disney using free cash flow to the firm (FCFF). The memorandum is dated **22 August 2025**. Its base case reports **$50.55 per share**, compared with a **$118.86** market-price reference used in the original analysis. These are historical figures, not a current price target or investment recommendation.

[Read the original memorandum (PDF)](/documents/DIS-Memo.pdf) · [Download the original model (Excel)](/documents/dis_fcffsimpleginzu.xlsx)

## Valuation thesis and research question

What assumptions about cash generation and reinvestment are needed to support the market-price reference? The memorandum contrasts Disney's brand and intellectual property with a conservative model of returns and reinvestment. Its conclusion depends on those assumptions rather than demonstrating a single objectively correct valuation.

## My contribution

The memorandum names Eshaan Arora as its author. The project includes an FCFF workbook, investor memorandum, and four supporting exhibits. The website preserves these original materials and presents their dated findings together.

## Key assumptions and methodology

The report uses a ten-year explicit forecast and a terminal value. It describes an initial WACC of about 10.3%, declining to about 8.7% in the terminal period, conservative reinvestment efficiency, and a terminal return on invested capital converging to the cost of capital. Consult the workbook for the detailed inputs and formulas.

In a stable-growth FCFF model:

<p class="equation"><var>Enterprise value</var> = Σ FCFF<sub>t</sub> / (1 + WACC)<sup>t</sup> + discounted terminal value</p>

<p class="equation"><var>Terminal value</var> = FCFF<sub>n+1</sub> / (WACC<sub>terminal</sub> − g)</p>

The workbook uses changing assumptions over time; the expressions above explain the general method rather than reproducing every spreadsheet formula. Stable-growth terminal value requires terminal WACC to exceed growth. Enterprise value is adjusted for debt, cash, minority interests, and options to arrive at equity value.

## Implementation and original exhibits

![Original enterprise-to-equity valuation bridge](/images/DIS_EV_to_Equity_Bridge.png)

![Original ten-year FCFF projection](/images/DIS_FCFF_Projection.png)

![Original present-value composition of explicit cash flows and terminal value](/images/DIS_PV_Composition.png)

![Original sensitivity of valuation to WACC](/images/DIS_Sensitivity_WACC.png)

## Results and sensitivity

The original website reports this sensitivity snapshot. It is preserved as historical model output; it has not been independently recomputed during the redesign.

| WACC | Value per share | Percentage of historical $118.86 reference |
| --- | --- | --- |
| 8.0% | $61.30 | 51.6% |
| 8.5% | $58.75 | 49.5% |
| 9.0% | $56.30 | 47.4% |
| 9.5% | $54.00 | 45.5% |
| 10.0% | $51.70 | 43.5% |

## Limitations and lessons

DCF values are sensitive to discount rates, terminal growth, reinvestment, and the durability of excess returns. The memo's scenario ranges and this one-dimensional WACC snapshot use different assumptions and should not be treated as identical cases. A two-dimensional sensitivity analysis would be a useful extension, but is not newly implemented here.

The valuation is tied to its 2025 inputs. The original documents retain their original language and market reference. Updating the model would require fresh financial statements and a new valuation date.

## Resources

- [Investor memorandum (PDF)](/documents/DIS-Memo.pdf)
- [Original FCFF model (Excel)](/documents/dis_fcffsimpleginzu.xlsx)
